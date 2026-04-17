'''
 FastAPI 的入口文件
 它把前面写的所有零件（数据库、模型、校验器、业务逻辑）全部组装在了一起。
 只要运行这个文件，后端服务就正式启动了。
'''

from fastapi import FastAPI, Depends, HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session
from backend import models, schemas, crud, security
from backend.database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body  # 新增导入
from pydantic import BaseModel

"""
创建表，每次启动服务时，它都会检查数据库。
如果在 models.py 里加了新表，重启服务后，SQLite 里会自动把表建好。不需要手动去写 SQL 建表语句
"""
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="接口自动化测试平台", version="1.0")

# 开启跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库依赖，这是一个生成器函数，专门用来管理数据库连接。
def get_db():
    db = SessionLocal()
    try:
        """
        把数据库连接“借”给下面的接口函数用。
        下面的接口函数通过 Depends(get_db) 来“借”这个连接。
        """
        yield db
    finally:
        # 不管接口是成功还是报错，必须把数据库连接关掉。这就像借了图书馆的书，看完必须还，否则连接数满了，程序就崩了
        db.close()

"""
健康检查
当访问 http://127.0.0.1:8000/ 时，返回一个简单的 JSON。用来确认服务是不是活着。
tags：这是给自动生成的 API 文档（Swagger UI）分类用的，方便管理。
"""
@app.get("/", tags=["健康检查"])
def index():
    return {"code": 20000, "msg": "FastAPI 启动成功！"}


"""
用例接口：定义这是一个 POST 请求，路径是 /case/add
response_model=schemas.TestCaseOut：自动序列化
虽然 crud 返回的是数据库模型对象（models.TestCase），
但 FastAPI 会自动把它转换成 Pydantic 模型（schemas.TestCaseOut），
然后变成 JSON 返回给前端。
这样前端就看不到数据库里的敏感字段（如果你不想让它看的话）。
"""
@app.post("/case/add", response_model=schemas.TestCaseOut)
def add_case(data: schemas.TestCaseCreate, db: Session = Depends(get_db)):
    """
    data: schemas.TestCaseCreate：FastAPI 会自动读取请求体里的 JSON，
    校验它是否符合 TestCaseCreate 的格式。如果不符合（比如少了个字段），直接自动报错 422。
    db: Session = Depends(get_db)：调用刚才写的 get_db 函数，拿到数据库连接。
    """
    return crud.create_test_case(db, data)

"""
这是一个 GET 请求。直接调用 CRUD 里的查询函数，把结果返回。
FastAPI 会自动把数据库对象列表转换成 JSON 列表。
"""
@app.get("/case/list")
def list_cases(db: Session = Depends(get_db)):
    return crud.list_test_cases(db)

# 定义接收 JSON 的模型
class LoginForm(BaseModel):
    username: str
    password: str

# 登录（真实JWT）
@app.post("/user/login")
def login(user: schemas.UserLogin):
    # 固定账号密码，直接登录成功，不用查数据库
    if user.username == "admin" and user.password == "123456":
        token = security.create_access_token(data={"sub": "admin"})
        return {"code": 20000, "data": {"token": token}}

    return {"code": 50000, "message": "账号或密码错误"}

# 获取用户信息
@app.get("/user/info")
def user_info(token: str):
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail="无效token")

    return {
        "code": 20000,
        "data": {
            "roles": ["admin"],
            "name": "admin",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif"
        }
    }

# ====================== 项目接口 ======================
@app.post("/project/add", response_model=schemas.ProjectOut)
def add_project(data: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, data)

@app.get("/project/list", response_model=list[schemas.ProjectOut])
def list_project(db: Session = Depends(get_db)):
    return crud.list_projects(db)

@app.post("/project/delete")
def delete_project(id: int = Body(..., embed=True), db: Session = Depends(get_db)):
    crud.delete_project(db, id)
    return {"code": 20000, "msg": "删除成功"}

# ====================== 环境接口 ======================
@app.post("/env/add", response_model=schemas.EnvConfigOut)
def add_env(data: schemas.EnvConfigCreate, db: Session = Depends(get_db)):
    return crud.create_env_config(db, data)

@app.get("/env/list", response_model=list[schemas.EnvConfigOut])
def list_env(db: Session = Depends(get_db)):
    return crud.list_env_configs(db)

@app.post("/env/delete")
def delete_env(id: int = Body(..., embed=True), db: Session = Depends(get_db)):
    crud.delete_env_config(db, id)
    return {"code": 20000, "msg": "删除成功"}


# 添加路由检测端点
@app.get("/debug/routes")
async def debug_routes():
    return {
        "routes": [
            {
                "path": route.path,
                "name": route.name,
                "methods": list(route.methods)
            }
            for route in app.routes
        ]
    }
