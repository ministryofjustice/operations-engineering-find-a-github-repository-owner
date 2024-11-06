import logging

from flask import Flask

from app.main.config.app_config import app_config
from app.main.config.cors_config import configure_cors
from app.main.config.error_handlers_config import configure_error_handlers
from app.main.config.jinja_config import configure_jinja
from app.main.config.limiter_config import configure_limiter
from app.main.config.logging_config import configure_logging
from app.main.config.routes_config import configure_routes
from app.main.models import db
from app.main.repositories.owner_repository import get_owner_repository
from app.main.services.asset_service import get_asset_service

logger = logging.getLogger(__name__)


def create_app(is_rate_limit_enabled=True) -> Flask:
    configure_logging(app_config.logging_level)

    logger.info("Starting app...")

    app = Flask(__name__, static_folder="static", static_url_path="/assets")

    app.secret_key = app_config.flask.app_secret_key

    app.config["SQLALCHEMY_DATABASE_URI"] = app_config.postgres.sql_alchemy_database_url
    db.init_app(app)
    with app.app_context():
        db.create_all()

    configure_routes(app)
    configure_error_handlers(app)
    configure_limiter(app, is_rate_limit_enabled)
    configure_jinja(app)
    configure_cors(app)

    if app_config.add_stub_values_to_database:
        create_stub_data(app)

    logger.info("Running app...")

    return app


def create_stub_data(app):
    admin_access = "STUBBED - Admin Access"
    asset_type = "STUBBED - GitHub Repository"

    with app.app_context():
        asset_service = get_asset_service()
        owner_repository = get_owner_repository()

        asset_service.clean_all_tables()

        hmpps = owner_repository.add_owner("STUBBED - HMPPS")
        opg = owner_repository.add_owner("STUBBED - OPG")
        laa = owner_repository.add_owner("STUBBED - LAA")

        operations_engineering = asset_service.add_asset(
            "operations-engineering", asset_type
        )
        asset_service.create_relationship(operations_engineering, hmpps, admin_access)

        opg_data = asset_service.add_asset("opg-data", asset_type)
        asset_service.create_relationship(opg_data, opg, admin_access)

        cla_public = asset_service.add_asset("cla_public", asset_type)
        asset_service.create_relationship(cla_public, laa, admin_access)
