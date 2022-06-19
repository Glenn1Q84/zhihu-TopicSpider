## Zhihu-TopicSpider

**截至2022-5月还是有效的**

爬取知乎话题下的问答数据，并且保存到本地（没有使用数据库），知乎话题数据主要分为讨论(essence)、精华(top_activity)、等待回答(question)，在抓取时也是按照这三类数据分别抓取。

**注意：**当前知乎页面仅仅展示一部分数据，本项目只能抓取展示出来的数据

## 支持的内容

- 指定话题下的所有问题信息（id,创建时间，浏览量，评论量）

- 问题下的所有回答（id,内容，点赞、评论）
- 回答下的所有评论（包括子评论，id，用户，点赞）



## **抓取思路**

问题id→回答id→评论：即先获取所有的问题id，然后根据问题id抓取所有的回答（包括回答id），接着根据回答id抓取对应的评论数据



## 如何运行

考虑到抓取的数据量比较大，容易被封IP，所以需要购买IP，5元/24小时，自己这边用的是讯代理，然后修改文件里面的IP地址

- **相关包的安装**

```python
pip install urllib3=1.25.11
pip install requests=2.26.0
pip install pyexecjs=1.5.1
```

- 运行pyexecjs需要安装node.js，具体安装过程如下：

  [node.js安装及环境配置超详细教程【Windows系统安装包方式】 - 明金同学 - 博客园 (cnblogs.com)](https://www.cnblogs.com/vmuu/p/15663250.html#_label1)

  安装软件，配置环境变量，以及通过npm命令安装jsdom包

  安装之后可以通过以下命令查看默认的安装路径,即jsdom

  ```
  npm root -g
  ```

  装好之后 修改Package/encrypt.py 的路径  path为自己的项目路径 path= "F:\Glenn\workspace_for_pycharm\zhihuspider"

- **抓取问题数据**,	1_QuestionInfo.py,抓好之后获取问题id，2_get_ids	

- **抓取回答**，3_get_answers.py; 抓好之后获取问答id, 4_get_answer_ids.py

- **抓取评论**，5_get_comments.py

- **最后是对数据的合并与清洗**，存储为id2data的形式到1_concated_data中，6_construct_question_id2data.py, 7_construct_QA_pairs.py,  8_construct_AC_pairs.py,

  

## 写在最后



仅可用于科研用途，抓取数据请谨慎，由此产生的法律纠纷后果自负！！！