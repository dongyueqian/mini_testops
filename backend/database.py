from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 数据库,定义数据库的“地址”。数据库文件名叫 test_platform.db，存放在当前项目目录下。
# 如果文件不存在，SQLAlchemy 会在第一次操作时自动创建它
SQLALCHEMY_DATABASE_URL = "sqlite:///./testops.db"

# engine 是程序与数据库之间的核心连接通道。
# 这是 SQLite 特有的配置。
# SQLite 默认为了安全，只允许“创建它的那个线程”来访问它。
# 但在 Web 框架（如 FastAPI）中，会有多个请求（多个线程）同时访问数据库。
# 如果不加connect_args={"check_same_thread": False}这行代码，程序会报错。
# 加上它，就是告诉 SQLite：“别检查线程了，谁都能来访问”。
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# SessionLocal 是一个工厂，用来生产“会话”。
# 通俗理解：
# 如果说 engine 是“通往数据库的大门”，那么 Session 就是“每次办事的临时窗口”。
# 每次处理一个用户请求时，我们都会从这个工厂拿一个新的 Session 来操作数据库，用完就关掉。
# 参数：
# bind=engine：把这个会话绑定到刚才定义的 engine 上。
# autocommit=False：不要自动提交。这意味着你必须显式地调用 commit()，否则数据不会保存（这是一种保护机制，防止误操作）。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 创建一个“基类”。
# 以后你在写数据库表（比如 User 表、Question 表）时，你的类都要继承这个 Base。
# 比如：class User(Base): ...
# 它就像是一个模具，让你定义的 Python 类能被 SQLAlchemy 识别为数据库表。
Base = declarative_base()

