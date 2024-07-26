import logging
from os import name
from plotly import data
import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request
from collections import Counter

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)

repositories = [
    {
        "name": "operations-engineering",
        "owners": ["Platforms and Architecture", "HMPPS"],
    },
    {
        "name": "operations-engineering-testing",
        "owners": ["Platforms and Architecture"],
    },
    {
        "name": "hmpps-auth",
        "owners": ["HMPPS"],
    },
    {
        "name": "opg-api",
        "owners": ["OPG"],
    },
    {
        "name": "laa-infrastucture",
        "owners": ["LAA"],
    },
    {
        "name": "laa-infrastucture",
        "owners": [],
    },
]


def generate_pie_chart(repositories: list[dict]):
    dataframe = pd.DataFrame(repositories)
    # Fill empty owner lists with the default value "Unknown"
    dataframe["owners"] = dataframe["owners"].apply(
        lambda owners: owners if owners else ["No owner"]
    )
    #
    # # Flatten the list of owners and count occurrences
    all_owners = [owner for owners_list in dataframe["owners"] for owner in owners_list]
    owner_counts = pd.DataFrame(
        Counter(all_owners).items(), columns=["owners", "count"]
    )
    # dataframe["owner"] = dataframe["owner"].replace("", None)
    # dataframe["owner"] = dataframe["owner"].fillna("Unknown")

    # owner_counts = dataframe["owner"].value_counts().reset_index()
    # owner_counts.columns = ["owner", "count"]
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
    if request.method == "POST":
        search_term = request.form.get("search")
        filtered_results = [
            repository
            for repository in repositories
            if search_term.lower() in repository["name"].lower()
        ]
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
