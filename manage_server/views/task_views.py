from flask import Blueprint, jsonify, request, send_file
from models import Task, User, Project, Comment
from extensions import db
from .utils import get_user_id_from_token
import os

task_bp = Blueprint("task", __name__)


@task_bp.route("/api/tasks", methods=["GET"])
def get_tasks():
    token = request.headers.get("Authorization")
    user_id = None

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    user = User.query.get(user_id)
    if user.role.value in ["管理员"]:
        tasks = (
            Task.query.join(Project)
            .filter(
                (Project.status != "ARCHIVED")
                if user_id
                else True
            )
            .all()
        )
    else:
        tasks = (
            Task.query.join(Project)
            .filter(
                (Project.status != "ARCHIVED") & (
                    Project.manager_id == user_id)
                if user_id
                else True
            )
            .all()
        )
    total = len(tasks)
    return jsonify({"total": total, "tasks": [task.to_dict() for task in tasks]})


@task_bp.route("/api/tasks/member", methods=["GET"])
def get_member_tasks():
    token = request.headers.get("Authorization")
    user_id = None

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    tasks = Task.query.filter_by(assignee_id=user_id).all()
    total = len(tasks)
    return jsonify({"total": total, "tasks": [task.to_dict() for task in tasks]})


@task_bp.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task_by_id(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())


@task_bp.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")
    assignee_id = data.get("assignee_id")
    project_id = data.get("project_id")
    status = data.get("status")
    token = request.headers.get("Authorization")
    try:
        token = token.split(" ")[1]
        user_id, error_message = get_user_id_from_token(token)
    except Exception as e:
        user_id = None
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    user = User.query.get(user_id)
    print(user.role.value)
    if not user or user.role.value not in ["经理", "管理员", "成员"]:
        return jsonify({"error": "该用户没有权限创建项目"}), 403

    new_task = Task(
        title=title,
        description=description,
        due_date=due_date,
        assignee_id=assignee_id,
        project_id=project_id,
        status=status,
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"id": new_task.id, "message": "任务创建成功"}), 201


@task_bp.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    due_date = data.get("due_date")
    project_id = data.get("project_id")
    status = data.get("status")
    token = request.headers.get("Authorization")

    try:
        token = token.split(" ")[1]
        user_id, error_message = get_user_id_from_token(token)
    except Exception as e:
        user_id = None
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    task = Task.query.get_or_404(task_id)
    if user_id != task.project.manager_id:
        return jsonify({"error": "该用户没有权限更新此任务"}), 403

    task.title = title
    task.description = description
    task.due_date = due_date
    task.project_id = project_id
    task.status = status

    db.session.commit()

    return jsonify({"message": "任务更新成功"}), 200


@task_bp.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    token = request.headers.get("Authorization")
    try:
        token = token.split(" ")[1]
        user_id, error_message = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    task = Task.query.get_or_404(task_id)
    if user_id != task.assignee_id:
        return jsonify({"error": "该用户没有权限删除此任务"}), 403

    db.session.delete(task)
    db.session.commit()

    return jsonify({"result": True, "message": "任务删除成功"}), 200


@task_bp.route("/api/upload", methods=["POST"])
def upload_file():
    try:
        file = request.files["file"]
        task_id = request.form.get("task_id")

        upload_dir = "static/uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_path = os.path.join(upload_dir, file.filename).replace("\\", "/")
        file.save(file_path)

        task = Task.query.get_or_404(task_id)
        task.attachmentUrl = file_path
        db.session.commit()

        return jsonify({"message": "文件上传成功", "file_path": file_path}), 201

    except Exception as e:
        return jsonify({"error": "文件上传失败", "message": str(e)}), 500


@task_bp.route("/api/download/<path:filename>", methods=["GET"])
def download_file(filename):
    token = request.headers.get("Authorization")
    user_id = None

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    # 在这里进行权限检查，例如检查用户角色
    user = User.query.get(user_id)
    if not user or user.role.value not in [
        "管理员",
        "经理",
        "成员",
    ]:
        return jsonify({"error": "没有权限访问该文件"}), 403

    file_path = filename
    if os.path.exists(file_path):
        return send_file(file_path)
    else:
        return jsonify({"error": "文件不存在"}), 404


@task_bp.route("/api/tasks/<int:id>/status", methods=["PUT"])
def update_task_status(id):
    data = request.get_json()
    status = data.get("status")

    if not status:
        return jsonify({"error": "状态不能为空"}), 400

    task = Task.query.get_or_404(id)
    task.status = status
    db.session.commit()

    return (
        jsonify({"message": "任务状态更新成功", "task_id": id, "status": status}),
        200,
    )


@task_bp.route("/api/tasks/<int:id>/comments", methods=["GET"])
def get_task_comments(id):
    task = Task.query.get_or_404(id)
    comments = task.task_comments
    return jsonify(
        {
            "message": "获取评论信息成功",
            "comments": [comment.to_dict() for comment in comments],
        }
    )


@task_bp.route("/api/tasks/<int:id>/comments", methods=["POST"])
def submit_task_comment(id):
    data = request.get_json()
    content = data.get("content")
    token = request.headers.get("Authorization")
    user_id = None

    try:
        token = token.split(" ")[1]
        user_id, _ = get_user_id_from_token(token)
    except Exception as e:
        return jsonify({"error": "解析授权令牌失败", "message": str(e)}), 401

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404

    task = Task.query.get_or_404(id)
    comment = Comment(task_id=task.id, content=content, author_name=user.name)
    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "评论提交成功", "comment": comment.to_dict()}), 201
