import logging
from app.main.middleware.auth import requires_auth
from app.main.services.database_service import DatabaseService
import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request
from collections import Counter

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


def generate_pie_chart_of_admin_access(repositories: list[dict]):
    dataframe = pd.DataFrame(repositories)
    dataframe["owners"] = dataframe["owners"].apply(
        lambda owners: [
            owner["relationship_type"]
            for owner in owners
            if "relationship_type" in owner
        ]
        if owners
        else ["Other Access"]
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


def generate_pie_chart(repositories: list[dict]):
    dataframe = pd.DataFrame(repositories)
    dataframe["owners"] = dataframe["owners"].apply(
        lambda owners: [
            owner["owner_name"] for owner in owners if "owner_name" in owner
        ]
        if owners
        else ["No owner"]
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


@main.route("/", methods=["GET", "POST"])
@requires_auth
def index():
    database_service = DatabaseService()
    repositories = database_service.find_all_repositories()
    owners = database_service.find_all_owners()
    repository_name = request.args.get("repository-name")
    selected_owners = request.args.getlist("owner")
    selected_access_levels = request.args.getlist("access-levels")

    filtered_repositories_by_name = []
    if repository_name:
        for repository in repositories:
            if repository_name and repository_name in repository["name"]:
                filtered_repositories_by_name = filtered_repositories_by_name + [
                    repository
                ]
    else:
        filtered_repositories_by_name = repositories

    filtered_repositories = []
    if selected_owners:
        for repository_here in filtered_repositories_by_name:
            if "NO_OWNER" in selected_owners and not repository_here["owners"]:
                filtered_repositories = filtered_repositories + [repository_here]
            for owner in selected_owners:
                owner_names = [o["owner_name"] for o in repository_here["owners"]]
                if owner in owner_names:
                    filtered_repositories = filtered_repositories + [repository_here]
                    break
    else:
        filtered_repositories = filtered_repositories_by_name

    repositories_filtered_by_access_level = []
    if selected_access_levels:
        for repository in filtered_repositories:
            owner_relationships = [o["relationship_type"] for o in repository["owners"]]
            has_admin_access = False
            for relationship in owner_relationships:
                if "ADMIN_ACCESS" in relationship:
                    has_admin_access = True

            if (
                "ADMIN" in selected_access_levels
                and has_admin_access
                or "OTHER" in selected_access_levels
                and not has_admin_access
            ):
                repositories_filtered_by_access_level = (
                    repositories_filtered_by_access_level + [repository]
                )
    else:
        repositories_filtered_by_access_level = filtered_repositories

    return render_template(
        "pages/home.html",
        repositories=repositories_filtered_by_access_level,
        pie_chart=generate_pie_chart(repositories_filtered_by_access_level)
        if repositories_filtered_by_access_level
        else None,
        pie_chart_of_admin_access=generate_pie_chart_of_admin_access(
            repositories_filtered_by_access_level
        )
        if repositories_filtered_by_access_level
        else None,
        repository_name=repository_name if repository_name else "",
        selected_owners=selected_owners if selected_owners else owners + ["NO_OWNER"],
        owners=owners,
        access_levels=["ADMIN", "OTHER"],
        selected_access_levels=selected_access_levels
        if selected_access_levels
        else ["ADMIN", "OTHER"],
    )
