# Paper Reading Lite · 先讲通论文的问题与方法

用一份连贯的中文图文报告，解释论文解决什么问题、采用什么方法、计算怎样一步步起作用，再展开实质创新、前作区别、设计理由、理论与实验依据，以及影响正确性、有效性和复现的细节。

“Lite”指流程集中、材料有用，不代表只看摘要或限定 20 分钟。长度服从理解需要。当前版本 **0.1.0**，采用 [MIT 许可证](LICENSE)，可作为 skill 或普通项目使用；版本与发布范围见 [发布说明](PUBLICATION.md)。

## 使用

从 [GitHub 仓库](https://github.com/Guokai-Liu/paper-reading-lite) 克隆项目，或在 [Releases](https://github.com/Guokai-Liu/paper-reading-lite/releases) 下载版本包。

~~~sh
git clone https://github.com/Guokai-Liu/paper-reading-lite.git
cd paper-reading-lite
~~~

提供 PDF、DOI、官方链接，或当前环境可访问的文献条目，并给助手这句话：

> 按 Paper Reading Lite 讲解这篇论文。读取本项目 PROMPT.md，沿论文自身的案例讲清问题、完整方法和设计依据，生成中文 Markdown 与深色 HTML，再核对前作差异、实验和容易遗漏的技术细节。

将整个项目目录放入代理支持的技能目录后，也可使用：

> 使用 $paper-reading-lite 讲解这篇论文。

技能入口是 [SKILL.md](SKILL.md)，与普通入口使用同一套规范。当前环境已有的 PDF、搜索、文件等能力完成阅读；本项目不包含模型 API 服务，也不要求安装一组其他阅读技能。后续局部问题保留原范围。

## 固定的写法

先讲完整故事，再沿实际计算顺序展开，最后用同一案例从输入走到输出。每一步说明接收什么、改变什么、为什么需要、下一步怎样使用。术语和前置知识就地补充，公式与原图对应正在解释的步骤。

| 六类内容 | 要回答的问题 |
|---|---|
| 完整故事 | 对象、任务、困难、核心改变和输出是什么？ |
| 问题与动机 | 旧办法具体卡在哪里，怎样引出本文设计？ |
| 方法与机制 | 对象如何变化，如何学习或运行，最终怎样得出结果？ |
| 证据 | 理论和实验验证了什么，支持范围有多大？ |
| 实质贡献与细节 | 与前作最小差别在哪里，忽略什么会改变方法或结论？ |
| 回看与复现条件 | 各步怎样连成整体，边界与材料缺口是什么？ |

不规定篇幅、图数或公式数；不拿模块列表、摘要改写或风险清单替代解释。标题随论文调整，具体取舍见 [写作基准](references/writing-standard.md)。

## 流程与材料

五阶段：来源确认 → 连贯解释 → 证据核对 → 轻量复现条件 → 显示检查与归档。

- [PROMPT.md](PROMPT.md)：执行流程。
- [报告模板](templates/report.md)：六类正文内容。
- [技术核查表](technical-checklist.md)：按论文挑选追查方向。
- [证据模板](templates/evidence.md)：来源、覆盖、主张、缺口与复现条件。
- [渲染器](scripts/render_report.py)：同源 Markdown → 离线深色 HTML。

原文、作者代码与原页是证据，已有报告只用于导航。案例不编造观测，作者动机、分析推断、实验证据与未知分别表达。学习报告不自动启动模型实验或外部发布。

## 目录与历史

已有工作区遵循当地约定；独立使用默认将每篇论文保存在 readings/<paper-id>/，用 DOI 或稳定标识避免重复目录。

~~~text
readings/<paper-id>/
  source/
  notes/workflows/lite-<YYYYMMDD>-<paper-id>-01/report.md
  notes/workflows/lite-<YYYYMMDD>-<paper-id>-01/report.html
  extractions/workflows/lite-<YYYYMMDD>-<paper-id>-01/evidence.md
  assets/workflows/lite-<YYYYMMDD>-<paper-id>-01/
~~~

重写递增编号，保留旧版本和其他路线。已有来源资产可以复用并注明来源。只创建实际需要的目录；报告完成、用户反馈、显示检查与实验复现分别记录。

## 生成网页

只用提示词不需要安装渲染依赖。随附渲染器需要 Python 3.9+、Node.js 和两个 Python 包；KaTeX 0.16.22 已附带。

~~~sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/render_report.py /path/to/report.md
~~~

默认在 Markdown 同目录生成 report.html，复制数学样式与字体到 render-assets/。已有 HTML 不会自动覆盖；确认本轮输出可替换后传 --overwrite。Node 不在 PATH 时传 --node。按论文隔离的工作区可用 --assets-dir 指定本篇资产目录：

~~~sh
.venv/bin/python scripts/render_report.py /path/to/report.md \
  --label "论文简称 · 问题与方法讲解" \
  --assets-dir /path/to/paper/assets/workflows/current-run/rendering
~~~

显示公式的两行 $$ 各自独占一行，前后留空行。渲染器支持显示公式、表格与相对路径图片；不处理行内 $...$ 或 Mermaid。需要它们时选用适用工具，不能把未渲染字符当成完成。

页面可离线显示数学，图片沿用报告路径；迁移时带上图片和 render-assets。仍需打开结果检查公式、原图、表格与窄屏布局，生成成功不能代替内容审读。

## 打包与验证范围

~~~sh
python3 scripts/build_release.py --output-dir dist
~~~

按文件清单生成 ZIP 与哈希清单，不打包阅读库。项目原创内容与脚本采用 [MIT 许可证](LICENSE)，KaTeX 保留其原有许可，见 [第三方说明](THIRD_PARTY_NOTICES.md)。

写作方式已有真实单篇阅读的正向反馈，不代表跨领域、跨模型或所有读者均有效。渲染和结构检查也不证明论文理解正确。后续根据真实反馈改进，不增加固定篇幅或模块配额。
