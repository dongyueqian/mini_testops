'''
定义API 接口收什么数据、返回什么数据
'''
from pydantic import BaseModel
from datetime import datetime

# BaseModel 是所有 Pydantic 类的父类，它能自动检查数据类型。比如，如果接口要求 id 是整数，但用户传了个字符串 "abc"，
# Pydantic 会自动拦截并报错，防止脏数据进入你的数据库

# 用例
# 基础数据，避免重复写 name, module, content，让下面的类继承它
class TestCaseBase(BaseModel):
    name: str
    module: str
    content: str

class TestCaseCreate(TestCaseBase):
    pass

class TestCaseOut(TestCaseBase):
    id: int
    create_time: datetime

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    token: str
    token_type: str = "bearer"

# 项目
class ProjectBase(BaseModel):
    name: str
    description: str = None

class ProjectCreate(ProjectBase):
    pass

class ProjectOut(ProjectBase):
    id: int
    create_time: datetime

    class Config:
        orm_mode = True

# 环境
class EnvConfigBase(BaseModel):
    env_name: str
    base_url: str
    description: str = None

class EnvConfigCreate(EnvConfigBase):
    pass

class EnvConfigOut(EnvConfigBase):
    id: int
    create_time: datetime

    class Config:
        orm_mode = True