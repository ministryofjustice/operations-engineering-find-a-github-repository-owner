import unittest
from unittest.mock import MagicMock, call, patch
from app.jobs.map_github_repositories_to_owners import main

test_owner_id = 1


@patch("app.main.services.github_service.GithubService.__new__")
@patch("app.main.services.database_service.DatabaseService.__new__")
class TestMain(unittest.TestCase):
    def test_when_team_has_direct_admin_access_then_admin_relationship_created(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "Test Repository",
                "github_teams_with_admin_access": ["Admin Team"],
                "github_teams_with_any_access": [],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": [],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [
            (test_owner_id, None)
        ]

        main(owners=[{"name": "Test Owners", "teams": ["Admin Team"]}])

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("Test Repository", test_owner_id, "ADMIN_ACCESS")]
        )

    def test_when_parent_team_has_admin_access_then_admin_relationship_created(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "Test Repository",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": [],
                "github_teams_with_admin_access_parents": ["Admin Team"],
                "github_teams_with_any_access_parents": [],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [
            (test_owner_id, None)
        ]

        main(owners=[{"name": "Test Owners", "teams": ["Admin Team"]}])

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("Test Repository", test_owner_id, "ADMIN_ACCESS")]
        )

    def test_when_team_has_any_access_then_default_relationship_created(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "Test Repository",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": ["Test Team"],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": [],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [
            (test_owner_id, None)
        ]

        main(owners=[{"name": "Test Owners", "teams": ["Test Team"]}])

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("Test Repository", test_owner_id)]
        )

    def test_when_parent_team_has_any_access_then_default_relationship_created(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "Test Repository",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": [],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": ["Test Team"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [
            (test_owner_id, None)
        ]

        main(owners=[{"name": "Test Owners", "teams": ["Test Team"]}])

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("Test Repository", test_owner_id)]
        )

    def test_when_prefix_matches_repository_name_then_default_relationship_created(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test-prefix-Test Repository",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": [],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": [],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [
            (test_owner_id, None)
        ]

        main(
            owners=[
                {
                    "name": "Test Owners",
                    "teams": ["Test Team"],
                    "prefix": "test-prefix-",
                }
            ]
        )

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test-prefix-Test Repository", test_owner_id)]
        )


if __name__ == "__main__":
    unittest.main()
