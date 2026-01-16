# 🚀 oniWikiBot (缺氧维基同步助手)

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

用于 **[缺氧Wiki主站点](https://oni.wiki)** 与 **[缺氧Bwiki](https://wiki.biligame.com/oni/)** 之间内容自动化同步的高效率工具集。

## 🌟 核心能力
- **全量/增量同步**：支持同步全站页面、特定分类或单个页面。
- **媒体资产搬运**：检测并同步缺失的游戏图标、原画等图片资源。
- **模块/模板转换**：自动适配两站之间 Lua 模块和模板语法的差异。
- **断点续传**：针对 Bwiki API 不稳定的特性，内置重试与错误跳过机制。
