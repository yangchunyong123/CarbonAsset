# 碳资产管理系统 V2 (Carbon Assets V2) - Code Wiki

## 1. 项目简介
碳资产管理系统 V2 是一个面向企业能耗与碳排放管理的系统。目标是建立“数据填报-核算计算-报告输出-资产运营”的闭环能力，实现能源与碳数据的一体化管理。该项目采用前后端分离架构，基于《需求文档》与《SPEC》实现从基础主数据、核算配置、数据填报、分析报告到碳资产与配额管理的全流程管理。

## 2. 项目整体架构
本项目采用 Monorepo（单体仓库）结构，前后端分离。
- **前端架构**：基于 `Vue 3.4+` + `Vite 5+`，UI 框架采用 `Element Plus`，状态管理使用 `Pinia`，图表展示使用 `ECharts`，请求库为 `Axios`。
- **后端架构**：基于 `Python 3.11+` 和 `Django 4.2 LTS` 构建的 REST API 服务，使用 `Django REST Framework (DRF)` 处理接口逻辑，并采用 `djangorestframework-simplejwt` 进行 JWT 认证。默认支持 `SQLite`（本地开发），生产环境支持 `MySQL 8.0+`。

### 2.1 目录结构概览
```text
/workspace/
├── backend/                  # Django 后端项目
│   ├── apps/                 # 后端业务模块（Django Apps）
│   ├── server/               # Django 项目配置与入口 (settings, urls, asgi, wsgi)
│   ├── scripts/              # 后端初始化代码生成脚本
│   ├── db.sqlite3            # 本地开发数据库
│   ├── manage.py             # Django 管理脚本
│   └── requirements.txt      # 后端依赖
├── frontend/                 # Vue3 前端项目
│   ├── public/               # 静态资源 (vite.svg 等)
│   ├── src/                  # 前端源码 (components, views, router, stores, utils)
│   ├── package.json          # 前端依赖与脚本
│   └── vite.config.js        # Vite 构建配置
├── scripts/                  # 代码生成与初始化脚本
└── SPEC.md / 需求文档.md     # 需求与技术规格文档
```

## 3. 主要模块职责

### 3.1 后端模块 (`backend/apps/`)
后端采用按业务域拆分的 Django Apps 架构，职责边界清晰：
- **`authn` (认证鉴权)**：负责用户登录、JWT 颁发、角色权限（RBAC）管理（模型：`Role`, `Menu`）。
- **`master_data` (主数据)**：负责燃料品种（`FuelType`）与生产用料（`Material`）主数据的 CRUD 维护。
- **`calc_config` (核算配置)**：负责核算行业模板（`CalcTemplate`）、边界项（`CalcBoundaryItem`）、排放因子（`CalcFactor`）的配置管理与版本控制。
- **`data_entry` (数据填报)**：负责月度数据填报主表（`EntryMonthlyData`）与明细数据（`EntryMonthlyItem`）的录入和维护。
- **`calculation` (核算引擎)**：处理核算计算任务（`CalcTask`），生成并存储计算结果（`CalcResult`）及明细。
- **`reports` (报告管理)**：负责排放报告、能耗报告的生成记录（`ReportRecord`）与附件（`ReportAttachment`）管理。
- **`analytics` (统计分析)**：负责能耗分析、用电分析、碳画像等图表数据的统计聚合。
- **`assets` (配额与交易)**：负责企业碳配额进度、交易记录的维护与管理。
- **`common` (通用模块)**：包含系统的通用分页逻辑（`pagination.py`）、统一响应封装等公共能力。

### 3.2 前端模块 (`frontend/src/`)
- **`views/`**：包含系统各业务路由页面组件，如 `DashboardView.vue` (总览), `DataEntryView.vue` (数据填报), `CalcTemplateView.vue` (核算配置), `FuelTypeView.vue` (燃料品种管理) 等。
- **`components/`**：通用业务组件与基础组件封装，如 `CrudPage.vue`（通用标准增删改查页面模板）。
- **`stores/`**：基于 Pinia 的状态管理，如 `auth.js` 负责 Token 存储、用户权限状态。
- **`router/index.js`**：管理页面路由与登录鉴权拦截，处理动态路由映射。
- **`utils/request.js`**：封装 Axios 请求，处理 JWT 请求头注入和统一的响应/错误码（401/403/500）拦截。

## 4. 关键类与函数说明

### 4.1 后端核心模型 (Models)
位于各个 `backend/apps/<app_name>/models.py` 中：
- `authn.models`：
  - `Role`, `Menu`, `UserRole`, `RoleMenu`：实现基于角色的菜单与接口权限控制。
- `master_data.models`：
  - `FuelType`：燃料品种字典表。
  - `Material`：生产用料字典表。
- `calc_config.models`：
  - `CalcTemplate`：行业核算模板定义。
  - `CalcBoundaryItem`：核算边界项（如化石燃料燃烧、购入电力）。
  - `CalcFactor`：排放因子与参数字典。
- `data_entry.models`：
  - `EntryMonthlyData`：企业每月的能源与物料消耗填报主记录。
  - `EntryMonthlyItem`：填报细项（包含各类能源消耗量等）。
- `calculation.models`：
  - `CalcTask`：异步或同步计算任务状态表。
  - `CalcResult` / `CalcResultDetail`：存储计算产出的总体排放量、能耗量结果及对应明细。
- `reports.models`：
  - `ReportRecord` / `ReportAttachment`：分析报告台账记录及关联文档附件。

### 4.2 后端核心视图 (Views & Serializers)
采用 DRF 的 `ModelViewSet` 自动提供标准 RESTful CRUD 接口：
- `LoginSerializer` (`authn`)：处理账号验证、生成 JWT Token 的序列化器。
- `EntryMonthlyDataViewSet` (`data_entry`)：提供月度填报数据的接口操作，可扩展触发对应月度的计算任务。
- `CalcTaskViewSet` (`calculation`)：管理计算任务列表、触发状态及查询接口。
- `StandardResultsSetPagination` (`common/pagination.py`)：自定义的通用分页类，规范入参 `page` 与 `page_size` 及标准返回结构。

### 4.3 前端核心逻辑
- `src/utils/request.js`：核心请求拦截器，在发送 HTTP 请求前自动注入 `Authorization: Bearer <token>`，响应拦截中对错误码如 401（Token过期）进行重定向到 `/login`。
- `src/components/CrudPage.vue`：高度抽象的列表管理页面组件，集成了头部查询表单、主体表格展示、底部分页器以及增删改查对话框等高频复用逻辑。

## 5. 依赖关系

### 5.1 前端核心依赖 (`frontend/package.json`)
- `vue` (^3.4.31)：核心视图响应式框架。
- `vue-router` (^5.0.6)：Vue 的官方路由管理。
- `pinia` (^3.0.4)：直观、类型安全的状态管理库。
- `element-plus` (^2.13.7)：基于 Vue 3，提供丰富的 UI 基础组件支持。
- `echarts` (^6.0.0)：百度开源的数据可视化图表库。
- `axios` (^1.15.2)：用于与后端 DRF 服务进行异步 HTTP 通信。

### 5.2 后端核心依赖 (`backend/requirements.txt`)
- `Django` (==4.2.16)：核心 Web 框架，提供 ORM、Admin 和基础安全组件。
- `djangorestframework` (==3.15.2)：构建强大且灵活的 Web APIs。
- `djangorestframework-simplejwt` (==5.3.1)：DRF 的 JSON Web Token 认证插件。
- `django-cors-headers` (==4.4.0)：添加跨域资源共享 (CORS) 响应头。
- `mysqlclient` (==2.2.4)：Python 连接 MySQL 数据库的高性能驱动。

## 6. 项目运行方式

### 6.1 环境准备与配置
- 前端需要 `Node.js >= 18`。
- 后端需要 `Python >= 3.11`。
- **数据库配置**：默认在本地开发环境使用 SQLite (`db.sqlite3`)，无需额外配置；如需连接 MySQL，可通过修改环境变量 `USE_SQLITE=false` 并提供 `MYSQL_HOST`, `MYSQL_DB`, `MYSQL_USER`, `MYSQL_PASSWORD` 等变量（可在 `backend/server/settings.py` 中查阅默认读取项）。

### 6.2 启动后端服务
1. 进入后端目录：
   ```bash
   cd /workspace/backend
   ```
2. 安装 Python 依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 数据库迁移（初始化数据库表结构）：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. （可选）创建超级管理员：
   ```bash
   python manage.py createsuperuser
   ```
5. 启动开发服务器：
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### 6.3 启动前端服务
1. 进入前端目录：
   ```bash
   cd /workspace/frontend
   ```
2. 安装 Node 依赖：
   ```bash
   npm install
   ```
3. 启动 Vite 开发服务器：
   ```bash
   npm run dev
   ```
4. 启动后，控制台会输出前端访问地址（默认通常为 `http://localhost:5173`），在浏览器中访问即可。前端在开发模式下会向后端的 API（`http://localhost:8000`）发起请求。
