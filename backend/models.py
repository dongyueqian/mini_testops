'''
定义数据库表结构
'''

from sqlalchemy import Column, Integer, String, Text, DateTime, Float,Boolean
from datetime import datetime
from backend.database import Base


# 1. 用例表
# class TestCase(Base)：定义了一个 Python 类 TestCase，它继承了 Base。以后你在代码里操作 TestCase，就是在操作数据库里的这张表。
# __tablename__ = "test_cases"：这行代码告诉 SQLAlchemy：“请在数据库里创建一个名字叫 test_cases 的表”。
class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), comment="用例名称")
    module = Column(String(64), comment="模块")
    content = Column(Text, comment="用例内容")
    create_time = Column(DateTime, default=datetime.now)

# 2. 任务执行记录表
class TaskRecord(Base):
    __tablename__ = "task_records"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String(64), comment="任务ID")
    status = Column(String(16), default="running", comment="状态")
    total = Column(Integer, default=0)
    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    duration = Column(Float, default=0.0)
    create_time = Column(DateTime, default=datetime.now)

# 3. 环境配置表
class EnvConfig(Base):
    __tablename__ = "env_configs"

    id = Column(Integer, primary_key=True, index=True)
    env_name = Column(String(32), comment="环境名称：test/pre/prod")
    base_url = Column(String(255), comment="域名")
    description = Column(Text, nullable=True)

# ==============================================
# 4. 用户表（只新增了这个，其他完全不动）
# ==============================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(64), unique=True, index=True, nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码（加密存储）")
    role = Column(String(32), default="test", comment="角色：admin/test")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")

# 5. 项目表
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, comment="项目名称")
    description = Column(Text, nullable=True, comment="项目描述")
    owner = Column(String(64), nullable=True, comment="项目负责人")  # ← 新增字段
    create_time = Column(DateTime, default=datetime.now)

