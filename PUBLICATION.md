# 发布与版本管理

当前版本：0.1.0，采用 [MIT 许可证](LICENSE)。

## 项目形态

GitHub 仓库：[Guokai-Liu/paper-reading-lite](https://github.com/Guokai-Liu/paper-reading-lite)。根目录本身就是一个 skill，同时包含提示词、模板、技术核查表和离线 HTML 渲染工具。读者既可以按普通项目入口使用，也可以把完整目录放入自己代理支持的技能目录。

首版定位为试用版本：方法来自真实使用及一篇明确好评的案例，但没有跨领域、跨模型或多人对照验证。它帮助助手执行和呈现阅读，不是脱离助手独立运行的自动论文分析服务。

## 发布包内容

使用 scripts/build_release.py 按明确清单导出 ZIP。包内包括说明、skill 入口、工作流、模板、渲染工具、KaTeX 及其原许可证。不会自动扫描或打包工作区的阅读库。

现有论文 PDF、出版社原图、完整私人阅读报告、聊天、绝对路径、Zotero 数据、账号配置和本地验证记录不作为首版发布内容。公开示例可后续选择适合分享的材料制作，并单独确认来源与展示范围。

## 版本与许可

- 仓库维护者：Guokai-Liu。
- 本项目原创提示词、文档与脚本采用 MIT 许可；第三方 KaTeX 的原有许可独立保留。
- 版本号以 VERSION 为准；发布包附逐文件 SHA256 清单。
- 首版不附完整论文阅读报告或论文原件。后续公开示例按具体材料的展示与分享范围准备。

历史版本通过 Git 标签与 Releases 保留。写作规则的改动应来自真实任务和反馈；更新脚本后运行相关验证，不以结构检查代替内容或学习效果验证。

GitHub 可按版本管理发布说明及附件：[官方发布说明](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)。项目许可证的作用与添加方式见 [官方许可证说明](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)。
