# `passed`、`failed`、`skipped` 分别是什么意思

以 `skill_test/ProgramBench/src/programbench/data/tasks/agourlay__zip-password-finder.704700d` 这个任务为例，ProgramBench 里这些状态不是整道题的总结果，而是**单个测试用例**的结果。

- `passed` 表示测试通过了。
- `failed` 表示测试失败了，通常是断言不成立。
- `skipped` 表示测试被跳过了，没有实际执行。

ProgramBench 是根据 JUnit XML 来判断这些状态的：

- 如果某个 `<testcase>` 里面没有任何结果子节点，就记为 `passed`。
- 如果里面有 `<failure>`，就记为 `failed`。
- 如果里面有 `<skipped>`，就记为 `skipped`。

代码里对应的是 [`parse_test_results`]( /home/xli/github/LLM/OpenSkillsReview/skill_test/ProgramBench/src/programbench/eval/eval.py#L845 )。

这个任务的 `tests.json` 还会告诉 ProgramBench 每个分支应该有哪些测试。比如 `3001c1482b82` 这个分支在 [`tests.json`]( /home/xli/github/LLM/OpenSkillsReview/skill_test/ProgramBench/src/programbench/data/tasks/agourlay__zip-password-finder.704700d/tests.json#L1 ) 里列出了 76 个测试。

这里还有一个很重要的 ProgramBench 细节：

- 如果某个测试本来应该出现，但最后没有出现在 JUnit XML 里，ProgramBench 不会把它算成 `failed` 或 `skipped`。
- 它会把这种情况补成 `not_run`，表示“预期测试缺失，没有真正跑到”。

也就是说，在这个系统里可以这样理解：

- `passed` = 行为符合预期
- `failed` = 断言或结果不符合预期
- `skipped` = 测试主动跳过
- `not_run` = 预期里有这个测试，但实际结果文件里没有它

另外，`tests.json` 里被标记为 ignored 的测试不会参与最终评分，所以真正算分时只看未忽略的测试。

如果你愿意，我也可以把这段再整理成一版更短的中文摘要，或者画成一个“JUnit XML -> ProgramBench 状态”的对照表。
