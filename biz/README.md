# FastAPI Business Service

基于 FastAPI 构建的现代化业务服务框架。

## 特性

- 🚀 基于 FastAPI 的高性能 Web 框架
- 📝 自动生成 API 文档（Swagger UI）
- 🔧 Pydantic 数据验证
- 🏗️ 模块化项目结构
- 🔐 JWT 认证支持
- 🌐 CORS 跨域支持
- ⚙️ 环境变量配置管理

## 项目结构

```
biz/
├── api/                    # API 路由
│   ├── endpoints/         # 各种端点
│   │   ├── health.py     # 健康检查
│   │   ├── users.py      # 用户管理
│   │   └── items.py      # 项目管理
│   └── routes.py         # 路由汇总
├── core/                  # 核心配置
│   └── config.py         # 应用配置
├── schemas/               # Pydantic 模型
│   ├── user.py           # 用户模型
│   └── item.py           # 项目模型
├── services/              # 业务逻辑层
│   ├── user_service.py   # 用户服务
│   └── item_service.py   # 项目服务
├── main.py               # 应用入口
├── requirements.txt      # 依赖包
└── .env.example         # 环境变量示例
```

## 快速开始

### 1. 安装依赖

```bash
cd biz
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，修改相应的配置
```

### 3. 启动服务

```bash
python main.py
```

或者使用 uvicorn：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问服务

- 应用首页: http://localhost:8000
- API 文档: http://localhost:8000/docs
- 备用文档: http://localhost:8000/redoc

## API 端点

### 健康检查
- `GET /api/v1/health/` - 基础健康检查
- `GET /api/v1/health/detailed` - 详细健康检查

### 用户管理
- `GET /api/v1/users/` - 获取用户列表
- `GET /api/v1/users/{user_id}` - 获取特定用户
- `POST /api/v1/users/` - 创建新用户
- `PUT /api/v1/users/{user_id}` - 更新用户
- `DELETE /api/v1/users/{user_id}` - 删除用户

### 项目管理
- `GET /api/v1/items/` - 获取项目列表
- `GET /api/v1/items/{item_id}` - 获取特定项目
- `POST /api/v1/items/` - 创建新项目
- `PUT /api/v1/items/{item_id}` - 更新项目
- `DELETE /api/v1/items/{item_id}` - 删除项目

## 开发指南

### 添加新的 API 端点

1. 在 `schemas/` 中定义数据模型
2. 在 `services/` 中实现业务逻辑
3. 在 `api/endpoints/` 中创建路由处理器
4. 在 `api/routes.py` 中注册路由

### 环境配置

所有配置都通过环境变量管理，配置项在 `core/config.py` 中定义。

## 部署

### Docker 部署

```bash
# 构建镜像
docker build -t fastapi-biz .

# 运行容器
docker run -p 8000:8000 fastapi-biz
```

### 生产环境

建议使用 Gunicorn + Uvicorn 进行生产环境部署：

```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
