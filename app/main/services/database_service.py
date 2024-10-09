import datetime
import logging
from typing import Any

import psycopg2

from app.main.config.app_config import app_config

logger = logging.getLogger(__name__)


class DatabaseService:
    def __execute_query(self, sql: str, values=None):
        with psycopg2.connect(
            dbname=app_config.postgres.db,
            user=app_config.postgres.user,
            password=app_config.postgres.password,
            host=app_config.postgres.host,
            port=app_config.postgres.port,
        ) as conn:
            cur = conn.cursor()
            cur.execute(sql, values)
            data = None
            try:
                data = cur.fetchall()
            except Exception:
                pass
            conn.commit()
            return data

    def create_owner_table(self) -> None:
        self.__execute_query(
            sql="""
                    CREATE TABLE IF NOT EXISTS owner (
                        id SERIAL PRIMARY KEY,
                        name varchar
                    )
                """
        )

    def create_relationship_table(self) -> None:
        self.__execute_query(
            sql="""
                    CREATE TABLE IF NOT EXISTS relationship (
                        id SERIAL PRIMARY KEY,
                        type varchar,
                        data jsonb not null default '{}'::jsonb,
                        asset_id integer references asset(id),
                        owner_id integer references owner(id)
                    )
                """
        )

    def create_asset_table(self) -> None:
        self.__execute_query(
            sql="""
                    CREATE TABLE IF NOT EXISTS asset (
                        id SERIAL PRIMARY KEY,
                        type varchar,
                        name varchar
                    )
                """
        )

    def clean_all_stubbed_values(self) -> None:
        self.__execute_query(sql="DELETE FROM relationship WHERE type LIKE 'STUBBED%'")
        self.__execute_query(sql="DELETE FROM owner WHERE name LIKE 'STUBBED%'")
        self.__execute_query(sql="DELETE FROM asset WHERE type LIKE 'STUBBED%'")

    def add_owner(self, name: str) -> None:
        self.__execute_query(
            "INSERT INTO owner (name) VALUES (%s);",
            values=[name],
        )

    def find_owner_by_name(self, name: str) -> list[tuple[Any, Any]]:
        return (
            self.__execute_query(
                sql="SELECT id, name FROM owner WHERE name = %s;",
                values=[name],
            )
            or []
        )

    def add_asset(self, type: str, name: str):
        self.__execute_query(
            "INSERT INTO asset (type, name) VALUES (%s, %s);",
            values=[type, name],
        )

    def add_asset_if_name_does_not_exist(self, type: str, name: str):
        results = self.find_asset_by_name(name)

        if not results:
            logger.info(f"Creating asset [ {name} ] because it does not exist")
            self.add_asset(type, name)

    def find_asset_by_name(self, name: str) -> list[tuple[Any, Any, Any]]:
        return (
            self.__execute_query(
                sql="SELECT id, type, name FROM asset WHERE name = %s;",
                values=[name],
            )
            or []
        )

    def add_relationship(self, type: str, asset_id: int, owner_id):
        self.__execute_query(
            "INSERT INTO relationship (type, asset_id, owner_id) VALUES (%s, %s, %s);",
            values=[type, asset_id, owner_id],
        )

    def update_relationship(self, type: str, asset_id: int, owner_id):
        results = (
            self.__execute_query(
                sql="SELECT * FROM relationship WHERE type = %s AND owner_id = %s and asset_id = %s;",
                values=[type, owner_id, asset_id],
            )
            or []
        )

        if not results:
            logger.info(
                f"Creating relationship [ {type} ] for asset [ {asset_id} ] and owner [ {owner_id} ] because it does not exist"
            )
            self.add_relationship(type, asset_id, owner_id)

    def add_relationship_between_asset_and_owner(
        self, asset_name: str, owner_id: int, type: str = "OTHER"
    ):
        self.add_asset_if_name_does_not_exist("REPOSITORY", asset_name)
        asset_id, _, _ = self.find_asset_by_name(asset_name)[0]

        self.update_relationship(
            "OTHER",
            asset_id,
            owner_id,
        )

    def add_stubbed_values(self):
        logger.info("Adding Stubs...")
        self.add_owner("STUBBED_PLATFORMS_AND_ARCHITECTURES")
        panda_owner_id, _ = self.find_owner_by_name(
            "STUBBED_PLATFORMS_AND_ARCHITECTURES"
        )[0]

        self.add_owner("STUBBED_HMPPS")
        hmpps_owner_id, _ = self.find_owner_by_name("STUBBED_HMPPS")[0]

        self.add_owner("STUBBED_OPG")
        opg_owner_id, _ = self.find_owner_by_name("STUBBED_OPG")[0]

        self.add_owner("STUBBED_LAA")
        laa_owner_id, _ = self.find_owner_by_name("STUBBED_LAA")[0]

        self.add_asset("STUBBED_REPOSITORY", "operations-engineering")
        operations_engineering_asset_id, _, _ = self.find_asset_by_name(
            "operations-engineering"
        )[0]

        self.add_asset("STUBBED_REPOSITORY", "operations-engineering-testing")
        operations_engineering_testing_asset_id, _, _ = self.find_asset_by_name(
            "operations-engineering-testing"
        )[0]

        self.add_asset("STUBBED_REPOSITORY", "hmpps-auth")
        hmpps_auth_asset_id, _, _ = self.find_asset_by_name("hmpps-auth")[0]

        self.add_asset("STUBBED_REPOSITORY", "opg-api")
        opg_api_asset_id, _, _ = self.find_asset_by_name("opg-api")[0]

        self.add_asset("STUBBED_REPOSITORY", "laa-infrastructure")
        laa_infrastructure_asset_id, _, _ = self.find_asset_by_name(
            "laa-infrastructure"
        )[0]

        self.add_asset("STUBBED_REPOSITORY", "laa-api")
        laa_api_asset_id, _, _ = self.find_asset_by_name("laa-api")[0]

        self.add_relationship(
            "STUBBED_OTHER",
            operations_engineering_asset_id,
            panda_owner_id,
        )
        self.add_relationship(
            "STUBBED_OWNER_HAS_ADMIN_ACCESS",
            operations_engineering_testing_asset_id,
            panda_owner_id,
        )
        self.add_relationship(
            "STUBBED_OWNER_HAS_ADMIN_ACCESS",
            operations_engineering_testing_asset_id,
            hmpps_owner_id,
        )
        self.add_relationship(
            "STUBBED_OWNER_HAS_ADMIN_ACCESS",
            hmpps_auth_asset_id,
            hmpps_owner_id,
        )
        self.add_relationship(
            "STUBBED_OWNER_HAS_ADMIN_ACCESS",
            laa_api_asset_id,
            laa_owner_id,
        )
        self.add_relationship(
            "STUBBED_OWNER_HAS_ADMIN_ACCESS",
            opg_api_asset_id,
            opg_owner_id,
        )

        self.find_all_repositories()

    def find_all_repositories(self):
        response = self.__execute_query("""
            SELECT 
                a.name AS asset_name,
                o.name AS owner_name,
                r.type AS relationship_type
            FROM 
                asset a
            LEFT JOIN 
                relationship r ON a.id = r.asset_id
            LEFT JOIN 
                owner o ON r.owner_id = o.id
            ORDER BY 
                a.id, o.id
        """)

        asset_owners_map = {}
        for asset_name, owner_name, relationship_type in response:
            if asset_name not in asset_owners_map:
                asset_owners_map[asset_name] = {"name": asset_name, "owners": []}

            if owner_name and relationship_type:
                asset_owners_map[asset_name]["owners"].append(
                    {"owner_name": owner_name, "relationship_type": relationship_type}
                )

        flattened_assets = list(asset_owners_map.values())
        return flattened_assets

    def find_all_owners(self):
        owners = (
            self.__execute_query("""
            SELECT name
            FROM owner
        """)
            or []
        )

        response = []
        for name in owners:
            response += name

        return response
