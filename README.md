# Student_AS
## • 简述: 用 Google Dialogflow 作为自然语言处理的 SDK 实现了一个以智能会话机器人为核心的, 为悉尼大学学生服 务的在线咨询平台. 它能帮助学校的 Student Office 回答常遇见的 FAQ(例如, 帮助新生查教室地图), 在选课高峰期 提供课程咨询从而为人工服务需求削峰, 以及替代一些繁琐的文秘事务 (例如, 教授答疑的预约排号)
## • 前端: 用纯 JS+jQuery 实现了一个聊天界面原型, 之后准备用 React 替换
## • 应用服务器: 基于 Flask 实现应用服务器, 负责处理 http 请求和管理会话业务逻辑. 服务部署在 AWS EC2 上
## • 自然语言处理: 基于 Google Dialogflow 用 Python 作为 wrapper 构建出一个 NLP Service 负责识别 intent.
## • 数据模块: 用 MySQL 搭建了存储服务, 并且部署了爬虫定期从学校网页上抓取数据
## • 相关技能: Python, Flask, AWS, MySQL, Redis, Google Dialogflow SDK
