
from datetime import datetime, date, timedelta
import json
from typing import Dict
import feedparser
from dotenv import load_dotenv
import os
from notion_client import Client
import requests

class Config(object):
    
    _ = load_dotenv()
    
    @classmethod
    def get_attr(cls, key: str, default: str = None) -> str:
        return os.getenv(key, default= default)


class NewsCopilot(object):
    def __init__(self, feed_url):
        self.feed_url = feed_url
        self.content_entries = []
        self.notion_tools = NotionTools()
    
    def read_from_feed(self, start_date, end_date) -> object:
        """读取RSS feeds 源 获取文章的url
        """
        feed = feedparser.parse(self.feed_url)
        print(feed['feed']['title'])
        
       # 检查日期是否在时间范围内


        for entry in feed.entries:
            published_date =  datetime.strptime(entry.published,  '%a, %d %b %Y %H:%M:%S %Z')
            if start_date <= published_date.date() <= end_date:   
                self.content_entries.append(entry)
        
        return self

    
    def send_to_notion(self, ai: bool = False):
        for entry in self.content_entries:
            if ai:
                pass
            else:
                self.notion_tools.add_to_database(entry)
            
        return self


    def __parse_content(self, url) -> str:
        pass

    def __ai_summary(self, content: str):
        pass






class NotionTools(object):
    def __init__(self):
        # self.notion_client = Client(auth=Config.get_attr("NOTION_TOKEN"))
        self.notion_token = Config.get_attr("NOTION_TOKEN")
        self.database_id = Config.get_attr("DATABASE_ID")
        self.headers = {
            "Authorization": f"Bearer {self.notion_token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"  # 版本号
        }
        
        
        
    
    def add_to_database(self, entry: Dict):
        
        # 定义要添加到数据库的数据
        data = {
            "parent": {
                "database_id": self.database_id
            },
            "properties": {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": entry["title"]
                            }
                        }
                    ]
                },
                "URL": {
                    "url": entry["link"]
                },
                "PublishDate": {
                    "rich_text": [
                        {
                            "text": {
                                "content": entry["published"]
                            }
                        }
                    ]
                }
                
            }
        }
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=self.headers,
            data=json.dumps(data),
            proxies={"http": "http://127.0.0.1:10809", "https": "http://127.0.0.1:10809"}
        )
        print(response.content)
        
        print("create page success: %s" % entry["title"])
    




"""
从RSS中获取文字，并解析文章内容，然后通过AI总结文章内容，并将总结后的文章通过notion api存放到notion中
1. 读取RSS feeds 源，获取文章的url
2. 解析url,提取文章内容
3. 调用AI总结文章
4. 调用notion API,将文章发送到notion
"""
if __name__ == "__main__":
    
    feed_url = "https://theaisummer.com/feed.xml"
    with_ai = False
    news_copilot = NewsCopilot(feed_url)
    news_copilot.read_from_feed(start_date=date.today() - timedelta(days=1000), end_date=date.today()).send_to_notion(ai=with_ai)
    