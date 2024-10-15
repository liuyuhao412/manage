from flask import Blueprint, jsonify, request
from models import Project, User, Process, ArchivedProject, Task
from datetime import datetime, timedelta
from extensions import db
from .utils import get_user_id_from_token

project_bp = Blueprint("project", __name__)


@project_bp.route("/api/projects", methods=["GET"])
def get_projects():
    token = request.headers.get("Authorization")
    user_id = None

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    user = User.query.get(user_id)
    if user.role.value in ["管理员"]:
        projects = (
            Project.query.filter(
                Project.status != "ARCHIVED",
            ).all()
            if user_id
            else Project.query.filter(Project.status != "ARCHIVED").all()
        )
    else:
        projects = (
            Project.query.filter(
                Project.status != "ARCHIVED", Project.manager_id == user_id
            ).all()
            if user_id
            else Project.query.filter(Project.status != "ARCHIVED").all()
        )

    total = len(projects)
    return jsonify(
        {"total": total, "projects": [
            project.to_dict() for project in projects]}
    )


@project_bp.route("/api/projects/<int:project_id>", methods=["GET"])
def get_project_details(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(project.to_dict())


@project_bp.route("/api/projects", methods=["POST"])
def create_project():
    data = request.json
    token = request.headers.get("Authorization")

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    user = User.query.get(user_id)
    if not user or user.role.value not in ["经理", "管理员"]:
        return jsonify({"error": "该用户没有权限创建项目"}), 403

    new_project = Project(
        name=data["name"],
        description=data.get("description"),
        start_date=data.get("start_date"),
        end_date=data.get("end_date"),
        status=data.get("status"),
        priority=data.get("priority"),
        manager_id=user_id,
    )

    db.session.add(new_project)
    db.session.commit()

    new_process = Process(project_id=new_project.id)
    db.session.add(new_process)
    db.session.commit()

    return jsonify({"id": new_project.id, "message": "项目创建成功"}), 201


@project_bp.route("/api/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    token = request.headers.get("Authorization")

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    project = Project.query.get_or_404(project_id)
    if user_id != project.manager_id:
        return jsonify({"error": "该用户没有权限更新项目"}), 403

    data = request.json
    project.name = data.get("name", project.name)
    project.description = data.get("description", project.description)
    project.start_date = data.get("start_date", project.start_date)
    project.end_date = data.get("end_date", project.end_date)
    project.status = data.get("status", project.status)
    project.priority = data.get("priority", project.priority)

    if project.status == "ARCHIVED":
        archived_project = ArchivedProject(
            project_id=project.id, archived_date=datetime.utcnow() + timedelta(hours=8)
        )
        db.session.add(archived_project)

    try:
        db.session.commit()
        return jsonify({"id": project.id, "message": "项目更新成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "数据库错误", "message": str(e)}), 500


@project_bp.route("/api/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    token = request.headers.get("Authorization")

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    project = Project.query.get_or_404(project_id)
    if user_id != project.manager_id:
        return jsonify({"error": "该用户没有权限删除此项目"}), 403

    process = Process.query.filter_by(project_id=project.id).first()
    tasks = Task.query.filter_by(project_id=project.id).all()
    for task in tasks:
        db.session.delete(task)
    db.session.delete(process)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"result": True, "message": "项目删除成功"})


@project_bp.route("/api/processes", methods=["GET"])
def get_processes():
    token = request.headers.get("Authorization")

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    processes = Process.query.join(Project).filter(
        Project.status != "ARCHIVED")

    if user_id:
        user = User.query.get(user_id)
        if user.role.value in ["管理员"]:
            processes = processes.all()
        else:
            processes = processes.filter(Project.manager_id == user_id).all()
    else:
        processes = processes.all()

    total = len(processes)
    return jsonify(
        {"total": total, "processes": [
            process.to_dict() for process in processes]}
    )


@project_bp.route("/api/processes/<int:process_id>", methods=["GET"])
def get_process_by_id(process_id):
    process = Process.query.get_or_404(process_id)
    return jsonify(process.to_dict())


@project_bp.route("/api/processes/<int:id>", methods=["PUT"])
def update_process(id):
    token = request.headers.get("Authorization")

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    process = Process.query.get_or_404(id)
    if user_id != process.project.manager_id:
        return jsonify({"error": "该用户没有权限更新项目"}), 403

    data = request.json
    completion_rate = round(data.get("completion_rate") / 100, 2)
    process.completion_rate = completion_rate
    process.update_time = datetime.utcnow() + timedelta(hours=8)

    try:
        db.session.commit()
        return jsonify({"id": process.id, "message": "进度更新成功"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "数据库错误", "message": str(e)}), 500


@project_bp.route("/api/archived-project", methods=["GET"])
def get_archived_projects():
    token = request.headers.get("Authorization")

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401
    user = User.query.get(user_id)
    if user.role.value in ["管理员"]:
        archived_projects = (
            ArchivedProject.query.join(Project).all()
            if user_id
            else ArchivedProject.query.all()
        )
    else:
        archived_projects = (
            ArchivedProject.query.join(Project).filter(
                Project.manager_id == user_id).all()
            if user_id
            else ArchivedProject.query.all()
        )

    total = len(archived_projects)
    return jsonify(
        {
            "total": total,
            "projects": [
                archived_project.to_dict() for archived_project in archived_projects
            ],
        }
    )
