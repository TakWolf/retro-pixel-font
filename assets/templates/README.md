![banner](docs/readme-banner.png)

# 复古像素字体 / Retro Pixel Font

[![SIL Open Font License 1.1](https://img.shields.io/badge/license-OFL--1.1-orange)](https://scripts.sil.org/OFL)
[![MIT License](https://img.shields.io/badge/license-MIT-green)](https://opensource.org/licenses/MIT)
[![Releases](https://img.shields.io/github/v/release/TakWolf/retro-pixel-font)](https://github.com/TakWolf/retro-pixel-font/releases)

一组开源的有怀旧游戏感觉的像素字体。字体基本上以英文、数字和符号为主。

如果您在寻找开源的泛中日韩或 Unicode 像素字体，请尝试 [「方舟像素字体」](https://github.com/TakWolf/ark-pixel-font) 。

这个项目不仅提供了全部的字形源文件，也提供了构建字体所需要的完整程序。

- [主页](https://retro-pixel-font.takwolf.com)
- [itch.io](https://takwolf.itch.io/retro-pixel-font)

## 预览

可以通过 [主页](https://retro-pixel-font.takwolf.com) 实时预览字体效果。

{{ preview }}

## 下载和使用

可在 [Releases](https://github.com/TakWolf/retro-pixel-font/releases) 下载最新的版本。

使用时请注意正确地设置渲染尺寸。

## 本地构建

这是一个标准的 [Python3](https://www.python.org) 项目。

当您配置好运行环境后，执行 `python ./build.py` 命令来开始构建。

等待任务完成后，可在 `build/outputs` 目录下找到生成的字体文件。

## 授权信息

分为「字体」和「构建程序」两个部分。

### 字体

使用 [SIL 开放字体许可证第 1.1 版](LICENSE-OFL) 授权。

### 构建程序

使用 [MIT 许可证](LICENSE-MIT) 授权。

## 程序依赖

- [FontTools](https://github.com/fonttools/fonttools)
- [Brotli](https://github.com/google/brotli)
- [Unidata Blocks](https://github.com/TakWolf/unidata-blocks)
- [PyPNG](https://gitlab.com/drj11/pypng)
- [Pillow](https://github.com/python-pillow/Pillow)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- [Jinja](https://github.com/pallets/jinja)
- [GitPython](https://github.com/gitpython-developers/GitPython)

## 赞助

如果这个项目对您有帮助，请考虑赞助来支持开发工作。

- [收款码](https://github.com/TakWolf/TakWolf/blob/master/payment-qr-codes.md)
- [爱发电](https://afdian.net/@takwolf)

赞助时请留下您的称呼，该信息将会被添加到赞助商列表中。

可以通过下面的链接来查看收到的赞助的具体情况：

[赞助详情](https://github.com/TakWolf/TakWolf/blob/master/sponsors.md)
