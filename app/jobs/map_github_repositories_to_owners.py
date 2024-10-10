from app.main.services.database_service import DatabaseService
import logging
from app.main.config.app_config import app_config
from app.main.config.logging_config import configure_logging
from app.main.services.github_service import GithubService

logger = logging.getLogger(__name__)


def contains_one_or_more(values: list[str], lists_to_check: list[list[str]]) -> bool:
    found = False

    for value in values:
        for list_to_check in lists_to_check:
            if value in list_to_check:
                found = True

    return found


def main(
    owners=[{"name": "HMPPS", "teams": ["HMPPS Developers"], "prefix": "hmpps-"}],
    hmpps_teams=["HMPPS Developers"],
    laa_teams=[
        "LAA Technical Architects",
        "LAA Developers",
        "LAA Crime Apps team",
        "LAA Crime Apply",
        "laa-eligibility-platform",
        "LAA Get Access",
        "LAA Payments and Billing",
    ],
    opg_teams=["OPG"],
    cica_teams=["CICA"],
    central_digital_teams=["Central Digital Product Team", "tactical-products"],
    platforms_and_architecture_teams=[
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
    tech_services_teams=["nvvs-devops-admins", "moj-official-techops"],
):
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
        teams_with_admin_access = [
            github_teams_with_admin_access,
            github_teams_with_admin_access_parents,
        ]
        teams_with_any_access = [
            github_teams_with_any_access,
            github_teams_with_any_access_parents,
        ]

        # HMPPS Digital
        if contains_one_or_more(hmpps_teams, teams_with_admin_access):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, hmpps_owner_id, "ADMIN_ACCESS"
            )
        elif (
            contains_one_or_more(hmpps_teams, teams_with_any_access)
            # Fuzzy Matches 👇
            or repository_name.startswith("hmpps-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, hmpps_owner_id
            )

        # LAA Digital
        if contains_one_or_more(laa_teams, teams_with_admin_access):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, laa_owner_id, "ADMIN_ACCESS"
            )
        elif (
            contains_one_or_more(laa_teams, teams_with_any_access)
            # Fuzzy Matches 👇
            or repository_name.startswith("laa-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, laa_owner_id
            )

        # OPG Digital
        if contains_one_or_more(opg_teams, teams_with_admin_access):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, opg_owner_id, "ADMIN_ACCESS"
            )
        elif (
            contains_one_or_more(opg_teams, teams_with_any_access)
            # Fuzzy Matches 👇
            or repository_name.startswith("opg-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, opg_owner_id
            )

        # CICA Digital
        if contains_one_or_more(cica_teams, teams_with_admin_access):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, cica_owner_id, "ADMIN_ACCESS"
            )
        elif (
            contains_one_or_more(cica_teams, teams_with_any_access)
            # Fuzzy Matches 👇
            or repository_name.startswith("cica-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, cica_owner_id
            )

        # Central Digital
        if contains_one_or_more(central_digital_teams, teams_with_admin_access):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, central_digital_owner_id, "ADMIN_ACCESS"
            )
        elif contains_one_or_more(central_digital_teams, teams_with_any_access):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, central_digital_owner_id
            )

        # Platforms and Architecture https://peoplefinder.service.gov.uk/teams/platforms
        if contains_one_or_more(
            platforms_and_architecture_teams, github_teams_with_admin_access
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, platforms_and_architecture_owner_id, "ADMIN_ACCESS"
            )
        elif (
            ## Platforms
            contains_one_or_more(
                platforms_and_architecture_teams,
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
        if contains_one_or_more(
            tech_services_teams,
            github_teams_with_admin_access,
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, tech_services_owner_id, "ADMIN_ACCESS"
            )
        elif contains_one_or_more(
            tech_services_teams,
            github_teams_with_any_access,
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository_name, tech_services_owner_id
            )

        database_service.add_asset_if_name_does_not_exist("REPOSITORY", repository_name)

    logger.info("Complete!")


if __name__ == "__main__":
    main()
