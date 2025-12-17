from flask import Flask, render_template, request
from app.config import Config
from app.db import wait_for_db
from app.queries import (
    list_projects,
    list_environments,
    deployments_by_day,
    deployments_by_week,
    deployments_by_month,
    deployments_current_week,
    deployments_current_month,
    deployments_current_year,
)


def create_server() -> Flask:
    server = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    return server


server = create_server()

# Ensure DB is reachable before loading the page
wait_for_db()


@server.route("/", methods=["GET"])
def index():
    # Dropdown data
    projects = list_projects()
    environments = list_environments()

    # Read query params
    selected_project_id = request.args.get("project_id", "all")
    selected_env_id = request.args.get("environment_id", "all")

    # Convert "all" → None, else int
    if selected_project_id == "all":
        selected_project_id = None
    else:
        try:
            selected_project_id = int(selected_project_id)
        except ValueError:
            selected_project_id = None

    if selected_env_id == "all":
        selected_env_id = None
    else:
        try:
            selected_env_id = int(selected_env_id)
        except ValueError:
            selected_env_id = None

    # Summary blocks (work for ALL or filtered)
    week_total = deployments_current_week(
        selected_project_id, selected_env_id
    )
    month_total = deployments_current_month(
        selected_project_id, selected_env_id
    )
    year_total = deployments_current_year(
        selected_project_id, selected_env_id
    )

    # Charts / tables
    day_rows = deployments_by_day(
        selected_project_id, selected_env_id, days=30
    )
    week_rows = deployments_by_week(
        selected_project_id, selected_env_id, weeks=12
    )
    month_rows = deployments_by_month(
        selected_project_id, selected_env_id, months=12
    )

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
    server.run(host="0.0.0.0", port=Config.PORT)

