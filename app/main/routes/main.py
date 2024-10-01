import logging
from app.main.middleware.auth import requires_auth
from app.main.services.database_service import DatabaseService
import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request
from collections import Counter

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


def generate_pie_chart(repositories: list[dict]):
    dataframe = pd.DataFrame(repositories)
    dataframe["owners"] = dataframe["owners"].apply(
        lambda owners: owners if owners else ["No owner"]
    )
    all_owners = [owner for owners_list in dataframe["owners"] for owner in owners_list]
    owner_counts = pd.DataFrame(
        Counter(all_owners).items(), columns=["owners", "count"]
    )

    logging.info(f"""
        {dataframe}
    """)
    fig = px.pie(
        owner_counts,
        names="owners",
        values="count",
    )
    return fig.to_html(full_html=False)


@main.route("/", methods=["GET", "POST"])
@requires_auth
def index():
    repositories = DatabaseService().find_all_repositories()
    repository_name = request.args.get("repository-name")
    owners = request.args.getlist("owner")

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
    if repository_name or owners:
        for repository in filtered_repositories_by_name:
            logging.info(f"Repo Name: {repository["name"]}")
            logging.info(f"Repo Owners: {repository["owners"]}")
            if "NO_OWNER" in owners and not repository["owners"]:
                filtered_repositories = filtered_repositories + [repository]
            for owner in owners:
                if owner in repository["owners"]:
                    filtered_repositories = filtered_repositories + [repository]
    else:
        filtered_repositories = filtered_repositories_by_name

    logging.info(repositories)
    logging.info(repository_name)
    logging.info(owners)
    logging.info(filtered_repositories)
    return render_template(
        "pages/home.html",
        repositories=filtered_repositories,
        pie_chart=generate_pie_chart(filtered_repositories)
        if filtered_repositories
        else None,
        repository_name=repository_name if repository_name else "",
        owners=owners,
    )
