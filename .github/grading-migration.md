# 迟交计分迁移记录

- 课程：**学科综合讲座**（`intro-to-cybersecurity-tools`）
- 制度生效日期：2026-11-10
- 共享审核器：course-pr-reviewer v0.15.0（`27337bbae625c39ce40489c06bb48f13d53d16e9`）
- 成绩分支：`grades`（初始提交 `62ac04d1e26f93587f6cc478cb0884d7a14a729a`，孤儿分支，由审核器写入）
- 配置文件：`.github/course-review.yml`

## 1. 已发布作业（冻结为 legacy）

以下清单按各仓库发布历史核对，**不按 deadline 是否已经过去推测**。这些作业不实行分段迟交扣分，
内容合格即自动合并，收据里 `score_cap_percent` 与 `awarded_points` 均为 `null`。

| 作业 | 截止时间 | 模式 |
|---|---|---|
| Lab1 | 2026-10-17T00:00:00+08:00 | legacy |
| Lab2 | 2026-10-20T00:00:00+08:00 | legacy |
| Lab3 | 2026-10-24T00:00:00+08:00 | legacy |
| Lab4 | 2026-10-26T00:00:00+08:00 | legacy |
| Lab5 | 2026-10-31T00:00:00+08:00 | legacy |
| Lab6 | 2026-11-07T00:00:00+08:00 | legacy |
| Lab7 | 2026-11-14T00:00:00+08:00 | legacy |

## 2. 从 Lab8 开始启用 tiered

2026-11-13 起，**Lab8 及之后发布的作业**改用 `tiered`：迟交不再阻止合并，只按迟交时长限制成绩上限，
并写入 `grades` 分支。Lab1～Lab7 维持 `legacy`，已合并的旧 PR 不追溯改分。

| 作业 | 截止时间 | 模式 |
|---|---|---|
| Lab8 | 2026-11-21T00:00:00+08:00 | tiered |

`Lab9` 及之后的作业尚未发布，发布时按下面的写法加入配置，模式仍为 `tiered`。

新增 Lab 时照抄：

```yaml
  LabN:
    enabled: true
    deadline: "YYYY-MM-DDT00:00:00+08:00"
    grading:
      mode: tiered
      max_points: "10.00"
```

发布前先运行：

```bash
course-pr-reviewer grade validate --config .github/course-review.yml --students .github/students.yml
```

## 3. 旧 PR 如何处理

- **已合并的历史 PR**：不回填成绩，不补算分段扣分，不修改历史评论。
- **仍打开的 Lab1～Lab7 PR**：下一次推送时按新规则审核；内容合格即合并，`legacy` 作业不扣分。
- **Lab8 及之后的新 PR**：按 `tiered` 审核并记录迟交分档，不必私聊教师申请放行。
- **已关闭的旧 PR**：不自动重新打开，学生可重新提交合规 PR。
- 本迁移没有批量关闭、批量重开或批量修改任何学生 PR。

## 4. 上线顺序（必须遵守）

1. 先把 `LiuXiYing/course-pr-reviewer` 的新版本推到 `main`；
2. 再推送本仓库的配置与工作流。

若顺序反了，旧审核器读不到 `grading` 字段会判定配置无效，所有 PR 会停在 `ERROR`（不合并、不计分）。
此时把审核器版本推上去即可恢复，不需要学生重新提交。

## 5. 回滚

1. 把 `.github/workflows/` 里 `LiuXiYing/course-pr-reviewer@...` 改回上一版本 commit；
2. 从 `.github/course-review.yml` 删除 `grading` 块与 `features.grading`，恢复 `close_late_pr: true`，
   并删除每个作业的 `grading:` 块；
3. `grades` 分支保留只读即可，不影响审核；确认不再使用后再删除；
4. 已写入的 `receipts/` 不要手工修改，保留作为审计记录。

## 6. 已知限制

- 公开仓库的 `grades` 分支同样是**公开**的，其中只有学号、GitHub 账号和分数，没有姓名与申诉材料。
- 48 小时修正期依赖截止前的实质性提交快照；无法核验时按真实迟交档计分，并在评论中提示可联系教师复核。
- 教师手工改分走 `overrides/`（schema 已定，尚无表单界面），不改写原始收据。
