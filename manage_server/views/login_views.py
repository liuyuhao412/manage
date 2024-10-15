import jwt
import datetime
from flask import Blueprint, jsonify, request
from models import User, AccountStatus
from extensions import (
    db,
    send_email_verification_code,
    generate_random_verification_code,
)
from config import Config
from .utils import get_user_id_from_token
from datetime import datetime, timedelta


login_bp = Blueprint("login", __name__)


@login_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    account = data.get("account")
    password = data.get("password")
    user = User.query.filter_by(username=account).first()
    if user and user.check_password(password):
        # 检查账户状态
        if user.account_status == AccountStatus.INACTIVE:
            return jsonify({"message": "账户已禁用"}), 403

        user.last_login_ip = request.remote_addr
        user.last_login_at = datetime.utcnow() + timedelta(hours=8)
        db.session.commit()

        # 生成 token
        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.utcnow() + timedelta(hours=8) + timedelta(hours=1),
            },
            Config.SECRET_KEY,
            algorithm="HS256",
        )
        return jsonify({"message": "登录成功", "token": token}), 200
    else:
        return jsonify({"message": "账号或密码错误"}), 401


@login_bp.route("/api/send-verification-code", methods=["POST"])
def send_verification_code():
    data = request.get_json()
    email = data.get("email")

    try:
        verification_code = generate_random_verification_code()
        print(verification_code)
        # send_email_verification_code(email, verification_code)

        return (
            jsonify(
                {"message": "验证码已发送", "verification_code": verification_code}
            ),
            200,
        )
    except Exception as e:
        return jsonify({"message": "发送验证码失败", "error": str(e)}), 500


@login_bp.route("/api/check-email-registered", methods=["POST"])
def check_email_registered():
    data = request.get_json()
    email = data.get("email")

    user = User.query.filter_by(username=email).first()
    if user:
        return jsonify({"message": "邮箱已注册", "registered": True}), 200
    else:
        return jsonify({"message": "邮箱未注册", "registered": False}), 200


@login_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    new_user = User(username=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "账号注册成功"}), 201


@login_bp.route("/api/recover-account", methods=["POST"])
def recover_account():
    data = request.get_json()
    email = data.get("email")
    new_password = data.get("newPassword")

    # 验证邮箱是否存在
    user = User.query.filter_by(username=email).first()
    if not user:
        return jsonify({"message": "邮箱未注册"}), 404

    # 更新用户密码
    user.set_password(new_password)
    db.session.commit()

    return jsonify({"message": "密码已成功重置"}), 200


@login_bp.route("/api/user-role", methods=["GET"])
def get_user_role():
    token = request.headers.get("Authorization").split(" ")[1]
    user_id, error_message = get_user_id_from_token(token)
    if user_id is None:
        return jsonify({"message": error_message}), 401

    user = User.query.get(user_id)
    if user:
        return jsonify({"role": user.role.value}), 200
    else:
        return jsonify({"message": "用户不存在"}), 404


@login_bp.route("/api/current-user-name", methods=["GET"])
def get_current_user_name():
    token = request.headers.get("Authorization").split(" ")[1]
    user_id, error_message = get_user_id_from_token(token)
    if user_id is None:
        return jsonify({"message": error_message}), 401

    user = User.query.get(user_id)
    if user:
        return jsonify({"username": user.name}), 200
    else:
        return jsonify({"message": "用户不存在"}), 404
