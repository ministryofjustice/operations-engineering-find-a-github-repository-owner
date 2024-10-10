import unittest
from unittest.mock import MagicMock, call, patch
from app.jobs.map_github_repositories_to_owners import main


@patch("app.main.services.github_service.GithubService.__new__")
@patch("app.main.services.database_service.DatabaseService.__new__")
class TestMain(unittest.TestCase):
    def test_admin_relationship_created_between_hmpps_and_repo_by_admin_team_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": ["HMPPS Developers"],
                "github_teams_with_any_access": ["HMPPS Developers"],
                "github_teams_with_admin_access_parents": ["HMPPS Developers"],
                "github_teams_with_any_access_parents": ["HMPPS Developers"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1, "ADMIN_ACCESS")]
        )

    def test_default_relationship_created_between_hmpps_and_repo_by_team_with_any_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": ["HMPPS Developers"],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": ["HMPPS Developers"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1)]
        )

    def test_default_relationship_created_between_hmpps_and_repo_by_prefix(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "hmpps-test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": [],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": [],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("hmpps-test", 1)]
        )

    def test_admin_relationship_created_between_laa_and_repo_by_admin_team_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": ["LAA Technical Architects"],
                "github_teams_with_any_access": ["LAA Technical Architects"],
                "github_teams_with_admin_access_parents": ["LAA Technical Architects"],
                "github_teams_with_any_access_parents": ["LAA Technical Architects"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1, "ADMIN_ACCESS")]
        )

    def test_default_relationship_created_between_laa_and_repo_by_team_with_any_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": ["LAA Technical Architects"],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": ["LAA Technical Architects"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1)]
        )

    def test_default_relationship_created_between_laa_and_repo_by_prefix(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "laa-test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": [],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": [],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("laa-test", 1)]
        )

    def test_admin_relationship_created_between_opg_and_repo_by_admin_team_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": ["OPG"],
                "github_teams_with_any_access": ["OPG"],
                "github_teams_with_admin_access_parents": ["OPG"],
                "github_teams_with_any_access_parents": ["OPG"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1, "ADMIN_ACCESS")]
        )

    def test_default_relationship_created_between_opg_and_repo_by_team_with_any_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": ["OPG"],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": ["OPG"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1)]
        )

    def test_default_relationship_created_between_opg_and_repo_by_prefix(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "opg-test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": [],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": [],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("opg-test", 1)]
        )

    def test_admin_relationship_created_between_cica_and_repo_by_admin_team_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": ["CICA"],
                "github_teams_with_any_access": ["CICA"],
                "github_teams_with_admin_access_parents": ["CICA"],
                "github_teams_with_any_access_parents": ["CICA"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1, "ADMIN_ACCESS")]
        )

    def test_default_relationship_created_between_cica_and_repo_by_team_with_any_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": ["CICA"],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": ["CICA"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1)]
        )

    def test_default_relationship_created_between_cica_and_repo_by_prefix(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "cica-test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": [],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": [],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("cica-test", 1)]
        )

    def test_admin_relationship_created_between_central_digital_and_repo_by_admin_team_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": ["Central Digital Product Team"],
                "github_teams_with_any_access": ["Central Digital Product Team"],
                "github_teams_with_admin_access_parents": [
                    "Central Digital Product Team"
                ],
                "github_teams_with_any_access_parents": [
                    "Central Digital Product Team"
                ],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1, "ADMIN_ACCESS")]
        )

    def test_default_relationship_created_between_central_digital_and_repo_by_team_with_any_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": ["Central Digital Product Team"],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": [
                    "Central Digital Product Team"
                ],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1)]
        )

    def test_admin_relationship_created_between_platforms_and_architectures_and_repo_by_admin_team_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": ["operations-engineering"],
                "github_teams_with_any_access": ["operations-engineering"],
                "github_teams_with_admin_access_parents": ["operations-engineering"],
                "github_teams_with_any_access_parents": ["operations-engineering"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1, "ADMIN_ACCESS")]
        )

    def test_default_relationship_created_between_platforms_and_architectures_and_repo_by_team_with_any_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": ["operations-engineering"],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": ["operations-engineering"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1)]
        )

    def test_admin_relationship_created_between_platforms_and_architectures_and_repo_by_admin_team_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "bichard7-test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": [],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": [],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("bichard7-test", 1)]
        )

    def test_admin_relationship_created_between_tech_services_and_repo_by_admin_team_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": ["nvvs-devops-admins"],
                "github_teams_with_any_access": ["nvvs-devops-admins"],
                "github_teams_with_admin_access_parents": ["nvvs-devops-admins"],
                "github_teams_with_any_access_parents": ["nvvs-devops-admins"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1, "ADMIN_ACCESS")]
        )

    def test_default_relationship_created_between_tech_services_and_repo_by_team_with_any_access(
        self, mock_database_service: MagicMock, mock_github_service: MagicMock
    ):
        mock_github_service.return_value.get_all_repositories.return_value = [
            {
                "name": "test",
                "github_teams_with_admin_access": [],
                "github_teams_with_any_access": ["nvvs-devops-admins"],
                "github_teams_with_admin_access_parents": [],
                "github_teams_with_any_access_parents": ["nvvs-devops-admins"],
            },
        ]
        mock_database_service.return_value.find_owner_by_name.return_value = [(1, None)]

        main()

        mock_database_service.return_value.add_relationship_between_asset_and_owner.assert_has_calls(
            [call("test", 1)]
        )


if __name__ == "__main__":
    unittest.main()
