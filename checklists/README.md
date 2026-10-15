# 27 个模块测试清单

本清单根据既有模块测试实践重写，用于展示测试设计范围。列出测试点不表示每项都已执行或通过；实际执行需要填写报告与证据。

每轮选择一个模块，以确认过的业务规则为预期，结合边界值、状态迁移、幂等和数据不变量进行验证。前后端同名模块观察层次不同，不应把静态检查当作真实流程验收。

| 编号 | 模块 | 主要风险 |
| --- | --- | --- |
| B01 | [工程骨架与横切](B01-foundation.md) | 统一响应、异常兜底与请求追踪 |
| B02 | [认证与权限](B02-authentication.md) | 登录态、角色与越权边界 |
| B03 | [商品与基础数据](B03-products.md) | 唯一约束、分类关系与批量导入 |
| B04 | [收银主链路结算](B04-checkout.md) | 金额、幂等与库存事务 |
| B05 | [售后与交班](B05-after-sales.md) | 退货限额与流程状态 |
| B06 | [库存查询与流水](B06-inventory-query.md) | 筛选分页、预警与导出 |
| B07 | [盘点、报损与调拨](B07-inventory-operations.md) | 库存变化的原子性 |
| B08 | [采购与收货](B08-purchasing.md) | 收货状态与移动平均成本 |
| B09 | [供应商与对账](B09-suppliers.md) | 期间口径与应付余额 |
| B10 | [会员](B10-members.md) | 充值、余额与积分流水 |
| B11 | [促销与优惠券](B11-promotions.md) | 组合条件与规则优先级 |
| B12 | [报表](B12-reports.md) | 多维统计与预聚合一致性 |
| B13 | [智能分析 BI](B13-business-intelligence.md) | 数据清洗、算法边界与异步状态 |
| B14 | [系统管理](B14-system-management.md) | 配置生效、角色与字典契约 |
| B15 | [定时任务、备份与日志](B15-scheduled-jobs.md) | 任务幂等与失败可观察性 |
| F01 | [前端工程底座与请求层](F01-frontend-foundation.md) | 拦截器、路由与重复提交 |
| F02 | [Mock 与类型契约](F02-frontend-contracts.md) | 前后端字段与模式差异 |
| F03 | [登录与布局](F03-frontend-login.md) | 登录跳转和权限展示 |
| F04 | [收银台](F04-frontend-pos.md) | 关键交互与真实结算 |
| F05 | [商品与基础数据页](F05-frontend-products.md) | 表单、导入与真实持久化 |
| F06 | [库存页](F06-frontend-inventory.md) | 页面接线与库存流程 |
| F07 | [采购与供应商页](F07-frontend-purchasing.md) | 状态操作与字段契约 |
| F08 | [会员页](F08-frontend-members.md) | 充值反馈与流水对应 |
| F09 | [促销与优惠券页](F09-frontend-promotions.md) | 复杂表单和作用范围 |
| F10 | [报表与看板页](F10-frontend-reports.md) | 展示口径与导出完整性 |
| F11 | [BI 分析页](F11-frontend-bi.md) | 异步任务与算法结果解释 |
| F12 | [系统管理页](F12-frontend-system.md) | 状态编码、配置与文件操作 |

建议先处理金额、库存、权限与事务，再完成报表/BI 和一般页面。实际顺序由基线失败、业务风险与环境决定。

共享入口：[完整方法](../docs/01-methodology.md) · [执行指南](../docs/04-execution-guide.md) · [模块报告](../templates/module-report.md)
