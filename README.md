# f10-qt

f10-go 的桌面客户端。一个基于 PyQt5 + QtWebEngine 的 Windows 桌面悬浮窗，跟随通达信（TDX）行情软件当前查看的股票，以可配置的布局实时展示 F10 类个股资料与财务数据。

## 功能特性

- **五类数据展示窗口**：f10（公司资料）、f10a 补充、f10b 股东、f11 经营、f12 财务，各自对应一个独立的悬浮子窗口。
- **跟随通达信当前股票**：后台线程监听通达信主窗口（`TdxW_MainFrame_Class`）中标题为 `分析图表-<股票名>` 的子窗口，识别当前查看的股票，并将该股票的数据推送到已打开的子窗口。
- **布局可视化配置**：每类数据都有配置页（Config Layout），支持拖拽排序、双击单元格编辑样式（背景色、字号、加粗、是否显示、阈值、比较条件、日期格式），可 Save / Reset。
- **数值高亮**：数值类字段可设置阈值与比较条件（`gte` / `lt`），满足条件时按指定前景色高亮显示。
- **数据更新**：通过带 HMAC 签名头的 HTTP POST 从后端拉取数据，写入本地 `data/*.json` 后重新加载。
- **套用策略**：从 MongoDB（经 SSH 隧道）读取规则，生成各页面的 `context.js` 查询文件，并导出股东 VIP 名单。
- **全局快捷键**：`右 Ctrl + 右 Shift` 切换所有子窗口置顶；boss 模式下 `Alt 左` 或 `X` 快速退出。
- **半透明悬浮窗**：主窗口与子窗口均为 0.9 透明度、透明背景，可切换置顶。

## 技术栈

- Python 3.7（仓库内含有 `cpython-37` 的 `.pyc` 文件）
- PyQt5：`QWidget`、`QWebEngineView`、`QWebChannel`（作为前端 JS 与 Python 之间的桥接）
- 前端：Bootstrap 4、jQuery、Vue.js、qwebchannel.js，以及 bootstrap-select / colorpicker / datepicker / toggle 等组件

依赖库（从代码 import 推导，仓库未提供 `requirements.txt`）：

- `PyQt5`
- `psutil`
- `pywin32`（提供 `win32gui`）
- `pynput`
- `func_timeout`（PyPI 包名为 `func-timeout`）
- `requests`
- `pymongo`
- `sshtunnel`
- `pypinyin`

## 目录结构

```
.
├── main.py                        # 入口：主窗口、Router、Backend、通达信监听与快捷键
├── subWindow.py                   # 数据展示子窗口
├── apply_strat.py                 # "套用策略"：从 MongoDB 读取规则生成 context.js
├── common/
│   ├── fetch.py                   # 数据抓取（HTTP POST + HMAC 签名头）
│   ├── loadPage.py                # HTML 页面加载与 js/css 注入
│   ├── js_generator.py            # 根据 conf JSON 生成渲染 JS
│   └── genTemp/                   # 根据 conf 重新生成各页面 <template> 的脚本
├── pages/
│   ├── home/                      # 主页面（控制台 + 配置入口）
│   ├── f10/ f10a_supplement/ f10b_shareholder/ f11_industry/ f12_finance/
│   │   ├── *.html                 # 数据展示页
│   │   ├── *_conf.html            # 布局配置页
│   │   └── conf/*.json            # 每类数据的字段/样式/阈值配置
│   └── js/ css/                   # 前端静态资源
└── README.md
```

## 安装与环境要求

- 仅支持 Windows（依赖 `win32gui`、`ctypes.windll`，并通过 `psutil` 结束 `QtWebEngineProcess.exe`）。
- Python 3.7。
- 安装依赖：

```bash
pip install PyQt5 psutil pywin32 pynput func-timeout requests pymongo sshtunnel pypinyin
```

- 在仓库根目录运行（程序使用 `pages/`、`data/`、`pref.json` 等相对路径）。

## 使用方法

1. 在仓库根目录启动：

```bash
python main.py
```

2. 打开通达信（TDX）并进入某只股票的“分析图表”页面，程序会自动识别当前股票名。
3. 主窗口操作：
   - **Config Layout** 下拉菜单：进入 f10 / f10a补充 / f10b股东 / f11经营 / f12财务 各自的配置页。
   - **subWindows** 多选框：勾选要打开的数据窗口类型。
   - **Show**：打开所选数据子窗口，展示当前股票的数据。
   - **Update**：从后端拉取最新数据并刷新。
   - **套用策略**：从 MongoDB 生成策略查询。
   - **boss** 复选框：启用老板键模式。
4. 快捷键：
   - `右 Ctrl + 右 Shift`：切换所有子窗口置顶。
   - boss 模式下按 `Alt 左` 或 `X`：退出程序。

## 配置说明

- **页面布局配置**：位于 `pages/<类型>/conf/<类型>.json`，为数组结构。前 3 项为表头（name、code、updatetime），后续为字段项。字段常见属性：
  - `tag`：`text` / `num` / `date` / `blank` / `label`
  - `display`、`bold`、`font_size`、`bg_color`、`font_color`
  - `num` 类型另有 `threshold`（阈值）与 `cond`（`gte` / `lt` / `nil`）
  - `date` 类型另有 `format`（`0`=yyyy-mm-dd、`2`=yy-mm-dd、`5`=mm-dd）
- 也可通过配置页拖拽、双击编辑后点击 **Save** 保存；**Reset** 从 `pages/<类型>/conf/<类型>_bak.json` 还原（该备份文件需自行准备，仓库中未包含）。
- **窗口配置**：`pref.json` 保存主窗口与各子窗口配置（`topmost`、`boss`、`updatetime`、各类型窗口的 `height` / `width`），程序关闭时写盘，启动时读取。
- **数据文件**：`data/{f10,f10a_supplement,f10b_shareholder,f11_industry,f12_finance}.json` 由 **Update** 抓取生成，结构为 `{"msg": "<JSON 字符串>"}`。

## 注意事项 / 已知限制

- 仅支持 Windows，未做跨平台处理。
- 代码中的后端地址、HMAC 密钥（`common/fetch.py`）、MongoDB 与 SSH 隧道连接参数（`apply_strat.py`）以及 Update 请求地址（`pages/home/home.html` 中的 `"https://"`）以空字符串/占位符存在，使用 **Update** 与 **套用策略** 前需自行补齐。
- 启动需要 `pref.json` 与 `data/*.json` 存在；仓库未包含这些运行时文件，`pref.json` 缺失会导致启动失败。
- 仓库根目录混入了 QtWebEngine 运行时文件（`QtWebEngineProcess.exe`、`icudtl.dat`、`qtwebengine_resources*.pak`）以及 `__pycache__` 缓存文件。
