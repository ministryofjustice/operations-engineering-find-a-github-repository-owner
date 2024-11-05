from app.main.models import Asset, db
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

    def find_all_by_owner(self, owner_name: str) -> list[AssetView]:
        assets = (
            self.db_session.query(Asset)
            .join(Asset.owners)
            .filter(Asset.owners.any(name=owner_name))
            .all()
        )

        return [AssetView.from_asset(asset) for asset in assets]

    def find_by_repository_name(self, name: str) -> AssetView | None:
        asset = self.db_session.query(Asset).filter(Asset.name == name).first()

        if asset:
            return AssetView.from_asset(asset)
        else:
            return None


def get_asset_repository() -> AssetRepository:
    if "asset_repository" not in g:
        g.asset_repository = AssetRepository()
    return g.asset_repository
