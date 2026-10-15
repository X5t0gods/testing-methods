# 独立回归示例

这两个示例使用 Python 3.11+ 标准库和模拟输入，展示一组业务断言如何在问题实现上失败、在修复实现上通过。它们为本作品集重新编写，不使用私有业务源码或数据库。

| 示例 | 核心风险 | 断言 |
| --- | --- | --- |
| [money_regression.py](money_regression.py) | 二进制浮点与舍入规则不符合精确十进制 HALF_UP 契约 | 半分、相邻边界、负数、进位和已有分位 |
| [report_aggregation.py](report_aggregation.py) | 同日不同门店被字典赋值覆盖 | 预期汇总值、顺序无关、金额守恒与空输入 |

```powershell
python examples/money_regression.py --mode before
python examples/money_regression.py --mode after
python examples/report_aggregation.py --mode before
python examples/report_aggregation.py --mode after
```

before 模式应因业务断言失败而返回 1；after 模式应全部通过并返回 0。这是刻意保留的教学对照，不能把 before 失败视为当前修复实现失败。

金额示例有 2 个测试方法，其中一个包含 7 个 subtest；汇总示例有 4 个测试方法。这些数字与原项目的 109/772 条历史结果没有加总关系。

本次实际运行的退出码与断言结果保存在[示例验证摘要](../evidence/portfolio-validation.json)。两个 before 模式各有 3 个预期断言失败；两个 after 模式全部通过。
