import logging
from os import name
from app.main.services.database_service import DatabaseService
from plotly import data
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
def index():
    repositories = DatabaseService().find_all_repositories()
    if request.method == "POST":
        search_term = request.form.get("search")
        if search_term.lower() == "no owner":
            filtered_results = [
                repository for repository in repositories if not repository["owners"]
            ]
        else:
            filtered_results = (
                [
                    repository
                    for repository in repositories
                    if search_term in repository["owners"]
                ]
                if search_term
                else repositories
            )

        logging.info(search_term)
        logging.info(filtered_results)
        return render_template(
            "pages/home.html",
            repositories=filtered_results,
            pie_chart=generate_pie_chart(filtered_results)
            if filtered_results
            else None,
            search_term=search_term,
        )
    return render_template(
        "pages/home.html",
        repositories=repositories,
        pie_chart=generate_pie_chart(repositories) if repositories else None,
    )
