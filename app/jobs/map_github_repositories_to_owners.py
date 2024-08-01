from app.main.services import database_service
from app.main.services.database_service import DatabaseService
import logging
from app.main.config.app_config import app_config
from app.main.config.logging_config import configure_logging


logger = logging.getLogger(__name__)


def main():
    configure_logging(app_config.logging_level)
    print("Running...")
    database_service = DatabaseService()
    database_service.find_all_repositories()


if __name__ == "__main__":
    main()
