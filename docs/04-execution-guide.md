# 执行指南与证据留存

本仓库的独立示例可以直接运行。下面的业务项目命令用于说明执行方式，需要另行取得项目源码、安装匹配依赖并准备独立测试环境；它们不是本仓库自带的可运行服务。

## 1. 明确三个目录

`testing-methods` 是本文档仓库；业务后端与业务前端是另外的代码目录。文档校验在本仓库根目录运行，pytest 在后端目录运行，npm 命令在前端目录运行。路径由使用者配置，不在文档中记录个人电脑目录。

## 2. 先检查环境与夹具

确认项目版本、连接目标与测试库隔离方式。现有项目测试夹具采用独占临时 MySQL 库，测试初始化会执行建表与种子导入，因此运行测试可能需要创建测试库的权限。数据库不可用与没有建库权限是不同故障，应分别记录。

服务级事务测试应检查内部 commit、独立会话、后台任务与浏览器写操作是否都处于测试环境中。单个 fixture 的 rollback 不能自动撤销另一个连接已提交的变化。

## 3. 捕获原始退出码

以下为 PowerShell 示例。在当前业务仓库中新建专用证据目录，并立即保存被测命令的退出码；不要用后续过滤命令的结果覆盖它。

```powershell
New-Item -ItemType Directory -Path artifacts -Force | Out-Null
& .\.venv\Scripts\python.exe -m pytest -q --timeout=120 *> artifacts\pytest.txt
$testExitCode = $LASTEXITCODE
Get-Content -LiteralPath artifacts\pytest.txt -Tail 15
Write-Output "pytest_exit_code=$testExitCode"
```

原始输出保存在本地。公开报告只提取必要统计与经过检查的片段，不直接上传完整日志。

## 4. 后端验证层次

| 命令示例 | 用途与说明 |
| --- | --- |
| `python -m pytest tests/test_services/test_money.py -q` | 金额逻辑子集；文件名需与项目当前版本一致 |
| `python -m pytest tests/test_report_logic.py tests/test_report_integration.py -q` | 报表逻辑与集成子集；有数据库前置 |
| `python -m pytest -q --timeout=120` | 全量结果；记录 passed/failed/error/skipped 与 warning |
| `python -m pytest -q --cov=app --cov-branch --cov-report=json:artifacts/coverage.json --cov-report=term-missing` | 采集行与分支覆盖率；记录采集对象与实际执行范围 |
| `python -m ruff check app scripts` | 静态检查；lint 与 formatter 检查是不同结果 |

接口测试同时检查真实 HTTP 状态、业务 code、返回字段及数据库副作用。项目将业务错误、未登录和无权限分开约定；这是项目契约，不应推广为所有 API 的通用规则。

## 5. 前端验证层次

在所检查的前端 package.json 中存在 `type-check`、`check:api`、`check:components`、`check:multroot`、`check:modules`、`check:runtime` 与 `test:pos` 脚本；没有配置 Vitest/Jest。以当前版本配置为准。

| 命令示例 | 验证目标 | 主要限制 |
| --- | --- | --- |
| `npm run type-check` | TypeScript 类型与 Vue 类型检查 | 不是业务逻辑或浏览器流程测试 |
| `npm run check:api` | 项目自检脚本中的接口/Mock 映射缺口 | 不能证明真实后端行为符合契约 |
| `npm run check:components` | 组件使用检查 | 检查范围由脚本决定 |
| `npm run check:runtime` | 浏览器逐路由的异常与日志 | 需要匹配浏览器、服务、登录态与数据 |
| `npm run test:pos` | 项目收银脚本定义的流程 | 要记录真实接口/Mock 模式，可能产生业务写入 |
| `npm run build` | 构建可用性 | 不等于部署或验收通过 |

对于收银、采购、会员充值等流程，应另外观察请求内容、重复点击、失败反馈、刷新后的持久化结果，以及权限切换。自动化截图和控制台信息可以辅助证据，不代替业务断言。

## 6. 非零、可手算的数据

报表与 BI 应先准备专属模拟数据，覆盖正向交易、退货、作废、跨日期与跨门店等情况。保存固定随机种子和业务标记，同时保留一个人工可核对的小样本。

清理按本轮创建的标记与依赖顺序进行。记录清理前后数量及业务不变量，避免对共享库执行清空或删除。造数命令的具体参数以当前脚本帮助为准，不在方法库中放可直接操作未知数据库的脚本。

## 7. 性能实验记录

每组实验记录源码版本、硬件、数据库参数、服务进程数、客户端并发、数据分布、预热方式、样本数、失败分布和 P50/P95/P99。发生超时或业务失败时，不应只计算成功样本后宣称整体达标。

算法对比固定事务数据与参数，记录数据指纹和计时边界。进程 RSS 采样会受同进程其他工作影响，采样峰值可能遗漏短暂分配；若需要算法独占内存，需设计独立进程实验。

## 8. 本仓库发布校验

运行 `python tools/verify_docs.py`，再运行两个示例的 before/after 模式。before 应失败且由预期断言触发，after 应通过。校验器验证链接、结构与证据摘要一致性，不替代对公开内容的人工隐私审查，也不重新验证私有项目历史指标。
