
from sqlalchemy import text
from app.db import SessionLocal

def list_projects():
    with SessionLocal() as s:
        rows = s.execute(text("SELECT id, name FROM projects WHERE active=1 ORDER BY name")).all()
        return [{"id": r.id, "name": r.name} for r in rows]

def list_environments():
    with SessionLocal() as s:
        rows = s.execute(text("SELECT id, name FROM environments ORDER BY name")).all()
        return [{"id": r.id, "name": r.name} for r in rows]

def deployments_by_day(project_id: int, environment_id: int, days: int = 30):
    sql = text("""
        SELECT DATE(deployed_at) AS d, COUNT(*) AS cnt
        FROM deployments
        WHERE project_id = :project_id
          AND environment_id = :environment_id
          AND deployed_at >= DATE_SUB(CURDATE(), INTERVAL :days DAY)
        GROUP BY d
        ORDER BY d ASC;
    """)
    with SessionLocal() as s:
        return s.execute(sql, {"project_id": project_id, "environment_id": environment_id, "days": days}).all()

def deployments_by_week(project_id: int, environment_id: int, weeks: int = 12):
    sql = text("""
        SELECT YEARWEEK(deployed_at, 3) AS yw, COUNT(*) AS cnt
        FROM deployments
        WHERE project_id = :project_id
          AND environment_id = :environment_id
          AND deployed_at >= DATE_SUB(CURDATE(), INTERVAL :weeks WEEK)
        GROUP BY yw
        ORDER BY yw ASC;
    """)
    with SessionLocal() as s:
        return s.execute(sql, {"project_id": project_id, "environment_id": environment_id, "weeks": weeks}).all()

def deployments_by_month(project_id: int, environment_id: int, months: int = 12):
    sql = text("""
        SELECT DATE_FORMAT(deployed_at, '%Y-%m') AS ym, COUNT(*) AS cnt
        FROM deployments
        WHERE project_id = :project_id
          AND environment_id = :environment_id
          AND deployed_at >= DATE_SUB(LAST_DAY(CURDATE()), INTERVAL :months MONTH)
        GROUP BY ym
        ORDER BY ym ASC;
    """)
    with SessionLocal() as s:
        return s.execute(sql, {"project_id": project_id, "environment_id": environment_id, "months": months}).all()

def deployments_current_week(project_id: int, environment_id: int):
    sql = text("""
        SELECT COUNT(*) AS cnt
        FROM deployments
        WHERE project_id = :project_id
          AND environment_id = :environment_id
          AND YEARWEEK(deployed_at, 3) = YEARWEEK(CURDATE(), 3)
    """)
    with SessionLocal() as s:
        return s.execute(sql, {
            "project_id": project_id,
            "environment_id": environment_id
        }).scalar() or 0

def deployments_current_month(project_id: int, environment_id: int):
    sql = text("""
        SELECT COUNT(*) AS cnt
        FROM deployments
        WHERE project_id = :project_id
          AND environment_id = :environment_id
          AND YEAR(deployed_at) = YEAR(CURDATE())
          AND MONTH(deployed_at) = MONTH(CURDATE())
    """)
    with SessionLocal() as s:
        return s.execute(sql, {
            "project_id": project_id,
            "environment_id": environment_id
        }).scalar() or 0


def deployments_current_year(project_id: int, environment_id: int):
    sql = text("""
        SELECT COUNT(*) AS cnt
        FROM deployments
        WHERE project_id = :project_id
          AND environment_id = :environment_id
          AND YEAR(deployed_at) = YEAR(CURDATE())
    """)
    with SessionLocal() as s:
        return s.execute(sql, {
            "project_id": project_id,
            "environment_id": environment_id
        }).scalar() or 0

def deployments_current_week_all():
    sql = text("""
        SELECT COUNT(*)
        FROM deployments
        WHERE YEARWEEK(deployed_at, 3) = YEARWEEK(CURDATE(), 3)
    """)
    with SessionLocal() as s:
        return s.execute(sql).scalar() or 0

def deployments_current_month_all():
    sql = text("""
        SELECT COUNT(*)
        FROM deployments
        WHERE YEAR(deployed_at) = YEAR(CURDATE())
          AND MONTH(deployed_at) = MONTH(CURDATE())
    """)
    with SessionLocal() as s:
        return s.execute(sql).scalar() or 0

def deployments_current_year_all():
    sql = text("""
        SELECT COUNT(*)
        FROM deployments
        WHERE YEAR(deployed_at) = YEAR(CURDATE())
    """)
    with SessionLocal() as s:
        return s.execute(sql).scalar() or 0
