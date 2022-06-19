import requests
import json
import time
from Package import GetChildComments
def timestamp2time(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime
# 获取评论基本信息

def GetAnswerCommentsInfo(answer_id, headers, proxies):
    comments_url = "https://www.zhihu.com/api/v4/answers/{}/root_comments?limit=20&offset=0&order=normal&status=open".format(
        answer_id)
    try:
        res = requests.get(comments_url, headers=headers, proxies=proxies, timeout=(3, 7))
        res.encoding = "utf-8"
        jsonRes = json.loads(res.text)
        # print(jsonRes.keys())
#判断字典中key是否存在
        if 'error' not in jsonRes.keys():
#总评论数量
            if jsonRes["paging"]["totals"]:
                main_comments_count = jsonRes["paging"]["totals"]
            else:
                main_comments_count = 0

            if jsonRes["common_counts"]:
                total_comments_counts = jsonRes["common_counts"]
            else:
                total_comments_counts = 0

        else:
            main_comments_count = 0
            total_comments_counts = 0
        return main_comments_count, total_comments_counts
    except Exception as e:
        print("获取问题评论信息失败：", e)

# 获取评论
def GetAnswerComments(answer_id, offset, headers, proxies):
    # 1. 获取精华、讨论的评论
    comments_url = "https://www.zhihu.com/api/v4/answers/{}/root_comments?limit=20&offset={}&order=normal&status=open".format(
        answer_id, offset)
    # 2. 获取等待回答的评论
    # comments_url = "https://www.zhihu.com/api/v4/questions/{}/root_comments?order=normal&limit=10&offset={}&status=open".format(
    #     question_id, offset)
    print("评论链接为：",comments_url)
    MAX_ATTEMPTS = 20
    comments_lst = []
    try:
        res = requests.get(comments_url, headers=headers, proxies=proxies, timeout=(3, 7))
        res.encoding = "utf-8"
        jsonRes = json.loads(res.text)
        print(jsonRes)
        for item in jsonRes["data"]:

            # print(item)
            if item['reply_to_author']==None:
                if item["id"]:
                    comment_id = item["id"]
                else:
                    comment_id = None

                if item["top"]:
                    top = item["top"]
                else:
                    top = None

                if item["featured"]:
                    featured = item["featured"]
                else:
                    featured = None

                if item["created_time"]:
                    created_time = timestamp2time(item["created_time"])
                else:
                    created_time = None

                if item["vote_count"]:
                    vote_count = item["vote_count"]
                else:
                    vote_count = None

                if item["child_comment_count"]:
                    child_comment_count = item["child_comment_count"]
                else:
                    child_comment_count = None

                if item["content"]:
                    content = item["content"]
                else:
                    content = None

                if item["author"]["member"]["id"]:
                    author_id = item["author"]["member"]["id"]
                else:
                    author_id = None

                if item["author"]["member"]["avatar_url_template"]:
                    author_avatar_url_template = item["author"]["member"]["avatar_url_template"]
                else:
                    author_avatar_url_template = None

                if item["author"]["member"]["headline"]:
                    author_headline = item["author"]["member"]["headline"]
                else:
                    author_headline = None

                if item["author"]["member"]["gender"]:
                    author_gender = item["author"]["member"]["gender"]
                else:
                    author_gender = None

                if item["child_comment_count"]:

                    total_childcomments_lst=GetChildComments.GetTotal_ChildComments(comment_id, child_comment_count, headers, proxies, MAX_ATTEMPTS)
                else:
                    total_childcomments_lst=[]

                tem_dict_comment = {
                    "comment_id": comment_id,
                    "created_time": created_time,
                    "comment_content": content,
                    "is_top": top,
                    "is_featured": featured,
                    "vote_count": vote_count,
                    "child_comment_count": child_comment_count,
                    "author_id": author_id,
                    "author_avatar_url_template": author_avatar_url_template,
                    "author_headerline": author_headline,
                    "author_gender": author_gender,
                    "total_childcomments_lst":total_childcomments_lst
                    }

                comments_lst.append(tem_dict_comment)

    except Exception as e:
        print("获取offset={}问题评论失败：{}".format(offset, e))

    finally:
        return comments_lst

# 根据偏移量批量获取回复的第一层评论
def GetTotal_answers_Comments(answer_id, num_comments, headers, proxies,MAX_ATTEMPTS):

    try:
        offset = 0
        total_comments_lst = []
        print("评论总数为:", num_comments)
        while num_comments > 0 and offset < num_comments:
            attempts = 0
            success = False
            try:
                print("正在获取第{}_{}条评论".format(offset,offset+20))
                comments_lst = GetAnswerComments(answer_id, offset, headers, proxies)
                for item in comments_lst:
                    total_comments_lst.append(item)
                print(total_comments_lst)
                offset = offset + 20
                success = True
            except Exception as e:
                attempts=attempts+1
                print("获取第offset = {},Answers条评论失败，休息20秒.......".format(offset - 5))
                offset = offset - 5
                time.sleep(20)
                print("继续获取offset={},answers".format(offset))
                attempts = attempts + 1
                if attempts == MAX_ATTEMPTS:
                    break
                break
            finally:

                time.sleep(5)

        # return total_comments_lst
    except Exception as e:
        print("获取total_comments_lst失败", e)
    finally:
        return total_comments_lst

