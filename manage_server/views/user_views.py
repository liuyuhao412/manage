from flask import Blueprint, jsonify, request, send_file
from models import User, AccountStatus
from extensions import db
import openpyxl
from io import BytesIO
from config import Config
import jwt

user_bp = Blueprint("user", __name__)


@user_bp.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    total = User.query.count()
    return jsonify(
        {
            "total": total,
            "users": [user.to_dict() for user in users],
        }
    )
    
@user_bp.route("/api/users/members", methods=["GET"])
def get_members():
    members = User.query.filter(User.role == "MEMBER").all()
    total = len(members)
    return jsonify(
        {
            "total": total,
            "members": [member.to_dict() for member in members],
        }
    )



@user_bp.route("/api/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@user_bp.route("/api/users", methods=["POST"])
def create_user():
    data = request.json
    username = data.get("username")

    username, role, name, gender, birthday = (
        data.get("username"),
        data.get("role"),
        data.get("name"),
        data.get("gender"),
        data.get("birthday") if data.get("birthday") else None,
    )
    print(role)
    new_user = User(
        username=username,
        role=role,
        name=name,
        gender=gender,
        birthday=birthday,
    )
    new_user.set_password(Config.DEFAULT_PASSWORD)  # 设置默认密码
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "用户添加成功"}), 201


@user_bp.route("/api/users/<int:user_id>/info", methods=["PUT"])
def update_user_info(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

    user.username = data.get("username")
    user.role = data.get("role")

    user.name = data.get("name")
    user.gender = data.get("gender")
    user.birthday = data.get("birthday")

    db.session.commit()
    return jsonify({"message": "用户信息更新成功"})


@user_bp.route("/api/users/<int:user_id>/status", methods=["PUT"])
def update_user_status(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    account_status = data["account_status"]
    user.account_status = (
        AccountStatus.ACTIVE if account_status else AccountStatus.INACTIVE
    )
    db.session.commit()
    return jsonify(
        {
            "message": "帐号状态更新成功",
        }
    )


@user_bp.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"result": True, "message": "用户删除成功"})


@user_bp.route("/api/users/export", methods=["POST"])
def export_users():
    data = request.json
    user_ids = data.get("userIds", [])

    users = User.query.filter(User.id.in_(user_ids)).all()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "用户列表"

    headers = [
        "ID",
        "用户名",
        "姓名",
        "性别",
        "出生日期",
        "角色",
        "账户状态",
        "创建时间",
        "上次登录时间",
        "上次登录IP",
    ]
    ws.append(headers)

    for user in users:
        ws.append(
            [
                user.id,
                user.username,
                user.name,
                user.gender,
                user.birthday.strftime("%Y-%m-%d") if user.birthday else None,
                user.role.value,
                "正常" if user.account_status == AccountStatus.ACTIVE else "禁用",
                user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                (
                    user.last_login_at.strftime("%Y-%m-%d %H:%M:%S")
                    if user.last_login_at
                    else None
                ),
                user.last_login_ip,
            ]
        )

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="用户列表.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@user_bp.route("/api/protected-route", methods=["GET"])
def protected_route():
    token = request.headers.get("Authorization").split(" ")[1]  # 获取 token
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        user = User.query.get(user_id)
        if user:
            # 根据用户角色执行相应操作
            return jsonify({"role": user.role.value}), 200
        else:
            return jsonify({"message": "用户不存在"}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token 已过期"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "无效的 Token"}), 401
