from sqlalchemy import text
from app.db import SessionLocal


# -----------------------------
# Dropdown data
# -----------------------------

def list_projects():
    with SessionLocal() as s:
        rows = s.execute(
            text("SELECT id, name FROM projects WHERE active = 1 ORDER BY name")
        ).all()
        return [{"id": r.id, "name": r.name} for r in rows]


def list_environments():
    with SessionLocal() as s:
        rows = s.execute(
            text("SELECT id, name FROM environments ORDER BY name")
        ).all()
        return [{"id": r.id, "name": r.name} for r in rows]


# -----------------------------
# Charts (filtered by project & env)
# -----------------------------

def deployments_by_day(project_id, environment_id, days=30):
    sql = """
        SELECT DATE(deployed_at) AS d, COUNT(*) AS cnt
        FROM deployments
        WHERE deployed_at >= DATE_SUB(CURDATE(), INTERVAL :days DAY)
    """
    params = {"days": days}

    if project_id:
        sql += " AND project_id = :project_id"
        params["project_id"] = project_id

    if environment_id:
        sql += " AND environment_id = :environment_id"
        params["environment_id"] = environment_id

    sql += " GROUP BY d ORDER BY d ASC"

    with SessionLocal() as s:
        return s.execute(text(sql), params).all()


def deployments_by_week(project_id, environment_id, weeks=12):
    sql = """
        SELECT YEARWEEK(deployed_at, 3) AS yw, COUNT(*) AS cnt
        FROM deployments
        WHERE deployed_at >= DATE_SUB(CURDATE(), INTERVAL :weeks WEEK)
    """
    params = {"weeks": weeks}

    if project_id:
        sql += " AND project_id = :project_id"
        params["project_id"] = project_id

    if environment_id:
        sql += " AND environment_id = :environment_id"
        params["environment_id"] = environment_id

    sql += " GROUP BY yw ORDER BY yw ASC"

    with SessionLocal() as s:
        return s.execute(text(sql), params).all()


def deployments_by_month(project_id, environment_id, months=12):
    sql = """
        SELECT DATE_FORMAT(deployed_at, '%Y-%m') AS ym, COUNT(*) AS cnt
        FROM deployments
        WHERE deployed_at >= DATE_SUB(LAST_DAY(CURDATE()), INTERVAL :months MONTH)
    """
    params = {"months": months}

    if project_id:
        sql += " AND project_id = :project_id"
        params["project_id"] = project_id

    if environment_id:
        sql += " AND environment_id = :environment_id"
        params["environment_id"] = environment_id

    sql += " GROUP BY ym ORDER BY ym ASC"

    with SessionLocal() as s:
        return s.execute(text(sql), params).all()


# -----------------------------
# Summary boxes (Week / Month / Year)
# Works for:
# - All projects + all envs
# - Specific project + env
# -----------------------------

def deployments_current_week(project_id=None, environment_id=None):
    sql = """
        SELECT COUNT(*) AS cnt
        FROM deployments
        WHERE YEARWEEK(deployed_at, 3) = YEARWEEK(CURDATE(), 3)
    """
    params = {}

    if project_id:
        sql += " AND project_id = :project_id"
        params["project_id"] = project_id

    if environment_id:
        sql += " AND environment_id = :environment_id"
        params["environment_id"] = environment_id

    with SessionLocal() as s:
        return s.execute(text(sql), params).scalar() or 0


def deployments_current_month(project_id=None, environment_id=None):
    sql = """
        SELECT COUNT(*) AS cnt
        FROM deployments
        WHERE YEAR(deployed_at) = YEAR(CURDATE())
          AND MONTH(deployed_at) = MONTH(CURDATE())
    """
    params = {}

    if project_id:
        sql += " AND project_id = :project_id"
        params["project_id"] = project_id

    if environment_id:
        sql += " AND environment_id = :environment_id"
        params["environment_id"] = environment_id

    with SessionLocal() as s:
        return s.execute(text(sql), params).scalar() or 0


def deployments_current_year(project_id=None, environment_id=None):
    sql = """
        SELECT COUNT(*) AS cnt
        FROM deployments
        WHERE YEAR(deployed_at) = YEAR(CURDATE())
    """
    params = {}

    if project_id:
        sql += " AND project_id = :project_id"
        params["project_id"] = project_id

    if environment_id:
        sql += " AND environment_id = :environment_id"
        params["environment_id"] = environment_id

    with SessionLocal() as s:
        return s.execute(text(sql), params).scalar() or 0

