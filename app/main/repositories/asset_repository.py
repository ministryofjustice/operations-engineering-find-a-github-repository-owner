from app.main.models import Asset, Relationship, db, Owner
from flask import g
from sqlalchemy.orm import scoped_session
from typing import List


class AssetView:
    def __init__(self, name: str, owner_names: List[str], admin_owner_names: List[str]):
        self.name = name
        self.admin_owner_names = admin_owner_names
        self.owner_names = owner_names

    @classmethod
    def from_asset(cls, asset: Asset):
        owner_names = [relationship.owner.name for relationship in asset.relationships]
        admin_owner_names = [
            relationship.owner.name
            for relationship in asset.relationships
            if "ADMIN_ACCESS" in relationship.type
        ]
        return cls(
            name=asset.name,
            owner_names=owner_names,
            admin_owner_names=admin_owner_names,
        )


class AssetRepository:
    def __init__(self, db_session: scoped_session = db.session):
        self.db_session = db_session

    def find_all(self) -> list[AssetView]:
        assets = self.db_session.query(Asset).all()

        return [AssetView.from_asset(asset) for asset in assets]

    def find_all_by_owners(self, owner_names: list[str]) -> list[AssetView]:
        assets = (
            self.db_session.query(Asset)
            .join(Asset.owners)
            .filter(Owner.name.in_(owner_names))
            .distinct()
            .all()
        )

        return [AssetView.from_asset(asset) for asset in assets]

    def find_all_by_owner(self, owner_name: str) -> list[AssetView]:
        assets = (
            self.db_session.query(Asset)
            .join(Asset.owners)
            .filter(Asset.owners.any(name=owner_name))
            .all()
        )

        return [AssetView.from_asset(asset) for asset in assets]

    def add_asset(self, name: str, type: str) -> Asset:
        asset = Asset()
        asset.name = name
        asset.type = type
        self.db_session.add(asset)
        self.db_session.commit()
        return asset

    def create_relationship(
        self, asset: Asset, owner: Owner, relationship_type: str
    ) -> Relationship:
        relationship = Relationship()
        relationship.owner_id = owner.id
        relationship.asset_id = asset.id
        relationship.type = relationship_type
        self.db_session.add(relationship)
        self.db_session.commit()
        return relationship

    def clean_all_tables(self):
        self.db_session.query(Relationship).delete()
        self.db_session.query(Owner).delete()
        self.db_session.query(Asset).delete()


def get_asset_repository() -> AssetRepository:
    if "asset_repository" not in g:
        g.asset_repository = AssetRepository()
    return g.asset_repository
