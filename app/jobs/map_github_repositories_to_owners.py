from app.main.services.database_service import DatabaseService
import logging
from app.main.config.app_config import app_config
from app.main.config.logging_config import configure_logging
from app.main.services.github_service import GithubService

import json

logger = logging.getLogger(__name__)


def convert_to_percentage(partial: int, total: int) -> str:
    return f"{round((partial / total) * 100)}%"


def contains_one_or_more(values: list[str], list_to_check: list[str]) -> bool:
    found = False

    for value in values:
        if value in list_to_check:
            found = True

    return found


def main():
    configure_logging(app_config.logging_level)
    logger.info("Running...")
    database_service = DatabaseService()
    github_service = GithubService(app_config.github.token)
    repositories = github_service.get_all_repositories()

    hmpps_owner_id, _ = database_service.find_owner_by_name("HMPPS")[0]
    laa_owner_id, _ = database_service.find_owner_by_name("LAA")[0]
    opg_owner_id, _ = database_service.find_owner_by_name("OPG")[0]
    cica_owner_id, _ = database_service.find_owner_by_name("CICA")[0]
    central_digital_owner_id, _ = database_service.find_owner_by_name(
        "Central Digital"
    )[0]
    platforms_and_architecture_owner_id, _ = database_service.find_owner_by_name(
        "Platforms and Architecture"
    )[0]
    tech_services_owner_id, _ = database_service.find_owner_by_name("Tech Services")[0]

    for repository in repositories:
        github_teams_with_admin_access = repository["github_teams_with_admin_access"]
        github_teams_with_admin_access_parents = repository[
            "github_teams_with_admin_access_parents"
        ]
        github_teams_with_any_access = repository["github_teams_with_any_access"]
        github_teams_with_any_access_parents = repository[
            "github_teams_with_any_access_parents"
        ]
        repository_name = repository["name"]

        # HMPPS Digital
        if (
            "HMPPS Developers" in github_teams_with_admin_access
            or "HMPPS Developers" in github_teams_with_admin_access_parents
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, hmpps_owner_id, "ADMIN_ACCESS"
            )
        elif (
            "HMPPS Developers" in github_teams_with_any_access
            or "HMPPS Developers" in github_teams_with_any_access_parents
            # Fuzzy Matches 👇
            or repository_name.startswith("hmpps-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, hmpps_owner_id
            )

        # LAA Digital
        if (
            "LAA Technical Architects" in github_teams_with_admin_access
            or "LAA Technical Architects" in github_teams_with_admin_access_parents
            or "LAA Developers" in github_teams_with_admin_access
            or "LAA Developers" in github_teams_with_admin_access_parents
            or "LAA Crime Apps team" in github_teams_with_admin_access
            or "LAA Crime Apps team" in github_teams_with_admin_access_parents
            or "LAA Crime Apply" in github_teams_with_admin_access
            or "LAA Crime Apply" in github_teams_with_admin_access_parents
            or "laa-eligibility-platform" in github_teams_with_admin_access
            or "laa-eligibility-platform" in github_teams_with_admin_access_parents
            or "LAA Get Access" in github_teams_with_admin_access
            or "LAA Get Access" in github_teams_with_admin_access_parents
            or "LAA Payments and Billing" in github_teams_with_admin_access
            or "LAA Payments and Billing" in github_teams_with_admin_access_parents
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, laa_owner_id, "ADMIN_ACCESS"
            )
        elif (
            "LAA Technical Architects" in github_teams_with_any_access
            or "LAA Technical Architects" in github_teams_with_any_access_parents
            or "LAA Developers" in github_teams_with_any_access
            or "LAA Developers" in github_teams_with_any_access_parents
            or "LAA Crime Apps team" in github_teams_with_any_access
            or "LAA Crime Apps team" in github_teams_with_any_access_parents
            or "LAA Crime Apply" in github_teams_with_any_access
            or "LAA Crime Apply" in github_teams_with_any_access_parents
            or "laa-eligibility-platform" in github_teams_with_any_access
            or "laa-eligibility-platform" in github_teams_with_any_access_parents
            or "LAA Get Access" in github_teams_with_any_access
            or "LAA Get Access" in github_teams_with_any_access_parents
            or "LAA Payments and Billing" in github_teams_with_any_access
            or "LAA Payments and Billing" in github_teams_with_any_access_parents
            # Fuzzy Matches 👇
            or repository_name.startswith("laa-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, laa_owner_id
            )

        # OPG Digital
        if (
            "OPG" in repository["github_teams_with_admin_access"]
            or "OPG" in repository["github_teams_with_admin_access_parents"]
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, opg_owner_id, "ADMIN_ACCESS"
            )
        elif (
            "OPG" in github_teams_with_any_access
            or "OPG" in github_teams_with_any_access_parents
            # Fuzzy Matches 👇
            or repository_name.startswith("opg-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, opg_owner_id
            )

        # CICA Digital
        if (
            "CICA" in github_teams_with_admin_access
            or "CICA" in github_teams_with_admin_access_parents
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, cica_owner_id, "ADMIN_ACCESS"
            )
        elif (
            "CICA" in github_teams_with_any_access
            or "CICA" in github_teams_with_any_access_parents
            # Fuzzy Matches 👇
            or repository_name.startswith("cica-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, cica_owner_id
            )

        # Central Digital
        if (
            "Central Digital Product Team"
            in repository["github_teams_with_admin_access"]
            or "Central Digital Product Team"
            in repository["github_teams_with_admin_access_parents"]
            or "tactical-products" in repository["github_teams_with_admin_access"]
            or "tactical-products"
            in repository["github_teams_with_admin_access_parents"]
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, central_digital_owner_id, "ADMIN_ACCESS"
            )
        elif (
            "Central Digital Product Team" in github_teams_with_any_access
            or "Central Digital Product Team" in github_teams_with_any_access_parents
            or "tactical-products" in github_teams_with_any_access
            or "tactical-products" in github_teams_with_any_access_parents
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, central_digital_owner_id
            )

        # Platforms and Architecture https://peoplefinder.service.gov.uk/teams/platforms
        if contains_one_or_more(
            [
                ### Hosting Platforms
                "modernisation-platform",
                "operations-engineering",
                "aws-root-account-admin-team",
                "WebOps",  # Cloud Platform
                "Studio Webops",  # Digital Studio Operations (DSO)
                ### Data Platforms
                "analytical-platform",
                "data-engineering",
                "analytics-hq",
                "data-catalogue",
                "data-platform",
                "data-and-analytics-engineering",
                "observability-platform",
                ### Publishing Platforms
                "Form Builder",
                "Hale platform",
                "JOTW Content Devs",
            ],
            github_teams_with_admin_access,
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, platforms_and_architecture_owner_id, "ADMIN_ACCESS"
            )
        elif (
            ## Platforms
            contains_one_or_more(
                [
                    ### Hosting Platforms
                    "modernisation-platform",
                    "operations-engineering",
                    "aws-root-account-admin-team",
                    "WebOps",  # Cloud Platform
                    "Studio Webops",  # Digital Studio Operations (DSO)
                    ### Data Platforms
                    "analytical-platform",
                    "data-engineering",
                    "analytics-hq",
                    "data-catalogue",
                    "data-platform",
                    "data-and-analytics-engineering",
                    "observability-platform",
                    ### Publishing Platforms
                    "Form Builder",
                    "Hale platform",
                    "JOTW Content Devs",
                ],
                github_teams_with_any_access,
            )
            ## Criminal Justice Services
            # Fuzzy Matches 👇
            or repository_name.startswith("bichard7")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, platforms_and_architecture_owner_id
            )

        # Tech Services
        if (
            "nvvs-devops-admins" in github_teams_with_admin_access
            or "nvvs-devops-admins" in github_teams_with_admin_access_parents
            or "moj-official-techops" in github_teams_with_admin_access
            or "moj-official-techops" in github_teams_with_admin_access_parents
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, tech_services_owner_id, "ADMIN_ACCESS"
            )
        elif (
            "nvvs-devops-admins" in github_teams_with_any_access
            or "nvvs-devops-admins" in github_teams_with_any_access_parents
            or "moj-official-techops" in github_teams_with_any_access
            or "moj-official-techops" in github_teams_with_any_access_parents
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, tech_services_owner_id
            )

        database_service.add_asset_if_name_does_not_exist("REPOSITORY", repository_name)

    logger.info("Complete!")


if __name__ == "__main__":
    main()
