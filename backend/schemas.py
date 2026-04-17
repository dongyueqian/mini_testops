"""
API 数据模型定义
定义所有接口的请求/响应数据结构
使用 Pydantic V2 语法 (需 pydantic>=2.0.0)
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# ====================== 测试用例模型 ======================
class TestCaseBase(BaseModel):
    """测试用例基础字段"""
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="用例名称",
        examples=["登录测试"]
    )
    module: str = Field(
        ...,
        description="所属模块",
        examples=["用户认证"]
    )
    content: str = Field(
        ...,
        description="测试步骤",
        examples=["1.访问登录页\n2.输入凭证"]
    )

class TestCaseCreate(TestCaseBase):
    """创建用例请求模型"""
    pass

class TestCaseOut(TestCaseBase):
    """用例响应模型"""
    id: int = Field(..., description="用例ID", examples=[1])
    create_time: datetime = Field(..., description="创建时间", examples=["2023-01-01T00:00:00"])
    
    model_config = ConfigDict(
        from_attributes=True,  # 替代 orm_mode
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "登录测试",
                "module": "用户认证",
                "content": "测试步骤...",
                "create_time": "2023-01-01T00:00:00"
            }
        }
    )

# ====================== 用户认证模型 ======================
class UserLogin(BaseModel):
    """用户登录请求"""
    username: str = Field(..., examples=["admin"])
    password: str = Field(..., examples=["123456"])

class Token(BaseModel):
    """令牌响应"""
    token: str = Field(..., examples=["eyJhbGciOi..."])
    token_type: str = Field(default="bearer", examples=["bearer"])

# ====================== 项目管理模型 ======================
class ProjectBase(BaseModel):
    """项目基础字段"""
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="项目名称",
        examples=["API测试平台"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="项目描述",
        examples=["接口自动化测试项目"]
    )

class ProjectCreate(ProjectBase):
    """创建项目请求"""
    pass

class ProjectOut(ProjectBase):
    """项目响应模型"""
    id: int = Field(..., description="项目ID", examples=[1])
    owner: Optional[str] = Field(
        default=None,
        description="负责人",
        examples=["admin"]
    )
    create_time: datetime = Field(..., description="创建时间", examples=["2023-01-01T00:00:00"])
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "API测试平台",
                "description": "接口自动化测试项目",
                "owner": "admin",
                "create_time": "2023-01-01T00:00:00"
            }
        }
    )

# ====================== 环境管理模型 ======================
class EnvConfigBase(BaseModel):
    """环境配置基础字段"""
    env_name: str = Field(..., description="环境名称", examples=["测试环境"])
    base_url: str = Field(..., description="基础URL", examples=["http://test.example.com"])
    description: Optional[str] = Field(
        default=None,
        description="环境描述", 
        examples=["用于功能测试的环境"]
    )

class EnvConfigCreate(EnvConfigBase):
    """创建环境请求"""
    pass

class EnvConfigOut(EnvConfigBase):
    """环境配置响应模型"""
    id: int = Field(..., description="环境ID", examples=[1])
    create_time: datetime = Field(..., description="创建时间", examples=["2023-01-01T00:00:00"])
    
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "env_name": "测试环境",
                "base_url": "http://test.example.com",
                "description": "测试环境配置",
                "create_time": "2023-01-01T00:00:00"
            }
        }
    )
