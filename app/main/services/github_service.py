from calendar import timegm
from time import gmtime, sleep
from typing import Callable

from github import (
    Github,
    RateLimitExceededException,
)
from requests import Session
from github.Organization import Organization
from github.Repository import Repository
from github.Team import Team
import logging

logger = logging.getLogger(__name__)


def retries_github_rate_limit_exception_at_next_reset_once(func: Callable) -> Callable:
    def decorator(*args, **kwargs):
        """
        A decorator to retry the method when rate limiting for GitHub resets if the method fails due to Rate Limit related exception.

        WARNING: Since this decorator retries methods, ensure that the method being decorated is idempotent
         or contains only one non-idempotent method at the end of a call chain to GitHub.

         Example of idempotent methods are:
            - Retrieving data
         Example of (potentially) non-idempotent methods are:
            - Deleting data
            - Updating data
        """
        try:
            return func(*args, **kwargs)
        except RateLimitExceededException as exception:
            logger.warning(
                f"Caught {type(exception).__name__}, retrying calls when rate limit resets."
            )
            rate_limits = args[0].github_client_core_api.get_rate_limit()
            rate_limit_to_use = (
                rate_limits.core
                if isinstance(exception, RateLimitExceededException)
                else rate_limits.graphql
            )

            reset_timestamp = timegm(rate_limit_to_use.reset.timetuple())
            now_timestamp = timegm(gmtime())
            time_until_core_api_rate_limit_resets = (
                (reset_timestamp - now_timestamp)
                if reset_timestamp > now_timestamp
                else 0
            )

            wait_time_buffer = 5
            sleep(
                time_until_core_api_rate_limit_resets + wait_time_buffer
                if time_until_core_api_rate_limit_resets
                else 0
            )
            return func(*args, **kwargs)

    return decorator


class GithubService:
    def __init__(self, org_token: str) -> None:
        self.organisation_name: str = "ministryofjustice"
        self.github_client_core_api: Github = Github(org_token)

    @retries_github_rate_limit_exception_at_next_reset_once
    def __get_all_parents_team_names_of_team(self, team: Team) -> list[str]:
        parents = []

        team_has_parent = True
        team_to_check = team

        while team_has_parent:
            if team_to_check is None or team_to_check.parent is None:
                team_has_parent = False
            else:
                parents.append(team_to_check.parent.name)
                team_to_check = team_to_check.parent
        return parents

    @retries_github_rate_limit_exception_at_next_reset_once
    def __get_teams_with_access(
        self, repository: Repository
    ) -> tuple[list[str], list[str], list[str], list[str]]:
        teams_with_admin_access = []
        teams_with_admin_access_parents = []
        teams_with_any_access = []
        teams_with_any_access_parents = []
        for team in list(repository.get_teams()):
            logger.info(f"Processing Team: [ {team.name} ]")
            permissions = team.get_repo_permission(repository)
            team_parents = self.__get_all_parents_team_names_of_team(team)
            if permissions and permissions.admin:
                teams_with_admin_access.append(team.name)
                teams_with_admin_access_parents.extend(team_parents)
            if permissions and (
                permissions.admin
                or permissions.maintain
                or permissions.push
                or permissions.pull
                or permissions.triage
            ):
                teams_with_any_access.append(team.name)
                teams_with_any_access_parents.extend(team_parents)
        return (
            teams_with_admin_access,
            teams_with_admin_access_parents,
            teams_with_any_access,
            teams_with_any_access_parents,
        )

    @retries_github_rate_limit_exception_at_next_reset_once
    def get_all_repositories(self, limit: int = 1000) -> list[dict]:
        response = []
        repositories = list(
            self.github_client_core_api.get_organization(
                self.organisation_name
            ).get_repos(type="public")
        )
        repositories_to_check = [
            repository
            for repository in repositories
            if not (repository.archived or repository.fork)
        ]
        logger.info(f"Total Repositories: [ {len(repositories_to_check)} ]")
        counter = 1
        for repo in repositories_to_check:
            if counter > limit:
                logger.info("Limit Reached, exiting early")
                break
            logger.info(
                f"Processing Repository: [ {repo.name} ] {counter}/{len(repositories_to_check)}"
            )
            (
                teams_with_admin_access,
                teams_with_admin_access_parents,
                teams_with_any_access,
                teams_with_any_access_parents,
            ) = self.__get_teams_with_access(repo)
            response.append(
                {
                    "name": repo.name,
                    "github_teams_with_admin_access": teams_with_admin_access,
                    "github_teams_with_admin_access_parents": teams_with_admin_access_parents,
                    "github_teams_with_any_access": teams_with_any_access,
                    "github_teams_with_any_access_parents": teams_with_any_access_parents,
                },
            )
            counter += 1
        return response
