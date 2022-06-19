import requests
import json
import time

def timestamp2time(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

# 获取评论
def GetChildComments(comment_id, offset, headers, proxies):
    # 获取子评论
    child_comments_url = "https://www.zhihu.com/api/v4/comments/{}/child_comments?limit=20&offset={}".format(
        comment_id, offset)

    print("评论链接为：",child_comments_url)

    child_comments_lst = []
    try:
        res = requests.get(child_comments_url, headers=headers, proxies=proxies, timeout=(3, 7))
        res.encoding = "utf-8"
        jsonRes = json.loads(res.text)

        for item in jsonRes["data"]:

            if item["id"]:
                child_comment_id = item["id"]
            else:
                child_comment_id = None

            if item["created_time"]:
                created_time = timestamp2time(item["created_time"])
            else:
                created_time = None

            if item["vote_count"]:
                vote_count = item["vote_count"]
            else:
                vote_count = None

            if item["content"]:
                content = item["content"]
            else:
                content = None

            if item["author"]["member"]["id"]:
                author_id = item["author"]["member"]["id"]
            else:
                author_id = None
            if item["author"]["member"]["gender"]:
                author_gender = item["author"]["member"]["gender"]
            else:
                author_gender = None

            if item["author"]["member"]["name"]:
                author_name = item["author"]["member"]["name"]
            else:
                author_name = None
            if item["author"]["member"]["headline"]:
                author_headline = item["author"]["member"]["headline"]
            else:
                author_headline = None

            if item["reply_to_author"]["member"]["gender"]:
                reply_author_gender = item["reply_to_author"]["member"]["gender"]
            else:
                reply_author_gender = None
            if item["reply_to_author"]["member"]["id"]:
                reply_author_id = item["reply_to_author"]["member"]["id"]
            else:
                reply_author_id = None
            if item["reply_to_author"]["member"]["name"]:
                reply_author_name = item["reply_to_author"]["member"]["name"]
            else:
                reply_author_name = None


            tem_dict_comment = {
                "child_comment_id": child_comment_id,
                "created_time": created_time,
                "child_comment_content": content,
                "vote_count": vote_count,
                "author_id":author_id,
                "author_gender":author_gender,
                "author_name":author_name,
                "author_headline":author_headline,
                "reply_author_gender":reply_author_gender,
                "reply_author_id":reply_author_id,
                "reply_author_name":reply_author_name
                 }

            child_comments_lst.append(tem_dict_comment)
        # print(comments_lst)

    except Exception as e:
        print("获取offset={}问题评论失败：{}".format(offset, e))

    finally:
        return child_comments_lst

# 获取评论
def GetTotal_ChildComments(comment_id, num_comments, headers, proxies,MAX_ATTEMPTS):
    try:
        offset = 0
        total_childcomments_lst = []
        print("子评论回复总数为:", num_comments)
        while num_comments > 0 and offset < num_comments:
            attempts = 0
            success = False
            try:
                print("正在获取第{}_{}条子评论".format(offset,offset+20))
                child_comments_lst = GetChildComments(comment_id, offset, headers, proxies)
                # 当子评论的数量过多的时候，按照偏移量来爬，每次会存一个列表，导致最后总的子评论的爬取的结果是列表嵌套列表的形式，故需遍历列表只存里面的元素
                for item in child_comments_lst:
                    total_childcomments_lst.append(item)
                offset = offset + 20
                success = True
            except Exception as e:

                attempts = attempts + 1
                print("获取第offset = {},Answers条子评论失败，休息20秒.......".format(offset - 5))
                offset = offset - 5
                time.sleep(20)
                print("继续获取offset={},answers".format(offset))
                attempts = attempts + 1
                if attempts == MAX_ATTEMPTS:
                    break
                break
            finally:
                time.sleep(5)
        print(total_childcomments_lst)
        return total_childcomments_lst
    except Exception as e:
        print("获取total_childcomments_lst失败", e)
    finally:
        return total_childcomments_lst

