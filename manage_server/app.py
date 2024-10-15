from flask import Flask
from flask_migrate import Migrate  # 导入 Migrate
from flask_cors import CORS  # 导入 CORS
from config import Config
from models import User, Project, Task, ArchivedProject, Process  # 导入所有模型
from extensions import db, mail  # 导入 db 实例


migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 启用 CORS
    CORS(app)

    # 初始化数据库和迁移
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # 导入视图
    from views.login_views import login_bp
    from views.user_views import user_bp  # 导入用户视图
    from views.project_views import project_bp  # 导入项目视图
    from views.task_views import task_bp  # 导入任务视图

    # 注册蓝图
    app.register_blueprint(login_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)

    return app


if __name__ == "__main__":
    app = create_app()  # 创建应用实例
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
