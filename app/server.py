import os
from flask import Flask, render_template, request
from app.config import Config
from app.db import wait_for_db
from app.queries import (
    list_projects, list_environments,
    deployments_by_day, deployments_by_week, deployments_by_month, deployments_current_week,
    deployments_current_month,
    deployments_current_year
)

def create_server() -> Flask:
    # templates and static directories are under app/
    server = Flask(__name__, template_folder="templates", static_folder="static")
    return server

server = create_server()

# Ensure DB is reachable before loading the page
wait_for_db()

@server.route("/", methods=["GET"])
def index():
    projects = list_projects()
    environments = list_environments()

    selected_project_id = request.args.get("project_id", default=str(projects[0]["id"]) if projects else None)
    selected_env_id = request.args.get("environment_id", default=str(environments[0]["id"]) if environments else None)

    try:
        selected_project_id = int(selected_project_id) if selected_project_id is not None else None
        selected_env_id = int(selected_env_id) if selected_env_id is not None else None
    except ValueError:
        selected_project_id, selected_env_id = None, None

    day_rows, week_rows, month_rows = [], [], []
    week_total = month_total = year_total = 0
    if selected_project_id and selected_env_id:
        day_rows   = deployments_by_day(selected_project_id, selected_env_id, days=30)
        week_rows  = deployments_by_week(selected_project_id, selected_env_id, weeks=12)
        month_rows = deployments_by_month(selected_project_id, selected_env_id, months=12)
        week_total  = deployments_current_week(selected_project_id, selected_env_id)
        month_total = deployments_current_month(selected_project_id, selected_env_id)
        year_total  = deployments_current_year(selected_project_id, selected_env_id)

    return render_template(
        "index.html",
        projects=projects,
        environments=environments,
        selected_project_id=selected_project_id,
        selected_env_id=selected_env_id,
        day_rows=day_rows,
        week_rows=week_rows,
        month_rows=month_rows,
        week_total=week_total,
        month_total=month_total,
        year_total=year_total,
    )

if __name__ == "__main__":
    # Port is controlled via env; default to 90
    server.run(host="0.0.0.0", port=Config.PORT)
