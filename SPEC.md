# 碳资产管理系统 V2 技术规格说明（SPEC）

## 1. 目标与范围
- 目标：基于《需求文档-任务拆解版.md》实现一个可上线的 `Vue3 + Django` 全栈项目。
- 范围：覆盖任务拆解文档中的 M1~M4，优先保障 M1 可落地可验收。
- 核心业务域：
  - 碳核算域：主数据、核算配置、数据填报、计算、报告。
  - 碳资产域：资产总览、配额管理、交易管理。
  - 分析域：能碳总览、能耗分析、用电分析、预警。

## 2. 技术栈与版本基线

### 2.1 前端技术栈
- `Vue 3.4+`
- `Vite 5+`
- `Element Plus 2+`
- `ECharts 5+`
- `Pinia 2+`
- `Vue Router 4+`
- `Axios 1+`

### 2.2 后端技术栈
- `Python 3.11+`
- `Django 4.2 LTS`
- `Django REST Framework 3.15+`
- `djangorestframework-simplejwt`（JWT）
- `MySQL 8.0+`
- `redis`（可选，缓存与异步任务状态）
- `celery`（可选，核算异步计算）

### 2.3 工程与质量工具
- 前端：`ESLint + Prettier + Vitest`
- 后端：`pytest + pytest-django + ruff/flake8`
- API 文档：`drf-spectacular` 或 `drf-yasg`
- 部署：`Nginx + Gunicorn + MySQL`

## 3. 项目结构（Monorepo）

```text
207-碳资产管理系统V2/
├─ frontend/                         # Vue3 前端项目
│  ├─ src/
│  │  ├─ api/                        # 接口定义
│  │  ├─ assets/
│  │  ├─ components/                 # 通用组件（表格/图表/筛选）
│  │  ├─ layouts/                    # 主布局、登录布局
│  │  ├─ router/                     # 动态路由与鉴权
│  │  ├─ stores/                     # Pinia 状态
│  │  ├─ utils/                      # 请求封装、权限工具
│  │  └─ views/                      # 业务页面
│  ├─ .env.development
│  └─ package.json
├─ backend/                          # Django 后端项目
│  ├─ apps/
│  │  ├─ common/                     # 通用能力（字典、日志、分页）
│  │  ├─ authn/                      # 认证鉴权
│  │  ├─ master_data/                # 燃料/用料主数据
│  │  ├─ calc_config/                # 核算配置
│  │  ├─ data_entry/                 # 数据填报
│  │  ├─ calculation/                # 核算引擎
│  │  ├─ reports/                    # 报告管理
│  │  ├─ analytics/                  # 统计分析
│  │  └─ assets/                     # 配额与交易
│  ├─ config/                        # Django settings, urls, wsgi/asgi
│  ├─ requirements.txt
│  └─ manage.py
├─ docs/
│  ├─ 需求文档.md
│  ├─ 需求文档-任务拆解版.md
│  └─ SPEC.md
└─ scripts/                          # 初始化、部署脚本
```

## 4. 架构设计

### 4.1 总体架构
- 前端：SPA 单页应用，路由按业务模块拆分。
- 后端：REST API 分层架构（View -> Service -> Repository/Model）。
- 数据层：MySQL 持久化，Redis 用于缓存和异步任务状态（可选）。
- 异步层：核算计算、报告生成可异步化（Celery + Redis/RabbitMQ）。

### 4.2 关键设计原则
- 统一返回结构、统一错误码、统一分页协议。
- 模块边界清晰：主数据、配置、填报、计算、报告、资产、分析分离。
- 口径版本化：核算因子、公式、模板支持版本追溯。
- 数据可审计：核心写操作（保存/重置/计算/删除/交易）留痕。

## 5. 环境配置规范

### 5.1 开发环境
- Node.js `>=18`
- Python `>=3.11`
- MySQL `8.0`
- Redis（可选）

### 5.2 变量约定
- 前端：`VITE_API_BASE_URL`, `VITE_APP_TITLE`
- 后端：`DJANGO_SECRET_KEY`, `DEBUG`, `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_DB`, `MYSQL_USER`, `MYSQL_PASSWORD`, `JWT_ACCESS_MINUTES`, `JWT_REFRESH_DAYS`

## 6. 后端 API 规范

### 6.1 统一响应格式
```json
{
  "code": 0,
  "message": "ok",
  "data": {},
  "request_id": "uuid"
}
```

### 6.2 分页协议
- 入参：`page`, `page_size`, `ordering`, `keyword`
- 出参：
```json
{
  "list": [],
  "total": 0,
  "page": 1,
  "page_size": 20
}
```

### 6.3 认证鉴权
- 登录：`POST /api/v1/auth/login`
- 刷新令牌：`POST /api/v1/auth/refresh`
- 当前用户：`GET /api/v1/auth/me`
- 权限模型：RBAC（用户-角色-菜单/接口）
- Header：`Authorization: Bearer <access_token>`

### 6.4 错误码建议
- `0` 成功
- `40001` 参数错误
- `40003` 未认证或 token 失效
- `40004` 无权限
- `50000` 服务器异常

## 7. 数据库模型（核心表）

### 7.1 认证与权限
- `sys_user`
- `sys_role`
- `sys_menu`
- `sys_user_role`
- `sys_role_menu`

### 7.2 主数据与配置
- `md_fuel_type`（燃料品种）
- `md_material`（生产用料）
- `calc_template`（行业模板）
- `calc_boundary_item`（核算边界项）
- `calc_factor`（排放因子与参数）
- `calc_template_version`（模板版本）

### 7.3 填报与计算
- `entry_monthly_data`（月度填报主表）
- `entry_monthly_item`（月度填报明细）
- `calc_task`（计算任务）
- `calc_result`（计算结果）
- `calc_result_detail`（计算明细）

### 7.4 报告与底单
- `report_record`（报告主表）
- `report_attachment`（报告附件）
- `report_ledger`（排放底单）

### 7.5 资产与交易
- `asset_quota_budget`（年度配额预算）
- `asset_quota_usage`（配额执行）
- `asset_trade_record`（交易记录）
- `asset_warning_record`（预警记录）

### 7.6 审计与字典
- `sys_dict_type`, `sys_dict_item`
- `sys_audit_log`

## 8. 前端页面与路由规划

### 8.1 路由分组
- `/login`
- `/dashboard/carbon-profile`（碳画像总览）
- `/calc/overview`（能碳总览）
- `/calc/entry`（数据填报）
- `/calc/config`（核算配置）
- `/calc/reports`（分析报告）
- `/calc/ledger`（排放底单）
- `/energy/fuel`（燃料品种管理）
- `/energy/material`（生产用料管理）
- `/analysis/energy`（能耗分析）
- `/analysis/power`（用电分析）
- `/asset/overview`（资产总览）
- `/asset/quota`（配额管理）
- `/asset/trade`（交易情况）

### 8.2 Pinia Store 切分
- `useAuthStore`：用户、token、权限
- `useDictStore`：字典缓存
- `useGlobalStore`：全局 loading、主题、面包屑
- 各业务模块本地 store：筛选条件、图表参数

### 8.3 图表组件规范
- 封装 `BaseChart`（统一 resize、loading、empty）
- 图表类型：趋势线、柱状对比、环图、K线
- 统一主题色与 tooltip 格式

## 9. 模块任务映射（与拆解文档对齐）

### 9.1 M1 对应实现范围
- `BASE-01 ~ BASE-05`
- `CONF-01 ~ CONF-04`
- `CALC-01 ~ CALC-04`
- 交付：登录鉴权、主数据、核算配置、填报计算、报告管理

### 9.2 M2 对应实现范围
- `ANA-01 ~ ANA-04`
- 交付：能碳总览、能耗分析、用电分析、预警中心

### 9.3 M3 对应实现范围
- `ASSET-01 ~ ASSET-03`
- 可选：`ASSET-04`
- 交付：资产总览、配额管理、交易管理

### 9.4 M4 对应实现范围
- `INT-*`, `QA-*`, `REL-01`
- 交付：性能优化、对接完善、上线发布

## 10. 安全与合规要求
- 密码加密存储（Django 内置哈希）。
- 接口级权限校验（菜单权限 + 数据权限预留）。
- 敏感操作审计日志。
- 防重放与限流（登录接口建议启用）。
- 导出接口权限与水印（可选）。

## 11. 测试策略

### 11.1 后端测试
- 单元测试：Service 层核心逻辑（计算、状态流转、权限判断）
- 接口测试：认证、列表、CRUD、导出
- 集成测试：配置->填报->计算->报告全链路

### 11.2 前端测试
- 组件测试：通用表格、筛选、图表组件
- 页面测试：关键页面渲染与交互
- E2E（可选）：登录、填报、计算、报告导出主流程

### 11.3 验收门槛
- P1/P2 缺陷为 0
- 关键 API 覆盖率 >= 80%
- 核心流程回归通过率 100%

## 12. 交付清单
- 前端工程源码（`frontend/`）
- 后端工程源码（`backend/`）
- 初始化 SQL / Django migrations
- API 文档（OpenAPI）
- 部署文档（Dev/UAT/Prod）
- 测试报告与验收报告

## 13. 开发启动步骤（建议）

### 13.1 第一步（脚手架）
1. 初始化 `frontend`（Vite + Vue3 + TS/JS）
2. 初始化 `backend`（Django + DRF + JWT）
3. 配置 MySQL 连接与基础迁移
4. 完成登录接口 + 登录页 + 权限菜单

### 13.2 第二步（M1 主链路）
1. 燃料/用料主数据 CRUD
2. 核算配置 CRUD + 版本管理
3. 数据填报 + 计算任务 + 结果展示
4. 报告列表 + 下载导出

### 13.3 第三步（分析与资产）
1. 能碳总览/能耗分析/用电分析图表化
2. 资产总览/配额管理/交易管理
3. 联调、压测、上线

## 14. 非目标（当前版本不做）
- 暂不实现复杂流程引擎（审批流）；
- 暂不实现多租户隔离（仅预留字段）；
- 暂不实现外部交易所实时双向同步（先支持内部台账）。

---
规格版本：`SPEC v1.0`  
生成日期：`2026-04-23`  
关联输入文档：`需求文档-任务拆解版.md`
