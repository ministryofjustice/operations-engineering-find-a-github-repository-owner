import logging

from app.main.models import Asset
from app.main.repositories.asset_repository import AssetRepository, get_asset_repository
from flask import g


class AssetService:
    def __init__(self, asset_repository: AssetRepository):
        self.__asset_repository = asset_repository

    def get_repositories_by_authoratative_owner(
        self,
        owner_to_filter_by: str,
    ) -> list[Asset]:
        repositories = self.__asset_repository.find_all_by_owner(owner_to_filter_by)
        response = [
            repo
            for repo in repositories
            if self.__is_owner_authoritative_for_repository(repo, owner_to_filter_by)
        ]
        return response

    def get_repositories_by_authoratative_owner_filtered_by_missing_relationship(
        self, owner_to_filter_by: str, relationship_to_filter_by: str
    ) -> list[Asset]:
        repositories = self.get_repositories_by_authoratative_owner(owner_to_filter_by)

        filtered_repositories = []
        for repository in repositories:
            if (
                relationship_to_filter_by not in repository.relationships[0].type
                and repository.owners[0].name == owner_to_filter_by
            ):
                filtered_repositories.append(repository)

        return filtered_repositories

    def __is_owner_authoritative_for_repository(
        self, repository: Asset, owner_to_filter_by: str
    ) -> bool:
        owners_with_access = [
            owner for owner in repository.owners if owner.name == owner_to_filter_by
        ]
        if not owners_with_access:
            return False

        if len(owners_with_access) > 1:
            logging.error(
                f"Data Issue - Multiple owners with the same name - need to look into repository name [ ${repository.name} with ] id [ ${repository.id} ]"
            )

        owner_relationship = repository.relationships[0]

        has_admin_access = bool("ADMIN_ACCESS" in owner_relationship.type)
        if has_admin_access:
            return True

        has_other_access = bool("OTHER" in owner_relationship.type)
        repository_admins = (
            self.__asset_repository.find_by_repository_name_and_relationship_type(
                repository.name, "ADMIN_ACCESS"
            )
        )

        if not repository_admins:
            # No other admins exist
            return True

        has_authorative_ownership = (
            has_other_access and len(repository_admins.owners) == 0
        )

        if repository.name in ["cloud-platform-environments", "jwt-laminas-auth"]:
            logging.info("Hit a repo we want to check")
        return has_authorative_ownership


def get_asset_service() -> AssetService:
    if "asset_service" not in g:
        g.asset_service = AssetService(get_asset_repository())
    return g.asset_service
