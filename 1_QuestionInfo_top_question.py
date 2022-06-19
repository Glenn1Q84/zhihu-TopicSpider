import os.path

import requests
import json
import time
import re,os
from Package.encrypt import encrypt
from utils import json_write,txt_save,ensure_dir

def timestamp2time(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


class GetOneQuestion():
    def __init__(self, topic_id, offset, proxies):
        self.topic_id = topic_id
        self.proxies = proxies
        self.offset = offset

    def __get_url(self):

        url = "https://www.zhihu.com/api/v4/topics/{}/feeds/top_question?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&offset={}&limit=10&after_id=0".format(
            self.topic_id, self.offset)
        print(url)
        return url

    def __get_html(self):
        try:

            # requests.DEFAULT_RETRIES = 5
            URL = self.__get_url()
            headers = get_headers(URL)

            r = requests.get(url=URL, headers=headers, proxies=self.proxies)
            r.encoding = 'utf-8'
            jsonQuestion = json.loads(r.text)
            return jsonQuestion

        except Exception as e:
            print("获取html失败:", e)

    def parse_html(self):
        jsonAnswer_data = self.__get_html()["data"]
        question_lst = []
        for i, item in enumerate(jsonAnswer_data):
            # if item["attached_info"]==None:
            #     print(0)
            print("当前时间：{},正在获取第{}问题".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), i + self.offset))

            target = item.get("target")

            question_id = target.get("id")
            question_title = target.get("title")
            created_time = target.get("created_time")
            type = target.get("type")

            answer_count = target.get("answer_count")
            visit_count = target.get("visit_count")
            follower_count = target.get("follower_count")

            dict_question = {
                "question_id":question_id,
                "question_title":question_title,
                "created_time": timestamp2time(created_time),
                "type":type,
                "answer_count":answer_count,
                "visit_count":visit_count,
                "follower_count":follower_count
            }
            question_lst.append(dict_question)

        return question_lst

# https://www.zhihu.com/api/v4/topics/19550937/feeds/top_question?include=data%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Canswer_type%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.paid_info%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Chermes_label%2Cis_labeled%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target.annotation_detail%2Ccomment_count%3B&limit=10&after_id=0


def GetQuestion(topic_id, question_count,start_offset, proxies,MAX_ATTEMPTS,save_dir):
    ensure_dir(save_dir)
    offset = start_offset
    error_offset = []
    while offset <= question_count:
        attempts = 0
        success = False
        while attempts < MAX_ATTEMPTS and not success:
            try:
                print("当前时间：{},正在获取offset={}条问题".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), offset))
                s1_time = time.perf_counter()

                Question = GetOneQuestion(topic_id=topic_id, offset=offset,proxies=proxies)
                qestion_lst = Question.parse_html()

                filename = os.path.join(save_dir,"offset_{}.json".format(str(offset)))
                print("成功保存offset={}至：".format(offset),filename)
                json_write(data=qestion_lst, filename=filename)
                e1_time = time.perf_counter()
                print("获取本次回答共用时：", e1_time - s1_time)
                success = True

                offset = offset + 5
                time.sleep(5)


            except:
                attempts=attempts+1
                print("获取第offset = {}条问题失败，休息20秒.......".format(offset))
                time.sleep(20)
                print("继续获取offset={},attempts={}".format(offset,attempts))
                if attempts == MAX_ATTEMPTS:
                    print("获取offset={}失败，跳过本次offset".format(offset))
                    error_offset.append(offset)
                    offset = offset + 5
                    break
            finally:
                if len(error_offset) != 0:
                    error_filename = os.path.join(save_dir,"error_offsets.txt")
                    txt_save(input_list=error_offset,filename=error_filename)



def get_sublist_all_elements(input_lst):
    out_lst = []
    for item in input_lst:
        out_lst.extend(item)
    return out_lst

def get_headers(url):
    X_ZSE_93 = '101_3_2.0'
    useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    sign, cookies = encrypt(X_ZSE_93,''.join(re.sub(r'.*zhihu\.com', '', url)))
    headers = {
        'cookie': f'd_c0={cookies}',
        'user-agent': useragent,
        'x-zse-93': X_ZSE_93,
        'x-zse-96': sign
    }
    return headers


if __name__ == '__main__':
    # COOKIE = None
    # HEADERS = get_headers()
    proxy_account = "fee2dyq3og:2giw3nwhny@103.45.149.120:23128"

    PROXIES = {"HTTP": "HTTP://" + proxy_account}
    topic_id = "19651260"
    dir = "top_question/questions_info"
    save_dir = os.path.join("output",topic_id,dir)
    GetQuestion(topic_id=topic_id, question_count=1100,start_offset=0, proxies=PROXIES,MAX_ATTEMPTS=5,save_dir=save_dir)


