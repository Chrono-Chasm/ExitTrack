import requests
import json
from typing import Optional, List


from dataclasses import dataclass


@dataclass
class Message:
    content: str
    summary: Optional[str] = None
    content_type: int = 2
    spt: Optional[str] = None
    spt_list: Optional[List[str]] = None
    url: Optional[str] = None
    """
    content (str): 必传，消息正文内容
    summary (str): 可选，消息摘要（默认截取 content 前20字符）
    content_type (int): 可选，内容类型（1=纯文本，2=HTML，3=Markdown，默认2）
    spt (str): 可选，单用户推送令牌
    spt_list (list[str]): 可选，多用户推送令牌列表（最多10个）
    url (str): 可选，原文链接
    """

    def __str__(self) -> str:
        if self.spt is not None and self.spt_list is not None:
            raise ValueError("spt 和 spt_list 不可同时设置")
        if self.spt_list is not None and len(self.spt_list) > 10:
            raise ValueError("spt_list 最多支持10个用户")
        message = {
            "content": self.content,
            "summary": self.summary,
            "contentType": self.content_type,
        }
        if self.spt is not None:
            message["spt"] = self.spt
        elif self.spt_list is not None:
            message["sptList"] = self.spt_list
        if self.url is not None:
            message["url"] = self.url
        return json.dumps(message, ensure_ascii=False, indent=2)

    def send(self):
        try:
            response = requests.post(
                "https://wxpusher.zjiecode.com/api/send/message/simple-push",
                data=self.__str__(),
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            if response.status_code >= 200 and response.status_code < 300:
                try:
                    return (response.status_code, response.json())
                except json.JSONDecodeError:
                    return (response.status_code, response.text)
            else:
                return (response.status_code, response.text)

        except requests.exceptions.RequestException as e:
            return (None, f"请求失败: {e}")

