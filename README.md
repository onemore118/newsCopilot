# newsCopilot
从RSS源获取新闻，然后存入notion。并且有AI总结和翻译功能，快速查看行业资讯。

从RSS中获取文字，并解析文章内容，然后通过AI总结文章内容，并将总结后的文章通过notion api存放到notion中
1. 读取RSS feeds 源，获取文章的url
2. 解析url,提取文章内容
3. 调用AI总结文章
4. 调用notion API,将文章发送到notion
