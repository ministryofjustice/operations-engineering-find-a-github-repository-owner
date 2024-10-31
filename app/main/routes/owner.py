import logging
from app.main.middleware.auth import requires_auth
from app.main.services.database_service import DatabaseService
import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request, abort
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
    selected_owner = request.args.get("owner") or "NO_OWNER"
    selected_access_levels = request.args.getlist("access-levels")
    exclude_other_relationships_where_admins_exist = bool(
        request.args.get("exclude_other_relationships_where_admins_exist")
    )
    filtered_repositories = []
    for repository in repositories:
        if "NO_OWNER" in selected_owner and not repository["owners"]:
            filtered_repositories = filtered_repositories + [repository]
            continue

        owners_with_admin_access = [
            o
            for o in repository["owners"]
            if "ADMIN_ACCESS" in o.get("relationship_type")
        ]

        for owner in repository["owners"]:
            if owner["owner_name"] == selected_owner:
                has_atleast_one_admin = bool(len(owners_with_admin_access) > 0)
                has_admin_access = bool(
                    "ADMIN_ACCESS" in owner.get("relationship_type")
                )
                has_other_access = bool("OTHER" in owner.get("relationship_type"))

                include_admin_access = bool(
                    "ADMIN" in selected_access_levels and has_admin_access
                )
                include_other_access = bool(
                    "OTHER" in selected_access_levels
                    and has_other_access
                    and not (
                        exclude_other_relationships_where_admins_exist
                        and has_atleast_one_admin
                    )
                )

                if include_admin_access or include_other_access:
                    filtered_repositories += [repository]

    filtered_repositories_by_name = []
    if repository_name:
        for repository in filtered_repositories:
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
        selected_owners=selected_owner,
        owners=owners,
        access_levels=["ADMIN", "OTHER"],
        selected_access_levels=selected_access_levels
        if selected_access_levels
        else ["ADMIN", "OTHER"],
        exclude_other_relationships_where_admins_exist=exclude_other_relationships_where_admins_exist,
    )


@owner_route.route("/<owner>", methods=["GET"])
@requires_auth
def owner_dashboard(owner: str):
    database_service = DatabaseService()
    repositories = database_service.find_all_repositories()
    owners = database_service.find_all_owners()

    if owner not in owners:
        abort(404)

    repositories_with_admin_access = []
    filtered_repositories_by_owner = []
    for repository in repositories:
        for repository_owner in repository["owners"]:
            if repository_owner["owner_name"] == owner:
                filtered_repositories_by_owner += [repository]

                if "ADMIN_ACCESS" in repository_owner.get("relationship_type"):
                    repositories_with_admin_access += [repository]

    return render_template(
        "pages/owner_dashboard.html",
        owner=owner,
        filtered_repositories_by_owner=filtered_repositories_by_owner,
        all_repositories=repositories,
        repositories_with_admin_access=repositories_with_admin_access,
    )
