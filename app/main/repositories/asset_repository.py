from sqlalchemy import join
from sqlalchemy.orm import scoped_session, joinedload
from flask import g
from app.main.models import Asset, Owner, Relationship, db
from app.main.routes import owner


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


def get_asset_repository() -> AssetRepository:
    if "asset_repository" not in g:
        g.asset_repository = AssetRepository()
    return g.asset_repository
