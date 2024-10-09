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
    repositories = github_service.get_all_repositories(limit=100)

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

    strict_search = False
    direct_access_level = (
        "github_teams_with_admin_access"
        if strict_search
        else "github_teams_with_any_access"
    )
    parent_access_level = (
        "github_teams_with_admin_access_parents"
        if strict_search
        else "github_teams_with_any_access_parents"
    )

    unownedRepos = []
    reposWithMultipleOwners = []
    hmppsRepos = []
    laaRepos = []
    opgRepos = []
    cicaRepos = []
    centralDigitalRepos = []
    platformsAndArchitectureRepos = []
    techServicesRepos = []

    for repository in repositories:
        ownersFound = 0
        if (
            # HMPPS Digital
            "HMPPS Developers" in repository[direct_access_level]
            or "HMPPS Developers" in repository[parent_access_level]
            # Fuzzy Matches 👇
            or repository["name"].startswith("hmpps-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository["name"], hmpps_owner_id
            )
            hmppsRepos.append(repository)
            ownersFound += 1

            if (
                "HMPPS Developers" in repository["github_teams_with_admin_access"]
                or "HMPPS Developers"
                in repository["github_teams_with_admin_access_parents"]
            ):
                database_service.add_relationship_between_asset_and_owner(
                    repository["name"], hmpps_owner_id, "ADMIN_ACCESS"
                )

        if (
            # LAA Digital
            "LAA Technical Architects" in repository[direct_access_level]
            or "LAA Technical Architects" in repository[parent_access_level]
            or "LAA Developers" in repository[direct_access_level]
            or "LAA Developers" in repository[parent_access_level]
            or "LAA Crime Apps team" in repository[direct_access_level]
            or "LAA Crime Apps team" in repository[parent_access_level]
            or "LAA Crime Apply" in repository[direct_access_level]
            or "LAA Crime Apply" in repository[parent_access_level]
            or "laa-eligibility-platform" in repository[direct_access_level]
            or "laa-eligibility-platform" in repository[parent_access_level]
            or "LAA Get Access" in repository[direct_access_level]
            or "LAA Get Access" in repository[parent_access_level]
            or "LAA Payments and Billing" in repository[direct_access_level]
            or "LAA Payments and Billing" in repository[parent_access_level]
            # Fuzzy Matches 👇
            or repository["name"].startswith("laa-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository["name"], laa_owner_id
            )
            laaRepos.append(repository)
            ownersFound += 1

            if (
                "LAA Technical Architects"
                in repository["github_teams_with_admin_access"]
                or "LAA Technical Architects"
                in repository["github_teams_with_admin_access_parents"]
                or "LAA Developers" in repository["github_teams_with_admin_access"]
                or "LAA Developers"
                in repository["github_teams_with_admin_access_parents"]
                or "LAA Crime Apps team" in repository["github_teams_with_admin_access"]
                or "LAA Crime Apps team"
                in repository["github_teams_with_admin_access_parents"]
                or "LAA Crime Apply" in repository["github_teams_with_admin_access"]
                or "LAA Crime Apply"
                in repository["github_teams_with_admin_access_parents"]
                or "laa-eligibility-platform"
                in repository["github_teams_with_admin_access"]
                or "laa-eligibility-platform"
                in repository["github_teams_with_admin_access_parents"]
                or "LAA Get Access" in repository["github_teams_with_admin_access"]
                or "LAA Get Access"
                in repository["github_teams_with_admin_access_parents"]
                or "LAA Payments and Billing"
                in repository["github_teams_with_admin_access"]
                or "LAA Payments and Billing"
                in repository["github_teams_with_admin_access_parents"]
            ):
                database_service.add_relationship_between_asset_and_owner(
                    repository["name"], laa_owner_id, "ADMIN_ACCESS"
                )
        if (
            # OPG Digital
            "OPG" in repository[direct_access_level]
            or "OPG" in repository[parent_access_level]
            # Fuzzy Matches 👇
            or repository["name"].startswith("opg-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository["name"], opg_owner_id
            )
            opgRepos.append(repository)
            ownersFound += 1

            if (
                "OPG" in repository["github_teams_with_admin_access"]
                or "OPG" in repository["github_teams_with_admin_access_parents"]
            ):
                database_service.add_relationship_between_asset_and_owner(
                    repository["name"], opg_owner_id, "ADMIN_ACCESS"
                )

        if (
            # CICA Digital
            "CICA" in repository[direct_access_level]
            or "CICA" in repository[parent_access_level]
            # Fuzzy Matches 👇
            or repository["name"].startswith("cica-")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository["name"], cica_owner_id
            )
            cicaRepos.append(repository)
            ownersFound += 1

            if (
                "CICA" in repository["github_teams_with_admin_access"]
                or "CICA" in repository["github_teams_with_admin_access_parents"]
            ):
                database_service.add_relationship_between_asset_and_owner(
                    repository["name"], cica_owner_id, "ADMIN_ACCESS"
                )
        if (
            # Central Digital
            "Central Digital Product Team" in repository[direct_access_level]
            or "Central Digital Product Team" in repository[parent_access_level]
            or "tactical-products" in repository[direct_access_level]
            or "tactical-products" in repository[parent_access_level]
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository["name"], central_digital_owner_id
            )
            centralDigitalRepos.append(repository)
            ownersFound += 1

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
                    repository["name"], central_digital_owner_id, "ADMIN_ACCESS"
                )

        if (
            # Platforms and Architecture https://peoplefinder.service.gov.uk/teams/platforms
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
                repository[direct_access_level],
            )
            ## Criminal Justice Services
            # Fuzzy Matches 👇
            or repository["name"].startswith("bichard7")
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository["name"], platforms_and_architecture_owner_id
            )
            platformsAndArchitectureRepos.append(repository)
            ownersFound += 1

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
                repository["github_teams_with_admin_access"],
            ):
                database_service.add_relationship_between_asset_and_owner(
                    repository["name"], central_digital_owner_id, "ADMIN_ACCESS"
                )
        if (
            # Tech Services
            "nvvs-devops-admins" in repository[direct_access_level]
            or "nvvs-devops-admins" in repository[parent_access_level]
            or "moj-official-techops" in repository[direct_access_level]
            or "moj-official-techops" in repository[parent_access_level]
        ):
            database_service.add_relationship_between_asset_and_owner(
                repository["name"], tech_services_owner_id
            )
            techServicesRepos.append(repository)
            ownersFound += 1

            if (
                "nvvs-devops-admins" in repository["github_teams_with_admin_access"]
                or "nvvs-devops-admins"
                in repository["github_teams_with_admin_access_parents"]
                or "moj-official-techops"
                in repository["github_teams_with_admin_access"]
                or "moj-official-techops"
                in repository["github_teams_with_admin_access_parents"]
            ):
                database_service.add_relationship_between_asset_and_owner(
                    repository["name"], cica_owner_id, "ADMIN_ACCESS"
                )

        if ownersFound == 0:
            database_service.add_asset_if_name_does_not_exist(
                "REPOSITORY", repository["name"]
            )
            unownedRepoCount = unownedRepos.append(repository)

        if ownersFound > 1:
            reposWithMultipleOwners.append(repository)

    unownedRepoCount = len(unownedRepos)
    hmppsRepoCount = len(hmppsRepos)
    laaRepoCount = len(laaRepos)
    opgRepoCount = len(opgRepos)
    cicaRepoCount = len(cicaRepos)
    centralDigitalRepoCount = len(centralDigitalRepos)
    platformsAndArchitectureRepoCount = len(platformsAndArchitectureRepos)
    techServicesRepoCount = len(techServicesRepos)
    reposWithMultipleOwnersCount = len(reposWithMultipleOwners)
    totalRepositories = len(repositories)
    totalFound = totalRepositories - unownedRepoCount

    logger.debug(
        json.dumps(
            {
                "totals": {
                    "totalRepos": totalRepositories,
                    "totalReposWithFoundOwners": [
                        totalFound,
                        convert_to_percentage(totalFound, totalRepositories),
                    ],
                    "reposWithMultipleOwnersCount": [
                        reposWithMultipleOwnersCount,
                        convert_to_percentage(
                            reposWithMultipleOwnersCount, totalRepositories
                        ),
                    ],
                    "unownedRepoCount": [
                        unownedRepoCount,
                        convert_to_percentage(unownedRepoCount, totalRepositories),
                    ],
                    "hmppsRepoCount": [
                        hmppsRepoCount,
                        convert_to_percentage(hmppsRepoCount, totalRepositories),
                    ],
                    "laaRepoCount": [
                        laaRepoCount,
                        convert_to_percentage(laaRepoCount, totalRepositories),
                    ],
                    "opgRepoCount": [
                        opgRepoCount,
                        convert_to_percentage(opgRepoCount, totalRepositories),
                    ],
                    "cicaRepoCount": [
                        cicaRepoCount,
                        convert_to_percentage(cicaRepoCount, totalRepositories),
                    ],
                    "centralDigitalRepoCount": [
                        centralDigitalRepoCount,
                        convert_to_percentage(
                            centralDigitalRepoCount, totalRepositories
                        ),
                    ],
                    "platformsAndArchitectureRepoCount": [
                        platformsAndArchitectureRepoCount,
                        convert_to_percentage(
                            platformsAndArchitectureRepoCount, totalRepositories
                        ),
                    ],
                    "techServicesRepoCount": [
                        techServicesRepoCount,
                        convert_to_percentage(techServicesRepoCount, totalRepositories),
                    ],
                },
                "repositories": {
                    "hmpps": hmppsRepos,
                    "laa": laaRepos,
                    "opg": opgRepos,
                    "cica": cicaRepos,
                    "centralDigital": centralDigitalRepos,
                    "platformsAndArchitecture": platformsAndArchitectureRepos,
                    "techServices": techServicesRepos,
                    "all": repositories,
                    "unownedRepos": unownedRepos,
                    "reposWithMultipleOwners": reposWithMultipleOwners,
                },
            }
        )
    )
    logger.info("Complete!")


if __name__ == "__main__":
    main()
