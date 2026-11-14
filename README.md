# 学科综合讲座 成绩记录分支

本分支由 [course-pr-reviewer](https://github.com/LiuXiYing/course-pr-reviewer)
自动写入，保存可信的验收与计分事实。

- `metadata.json`：课程标识与 schema 版本。
- `claims/`：截止前有效提交的快照，用于 48 小时修正期判定。
- `receipts/`：每个学生每次作业的最终验收与得分事实。
- `overrides/`：教师审批的例外记录，不改写原始收据。
- `reports/`：由收据重新生成的汇总表，可随时删除重建。
- `audit/`：覆盖与更正操作日志。

请勿手工修改 `receipts/` 与 `claims/`；需要改分时由教师工作流写入 `overrides/`。
本分支在公开仓库中同样是公开的，不记录姓名、联系方式或申诉材料。
