# 文件一键整理与复原工具

## 项目介绍
本工具是一个基于 Python 开发的文件整理与复原工具，它可以帮助用户快速对文件夹内的文件进行分类整理，同时支持一键将整理后的文件复原到原始位置。通过将其添加到 Windows 右键菜单，用户可以在任意文件夹上轻松执行整理和复原操作，极大地提高了文件管理的效率。

## 功能特性
1. **丰富的文件分类**：支持多种常见文件类型的分类，包括 Word 文档、Excel 表格、PPT、图片、视频、音频、程序代码、压缩文件等 20 多种类型。
2. **智能整理**：在整理文件前，会自动检查文件夹内存在的文件类型，并仅创建有对应文件的分类文件夹，避免出现空文件夹。
3. **一键复原**：再次点击右键菜单的“一键整理(整理/复原)”选项，即可将文件复原到整理前的原始位置。
4. **持久化记录**：即使电脑重启或原文件被删除，只要目标文件夹中的记录文件存在，复原功能仍然可以正常使用。

## 安装与使用

### 安装依赖
确保你的系统已经安装了 Python 环境（建议使用 Python 3.6 及以上版本）。如果尚未安装 Python，可以从 [Python 官方网站](https://www.python.org/downloads/) 下载并安装。

### 下载项目
你可以通过以下方式下载项目代码：
```bash
git clone https://github.com/Chiyang001/一键整理.git
cd 一键整理
```

### 打包成可执行文件（可选）
如果你想将脚本打包成独立的可执行文件（`.exe`），可以使用 `PyInstaller`。首先安装 `PyInstaller`：
```bash
pip install pyinstaller
```
然后在项目目录下执行以下命令进行打包：
```bash
pyinstaller --onefile --console file_sort.py
```
打包完成后，在 `dist` 目录下会生成一个名为 `file_sort.exe` 的可执行文件。

### 注册右键菜单
以管理员身份运行 `file_sort.exe`（如果是打包后的文件）或 `file_sort.py` 脚本，在菜单中选择“1. 开启”，即可将“一键整理(整理/复原)”选项添加到 Windows 右键菜单中。如果右键菜单未立即显示，请注销或重启计算机。

### 使用方法
- **整理文件**：在任意文件夹上右键单击，选择“一键整理(整理/复原)”，工具会自动对该文件夹内的文件进行分类整理。
- **复原文件**：再次在该文件夹上右键单击，选择“一键整理(整理/复原)”，工具会将文件复原到整理前的原始位置。

### 关闭功能
以管理员身份运行 `file_sort.exe` 或 `file_sort.py` 脚本，在菜单中选择“2. 关闭”，即可从右键菜单中移除该功能，并删除相关的备份文件和记录。

## 文件分类规则
以下是本工具支持的文件分类及其对应的扩展名：

| 分类 | 扩展名 |
| ---- | ---- |
| Word 文档 | doc, docx, docm, dot, dotx, dotm, wps, wpt, rtf, odt, docb |
| Excel 表格 | xls, xlsx, xlsm, xlt, xltx, xltm, xlsb, ods, csv, tsv |
| PPT | ppt, pptx, pptm, pot, potx, potm, pps, ppsx, ppsm, odp, ppam |
| 图片 | jpg, jpeg, png, gif, bmp, tiff, tif, psd, ico, webp, heic, heif, svg, raw, nef, cr2, orf, arw, dng |
| 文本 | txt, log, ini, cfg, json, xml, htm, html, md, nfo |
| 视频 | mp4, avi, mov, mkv, flv, wmv, rmvb, mpeg, mpg, 3gp, ts, vob, m4v, webm, ogv |
| 音频 | mp3, wav, ogg, aac, flac, wma, m4a, ape, opus, amr, mid, midi |
| 程序代码 | py, java, c, cpp, js, css, php, rb, go, sh, pl, lua, asm, cs, vb, fs, rs, swift, kt, dart, ts, scala, groovy |
| 压缩文件 | zip, rar, 7z, tar, gz, bz2, xz, zst |
| 数据库文件 | mdb, accdb, sqlite, sqlite3, db, dbf, sdf |
| 可执行文件 | exe, msi, com, bat, cmd, vbs, ps1 |
| 字体文件 | ttf, otf, fon, fnt |
| PDF 文件 | pdf |
| CAD 文件 | dwg, dxf, dwt, dwf |
| PSD 文件 | psd |
| AI 文件 | ai |
| EPS 文件 | eps |
| SVG 文件 | svg |
| 3D 模型文件 | obj, fbx, 3ds, stl, dae, blend |
| 动画文件 | fla, swf |
| 电子表格模板 | xlt, xltx, xltm |
| 演示文稿模板 | pot, potx, potm |
| 邮件文件 | eml, msg |
| 证书文件 | crt, cer, pem, pfx, p12 |
| 配置文件 | ini, cfg, conf, properties |
| 日志文件 | log |

## 注意事项
- 请确保以管理员身份运行脚本或可执行文件，否则可能无法正常注册右键菜单。
- 工具会在目标文件夹下创建一个名为 `file_sort_record.json` 的记录文件，请勿手动删除该文件，否则可能导致文件无法复原。
- 如果在使用过程中遇到问题，可以尝试重新注册右键菜单或重新运行脚本。

## 贡献与反馈
如果你对本项目有任何建议或发现了 bug，欢迎在 GitHub 上提交 issue 或 pull request。我们非常欢迎你的贡献，让这个工具变得更加完善！

## 许可证
本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT)，你可以自由使用、修改和分发本项目的代码。
