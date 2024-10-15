from extensions import db
from datetime import datetime, timedelta
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash


class UserRoles(Enum):
    ADMIN = "管理员"
    MANAGER = "经理"
    MEMBER = "成员"
    USER = "用户"


class AccountStatus(Enum):
    ACTIVE = "正常"
    INACTIVE = "禁用"


class ProjectStatus(Enum):
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"
    ARCHIVED = "已归档"


class ProjectPriority(Enum):
    LOW = "低"
    NORMAL = "正常"
    HIGH = "高"


class TaskStatus(Enum):
    IN_PROGRESS = "进行中"
    COMPLETED = "已完成"


class User(db.Model):
    __tablename__ = "users"  # 数据库表名

    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名
    password_hash = db.Column(db.String(256))  # 密码哈希
    role = db.Column(
        db.Enum(UserRoles), nullable=False, default=UserRoles.USER
    )  # 用户角色，默认值为 '用户'
    name = db.Column(db.String(80), nullable=True)  # 用户姓名
    gender = db.Column(db.String(10), nullable=True)  # 性别
    birthday = db.Column(db.Date, nullable=True)  # 生日
    account_status = db.Column(
        db.Enum(AccountStatus), nullable=False, default=AccountStatus.ACTIVE
    )  # 账户状态
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(hours=8),
    )  # 账户创建时间（北京时间）
    last_login_at = db.Column(db.DateTime, nullable=True)  # 上次登录时间（北京时间）
    last_login_ip = db.Column(db.String(45), nullable=True)  # 上次登录IP

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # 验证密码

    def to_dict(self):
        birthday = self.birthday.strftime("%Y-%m-%d") if self.birthday else None
        role = self.role.value
        account_status = self.account_status.value == "正常"
        created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        last_login_at = (
            self.last_login_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.last_login_at
            else None
        )

        return {
            "id": self.id,
            "username": self.username,
            "role": role,
            "name": self.name,
            "gender": self.gender,
            "birthday": birthday,  # 返回格式化后的生日
            "account_status": account_status,
            "created_at": created_at,
            "last_login_at": last_login_at,
            "last_login_ip": self.last_login_ip,
        }


class Project(db.Model):
    __tablename__ = "projects"  # 数据库表名

    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(200), nullable=False)  # 项目名称
    description = db.Column(db.Text, nullable=True)  # 项目描述
    start_date = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(hours=8),
    )  # 开始时间，默认值为当前时间
    end_date = db.Column(db.DateTime, nullable=False)  # 结束时间
    status = db.Column(
        db.Enum(ProjectStatus), nullable=False, default=ProjectStatus.IN_PROGRESS
    )  # 项目状态
    priority = db.Column(
        db.Enum(ProjectPriority), nullable=True, default=ProjectPriority.NORMAL
    )
    manager_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 外键

    manager = db.relationship("User", backref="projects")  # 反向关系

    def to_dict(self):
        start_date = (
            self.start_date.strftime("%Y-%m-%d %H:%M:%S") if self.start_date else None
        )
        end_date = (
            self.end_date.strftime("%Y-%m-%d %H:%M:%S") if self.end_date else None
        )
        status = self.status.value
        priority = self.priority.value
        manager_name = (
            self.manager.name if self.manager else None
        )  # 根据 manager_id 获取 name
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": start_date,
            "end_date": end_date,
            "status": status,
            "priority": priority,
            "manager_id": self.manager_id,
            "manager_name": manager_name,
        }


class Process(db.Model):
    __tablename__ = "process"  # 数据库表名

    id = db.Column(db.Integer, primary_key=True)  # 主键
    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id"), nullable=False
    )  # 外键
    completion_rate = db.Column(
        db.Float, nullable=False, default=0.0
    )  # 完成率，默认值为 0.0
    update_time = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(hours=8),
    )  # 更新时间，默认值为当前时间

    project = db.relationship("Project", backref="progress")  # 反向关系

    def to_dict(self):
        project_name = self.project.name
        return {
            "id": self.id,
            "project_id": self.project_id,
            "project_name": project_name,
            "completion_rate": self.completion_rate * 100,
            "update_time": (
                self.update_time.strftime("%Y-%m-%d %H:%M:%S")
                if self.update_time
                else None
            ),
        }


class ArchivedProject(db.Model):
    __tablename__ = "archived_projects"  # 数据库表名

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id"), nullable=False
    )  # 外键，设置为不可为空
    archived_date = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )  # 归档时间，默认值为当前时间

    project = db.relationship(
        "Project", backref="archived_projects", lazy=True
    )  # 反向关系，添加 lazy 加载

    def to_dict(self):
        manager_name = (
            self.project.manager.name if self.project.manager else None
        )  # 根据 manager_id 获取 name
        return {
            "id": self.id,
            "project_id": self.project_id,
            "manager_name": manager_name,
            "project_name": self.project.name,
            "archived_date": (
                self.archived_date.strftime("%Y-%m-%d %H:%M:%S")
                if self.archived_date
                else None
            ),
        }


class Task(db.Model):
    __tablename__ = "tasks"  # 数据库表名

    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(200), nullable=False)  # 任务名称
    description = db.Column(db.Text, nullable=True)  # 任务描述
    due_date = db.Column(db.DateTime, nullable=False)  # 截止时间

    assignee_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 外键
    project_id = db.Column(
        db.Integer, db.ForeignKey("projects.id"), nullable=False
    )  # 外键
    status = db.Column(
        db.Enum(TaskStatus), nullable=False, default=TaskStatus.IN_PROGRESS
    )

    assignee = db.relationship("User", backref="tasks")  # 反向关系
    project = db.relationship("Project", backref="tasks", lazy=True)  # 修改反向关系名称
    attachmentUrl = db.Column(db.String(255), nullable=True)  # 附件路径

    def to_dict(self):
        due_date = (
            self.due_date.strftime("%Y-%m-%d %H:%M:%S") if self.due_date else None
        )

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "due_date": due_date,
            "assignee_id": self.assignee_id,
            "assignee_name": self.assignee.name,
            "project_id": self.project_id,
            "project_name": self.project.name,
            "project_manager_name": self.project.manager.name,
            "attachmentUrl": self.attachmentUrl,
            "status": self.status.value,
        }


class Comment(db.Model):
    __tablename__ = "comments"  # 数据库表名

    id = db.Column(db.Integer, primary_key=True)  # 评论的唯一标识符
    task_id = db.Column(
        db.Integer, db.ForeignKey("tasks.id"), nullable=False
    )  # 关联的任务ID
    author_name = db.Column(db.String(80), nullable=False)  # 评论者的名字
    content = db.Column(db.Text, nullable=False)  # 评论内容
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.utcnow() + timedelta(hours=8),
    )  # 评论创建时间

    task = db.relationship("Task", backref="task_comments")  # 反向关系

    def to_dict(self):
        created_at = (
            self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        )
        return {
            "id": self.id,
            "task_id": self.task_id,
            "author_name": self.author_name,
            "content": self.content,
            "created_at": created_at,
        }
