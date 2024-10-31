import logging
from app.main.middleware.auth import requires_auth
from app.main.services.database_service import DatabaseService
import plotly.express as px
import pandas as pd
from flask import Blueprint, render_template, request
from collections import Counter

logger = logging.getLogger(__name__)

main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
@requires_auth
def index():
    database_service = DatabaseService()
    owners = database_service.find_all_owners()

    return render_template("pages/home.html", owners=owners)
