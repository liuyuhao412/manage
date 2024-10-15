from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from config import Config
import random
import traceback
import threading
from flask import current_app

db = SQLAlchemy()
mail = Mail()

def send_email_verification_code(email, verification_code):
    def send_email(app):
        with app.app_context():  # 推送应用上下文
            try:
                msg = Message(
                    "您的验证码", sender=Config.MAIL_DEFAULT_SENDER, recipients=[email]
                )
                msg.body = (
                    f"[管理助手] 您的验证码是：{verification_code}。请在10分钟内使用。"
                )
                mail.send(msg)
            except Exception as e:
                print(f"发送邮件时出错: {e}")  # 打印错误信息
                traceback.print_exc()  # 打印详细的错误堆栈信息

    # 创建并启动线程，传递 Flask 应用实例
    email_thread = threading.Thread(target=send_email, args=(current_app._get_current_object(),))
    email_thread.start()

def generate_random_verification_code(length=6):
    return "".join(random.choices("0123456789", k=length))
