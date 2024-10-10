import unittest
from unittest.mock import MagicMock, call, patch
from app.jobs.map_github_repositories_to_owners import main


@patch("app.main.services.github_service.GithubService.__new__")
@patch("app.main.services.database_service.DatabaseService.__new__")
class TestMain(unittest.TestCase):
    def test_admin_relationship_created_between_hmpps_and_repo(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "hmpps-test",
                "github_teams_with_admin_access": ["HMPPS Developers"],
                "github_teams_with_any_access": ["HMPPS Developers"],
                "github_teams_with_admin_access_parents": ["HMPPS Developers"],
                "github_teams_with_any_access_parents": ["HMPPS Developers"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("hmpps-test", 1, "ADMIN_ACCESS")]
        )


if __name__ == "__main__":
    unittest.main()
