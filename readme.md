# ExitTrack - 程序执行结果微信通知工具

ExitTrack 用于将程序执行结果发送到微信上，方便开发者远程监控程序运行状态。

## 功能特性

- 简单易用
- 程序执行完成后自动发送微信通知
- 支持自定义通知内容

## 安装

克隆本项目到本地，然后进入项目根目录并安装：
   ```bash
   git clone https://github.com/Chrono-Chasm/ExitTrack.git
   cd ExitTrack
   pip install .
   ```

## 快速开始

1. 只需要在程序开头导入模块：
   ```python
   import exit_track
   # your code here ...
   ```

2. 首次使用时，按照提示输入 SPT（单用户推送令牌）：
   - 获取 SPT 的链接：[https://wxpusher.zjiecode.com/docs/#/?id=%e8%8e%b7%e5%8f%96spt](https://wxpusher.zjiecode.com/docs/#/?id=%e8%8e%b7%e5%8f%96spt)
   - 用微信扫描即可获取自己的 SPT

   SPT 将默认保存在 `~/SPT.json` 文件中（可修改 `exit_track/init.py` 更改存储位置）

## 自定义通知内容

你可以覆盖默认的 `build_message` 函数来自定义通知内容：

```python
import exit_track

def build_message():
    summary = "执行成功" 
    message = exit_track.Message(
        content=f"{summary}：\n{exit_track.get_exit_info()}",
        summary=summary,
        content_type=1,
        spt=exit_track.SPT,
    )
    return message

exit_track.build_message = build_message
```

## API 参考

### 可用变量

- `exit_track.SPT`: 用户配置的单用户推送令牌

### 可用函数

- `get_exit_info()`: 获取程序退出信息
- `build_message()`: 构建消息内容（可覆盖）

### Message 类属性

| 属性 | 类型 | 必选 | 说明 |
|------|------|------|------|
| `content` | str | 是 | 消息正文内容 |
| `summary` | str | 否 | 消息摘要（默认截取 content 前20字符） |
| `content_type` | int | 否 | 内容类型（1=纯文本，2=HTML，3=Markdown，默认2） |
| `spt` | str | 否 | 单用户推送令牌 |
| `spt_list` | list[str] | 否 | 多用户推送令牌列表（最多10个） |
| `url` | str | 否 | 原文链接 |