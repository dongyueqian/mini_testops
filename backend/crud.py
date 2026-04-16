'''
负责把前端传来的数据（Schema）转换成数据库对象（Model），然后真正地存进去或取出来
'''

from sqlalchemy.orm import Session
from backend import schemas, models
from passlib.context import CryptContext

# ------------------------------
# 用例 CRUD
# ------------------------------
"""
db: Session：这是数据库连接会话。就像你去银行办事，必须先拿一个排队号（Session），办完事要把号还回去。
data: schemas.TestCaseCreate：这是前端传过来的数据，已经被 Pydantic 校验过了。
**data.dict()（核心魔法）**：data.dict()：把 Pydantic 模型转换成 Python 字典。例如 {'name': '登录', 'module': '用户'...}。
**：这是 Python 的解包语法。它把字典里的键值对拆开，变成关键字参数。
"""
def create_test_case(db: Session, data: schemas.TestCaseCreate):
    # 1. 实例化数据库对象
    db_obj = models.TestCase(**data.dict())

    # 2. 加入会话（准备阶段）
    db.add(db_obj)

    # 3. 提交事务（真正写入数据库）
    db.commit()

    # 4. 刷新对象（获取数据库生成的 ID 和时间）
    # 比如 id 和 create_time 是数据库自己生成的，刷新后，db_obj 里才会有这两个值，否则是 None。
    db.refresh(db_obj)

    # 5. 返回结果
    return db_obj


 # 1. 指定查哪张表 # 2. 加筛选条件 (WHERE id = ?)  # 3. 只拿第一条（返回模型对象或 None）
def get_test_case(db: Session, case_id: int):
    return db.query(models.TestCase).filter(models.TestCase.id == case_id).first()

# 列表查询
def list_test_cases(db: Session):
    return db.query(models.TestCase).all()   # all()，它返回的是一个列表 []，里面包含所有的用例对象。

# 删除操作，删除通常也是先查后删。如果用户传了一个不存在的 ID，我们直接返回 None，不做任何操作。
def delete_test_case(db: Session, case_id: int):
    # 1. 先查出来（找不到就删个寂寞）
    obj = get_test_case(db, case_id)
    if obj:
        # 2. 标记删除
        db.delete(obj)
        # 3. 提交
        db.commit()
    return obj

# ------------------------------
# 环境配置 CRUD
# ------------------------------
def create_env_config(db: Session, data: schemas.EnvConfigCreate):
    db_obj = models.EnvConfig(**data.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_env_config(db: Session, env_id: int):
    return db.query(models.EnvConfig).filter(models.EnvConfig.id == env_id).first()

def list_env_configs(db: Session):
    return db.query(models.EnvConfig).all()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserLogin):
    hashed_pwd = get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ================== 项目 ==================
def create_project(db: Session, data: schemas.ProjectCreate):
    item = models.Project(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_projects(db: Session):
    return db.query(models.Project).all()

def delete_project(db: Session, id: int):
    item = db.query(models.Project).filter(models.Project.id == id).first()
    if item:
        db.delete(item)
        db.commit()
    return item

# ================== 环境 ==================
def create_env_config(db: Session, data: schemas.EnvConfigCreate):
    item = models.EnvConfig(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def list_env_configs(db: Session):
    return db.query(models.EnvConfig).all()

def delete_env_config(db: Session, id: int):
    item = db.query(models.EnvConfig).filter(models.EnvConfig.id == id).first()
    if item:
        db.delete(item)
        db.commit()
    return item