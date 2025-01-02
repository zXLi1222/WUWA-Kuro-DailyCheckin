# WUWA-Kuro-DailyCheckin

库街区鸣潮自动签到轻量级 Python 脚本。

## 功能
- 自动完成库街区签到和鸣潮每日签到。
- 没有任何多余的功能。

## 安装与使用

1. **下载脚本**
   - 克隆本仓库或直接下载 `Kuro.py` 。

2. **配置脚本**
   - 使用抓包工具获取库街区鸣潮签到的 `ROLE_ID`、`USER_ID` 和 `Token`。
   - 打开 `Kuro.py` 文件，使用获取到的值替换相应的占位符。

3. **运行脚本**
   - 将脚本移动到任意支持 Python 的环境中。（没有requests则需要 `pip install requests`）
   - 然后例如：
     - 在本地计算机上手动运行：`python Kuro.py`
     - 设置为服务器或任务自动化平台（如青龙面板）的定时任务。

## 参考
此项目参考自 [mxyooR/Kuro-autosignin](https://github.com/mxyooR/Kuro-autosignin)。
