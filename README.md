# 接口自动化测试平台服务端 API 文档

## 基础信息
- **服务地址**: `http://localhost:8000`
- **接口协议**: HTTP/HTTPS
- **数据格式**: JSON
- **认证方式**: JWT (需在Header中添加 `Authorization: Bearer <token>`)

---

## 接口列表
| 分组         | 方法   | 路径               | 描述                         |
|--------------|--------|--------------------|------------------------------|
| 健康检查     | GET    | /                  | 服务状态检查                 |
| 用户认证     | POST   | /user/login        | 用户登录（获取 Token）       |
| 用户认证     | GET    | /user/info         | 获取当前用户信息             |
| 项目管理     | POST   | /project/add       | 创建新项目                   |
| 项目管理     | GET    | /project/list      | 获取项目列表                 |
| 项目管理     | POST   | /project/delete    | 删除项目                     |
| 环境管理     | POST   | /env/add           | 添加环境配置                 |
| 环境管理     | GET    | /env/list          | 获取环境列表                 |
| 环境管理     | POST   | /env/delete        | 删除环境配置                 |
| 测试用例管理 | POST   | /case/add          | 创建测试用例                 |
| 测试用例管理 | GET    | /case/list         | 获取用例列表                 |
| 开发工具     | GET    | /debug/routes      | 查看所有路由                 |
---
## 错误码说明
| 错误码   | 说明 |
|-------|-----|
| 20000 | 成功  |
| 401   | 未授权/Token无效|
| 403   | 禁止访问|
| 404   | 资源不存在 |
| 401   | 未授权/Token无效|
| 422   | 参数校验失败|
| 50000 | 业务逻辑错误 |
| 500   | 服务器内部错误 |

## 启动服务命令
python -m uvicorn backend.main:app --reload 



## 交互式文档
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
