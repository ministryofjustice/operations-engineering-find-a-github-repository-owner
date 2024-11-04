from app.main.models import Asset, db
from flask import g
from sqlalchemy.orm import scoped_session


class AssetView:
    def __init__(self, name: str, owners: list[str]):
        self.name = name
        self.owners = owners

    @classmethod
    def from_asset(cls, asset: Asset):
        filtered_owners = [
            relationship.owner.name
            for relationship in asset.relationships
            if "ADMIN_ACCESS" in relationship.type
        ]
        return cls(name=asset.name, owners=filtered_owners)


class AssetRepository:
    def __init__(self, db_session: scoped_session = db.session):
        self.db_session = db_session

    def find_all(self) -> list[Asset]:
        return self.db_session.query(Asset).all()

    def find_all_by_owner(self, owner_name: str) -> list[Asset]:
        assets = (
            self.db_session.query(Asset)
            .join(Asset.owners)
            .filter(Asset.owners.any(name=owner_name))
            .all()
        )

        return list(assets)

    def find_by_repository_name_and_relationship_type(
        self, name: str, relationship_type: str
    ) -> AssetView | None:
        asset = self.db_session.query(Asset).filter(Asset.name == name).first()

        if asset:
            return AssetView.from_asset(asset)
        else:
            return None


def get_asset_repository() -> AssetRepository:
    if "asset_repository" not in g:
        g.asset_repository = AssetRepository()
    return g.asset_repository
