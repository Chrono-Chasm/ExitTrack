from .exit_hooks import *
from .wxpush import Message
from pathlib import Path
import json

try:
    with open(Path("~/SPT.json").expanduser()) as f:
        SPT = json.load(f)["SPT"]
except Exception as e:
    SPT = input("Please enter your SPT(https://wxpusher.zjiecode.com/docs/#/?id=%e8%8e%b7%e5%8f%96spt):")
    with open(Path("~/SPT.json").expanduser(), "w") as f:
        json.dump({"SPT": SPT}, f)


def build_message():
    summary = "喜报" if EXIT_STATUS == 0 else "悲报"
    message = Message(
        content=f"{summary}：\n{get_exit_info()}",
        summary=summary,
        content_type=1,
        spt=SPT,
    )
    return message


def send_message():
    status_code, result = build_message().send()
    print(f"status_code: {status_code}")
    print(f"result: {result}")


exit_hooks.add_exit_hook(send_message)

__all__ = [
    "EXIT_STATUS",
    "get_exit_info",
    "build_message",
    "Message",
    "SPT",
    "exit_hooks",
]
