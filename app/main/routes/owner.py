import logging
from app.main.middleware.auth import requires_auth
from app.main.services.database_service import DatabaseService
import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request
from collections import Counter

logger = logging.getLogger(__name__)

owner_route = Blueprint("owner_route", __name__)


def generate_pie_chart_of_admin_access(repositories: list[dict], selected_owner: str):
    dataframe = pd.DataFrame(repositories)
    dataframe["owners"] = dataframe["owners"].apply(
        lambda owners: [
            owner["relationship_type"]
            for owner in owners
            if "relationship_type" in owner and owner["owner_name"] == selected_owner
        ]
        if owners
        else ["No relationships"]
    )
    all_owners = [owner for owners_list in dataframe["owners"] for owner in owners_list]
    owner_counts = pd.DataFrame(
        Counter(all_owners).items(), columns=["owners", "count"]
    )

    fig = px.pie(
        owner_counts,
        names="owners",
        values="count",
    )
    return fig.to_html(full_html=False)


@owner_route.route("/", methods=["GET"])
@requires_auth
def index():
    database_service = DatabaseService()
    repositories = database_service.find_all_repositories()
    owners = database_service.find_all_owners()
    repository_name = request.args.get("repository-name")
    selected_owner = request.args.get("owner")
    selected_access_levels = request.args.getlist("access-levels")

    filtered_repositories = []
    if selected_owner:
        for repository in repositories:
            if "NO_OWNER" in selected_owner and not repository["owners"]:
                filtered_repositories = filtered_repositories + [repository]
                continue

            selected_owners_full = []
            for owner in repository["owners"]:
                if owner["owner_name"] == selected_owner:
                    selected_owners_full += [owner]
                    for owner in selected_owners_full:
                        has_admin_access = (
                            True
                            if "ADMIN_ACCESS" in owner.get("relationship_type")
                            else False
                        )

                        if (
                            "ADMIN" in selected_access_levels
                            and has_admin_access
                            or "OTHER" in selected_access_levels
                            and not has_admin_access
                        ):
                            repositories_filtered_by_access_level = (
                                filtered_repositories + [repository]
                            )
                            filtered_repositories = filtered_repositories + [repository]
                            break
    else:
        filtered_repositories = repositories

    filtered_repositories_by_name = []
    if repository_name:
        for repository in repositories:
            if repository_name and repository_name in repository["name"]:
                filtered_repositories_by_name = filtered_repositories_by_name + [
                    repository
                ]
    else:
        filtered_repositories_by_name = filtered_repositories

    repositories_filtered_by_access_level = filtered_repositories_by_name

    return render_template(
        "pages/owner.html",
        repositories=repositories_filtered_by_access_level,
        pie_chart_of_admin_access=generate_pie_chart_of_admin_access(
            repositories_filtered_by_access_level, selected_owner
        )
        if repositories_filtered_by_access_level
        else None,
        repository_name=repository_name if repository_name else "",
        selected_owners=selected_owner if selected_owner else "NO_OWNER",
        owners=owners,
        access_levels=["ADMIN", "OTHER"],
        selected_access_levels=selected_access_levels
        if selected_access_levels
        else ["ADMIN", "OTHER"],
    )
