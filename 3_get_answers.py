import requests
import json

import os
from utils import json_read
import re
from Package.encrypt import encrypt

import time
def timestamp2time(timestamp):
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def ensure_dir(filename):
    (path, name) = os.path.split(filename)
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, " is created")
    else:
        print(path, " already exists")

def json_write(data, filename):
    with open(filename, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
        print("成功保存文件{}".format(str(filename)))

class GetAnswerInfo():
    def __init__(self, question_id,proxies):
        self.question_id = question_id
        self.proxies = proxies

    def __get_url(self):
        url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset=8&platform=desktop&sort_by=default".format(
            self.question_id)
        return url

    def __get_html(self):
        try:
            # requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            # requests.DEFAULT_RETRIES = 5
            URL = self.__get_url()
            headers = get_headers(URL)
            r = requests.get(url=URL, headers=headers, proxies=self.proxies)
            r.encoding = 'utf-8'
            jsonAnswer = json.loads(r.text)
            return jsonAnswer

        except Exception as e:
            print("获取html失败:", e)
    def get_totals(self):
        max_answers_count= self.__get_html()["paging"]["totals"]

        return max_answers_count


class GetOneAnswer():
    def __init__(self, question_id, offset, proxies):
        self.question_id = question_id
        self.proxies = proxies
        self.offset = offset

    def __get_url(self):
        url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Creaction_instruction%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cvip_info%2Cbadge%5B%2A%5D.topics%3Bdata%5B%2A%5D.settings.table_of_content.enabled&limit=5&offset={}&platform=desktop&sort_by=default".format(
            self.question_id, self.offset)
        print(url)
        return url

    def __get_html(self):
        try:

            # requests.DEFAULT_RETRIES = 5
            URL = self.__get_url()
            headers = get_headers(URL)
            r = requests.get(url=URL, headers=headers, proxies=self.proxies)
            r.encoding = 'utf-8'
            jsonAnswer = json.loads(r.text)
            return jsonAnswer

        except Exception as e:
            print("获取html失败:", e)

    def parse_html(self):
        jsonAnswer_data = self.__get_html()["data"]

        answer_lst = []

        for i, item in enumerate(jsonAnswer_data):
            print("当前时间：{},正在获取第{}条回答".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), i + self.offset))
            if item["id"]:
                answer_id = item["id"]
            else:
                answer_id = None

            if item["created_time"]:
                created_time = timestamp2time(item["created_time"])
            else:
                created_time = None

            if item["content"]:
                content = item["content"]
            else:
                content = None

            if item["comment_count"]:
                comment_count = item["comment_count"]
            else:
                comment_count = None

            if item["voteup_count"]:
                voteup_count = item["voteup_count"]
            else:
                voteup_count = None

            if item["author"]["id"]:
                author_id = item["author"]["id"]
            else:
                author_id = None

            if item["author"]["name"]:
                author_name = item["author"]["name"]
            else:
                author_name = None

            if item["author"]["gender"]:
                author_gender = item["author"]["gender"]
            else:
                author_gender = None


            if item["author"]["avatar_url_template"]:
                author_avatar_url_template = item["author"]["avatar_url_template"]
            else:
                author_avatar_url_template = None

            if item["author"]["follower_count"]:
                author_follower_count = item["author"]["follower_count"]
            else:
                author_follower_count = None

            dict_answer = {
                "answer_id": answer_id,
                "created_time": created_time,
                "content": content,
                "comment_count": comment_count,
                "voteup_count": voteup_count,
                "author_id": author_id,
                "author_name": author_name,
                "author_gender": author_gender,
                "author_avatar_url_template": author_avatar_url_template,
                "author_follower_count": author_follower_count,
            }

            answer_lst.append(dict_answer)
        return answer_lst


def GetAnswers(question_id,answer_count_proportion, proxies,MAX_ATTEMPTS):

    Answer = GetAnswerInfo(question_id,proxies)
    max_answers_count=Answer.get_totals()
    true_answer_count = int(max_answers_count * answer_count_proportion)

    print("当前时间={} ,question_id={},共有={}条回答,百分比获取回答数为={}".format(
        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        question_id,
        max_answers_count,
        true_answer_count))

    if max_answers_count > 0:
        offset = 0
        total_answer_lst = []

        while offset <= true_answer_count:
            attempts = 0
            print("当前时间：{},正在获取offset={}条回答".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), offset))
            s1_time = time.perf_counter()

            Answers = GetOneAnswer(question_id=question_id, offset=offset,proxies=proxies)
            answer_lst = Answers.parse_html()
            total_answer_lst.append(answer_lst)
            offset = offset + 5

            e1_time = time.perf_counter()
            print("获取本次回答共用时：", e1_time - s1_time)
            # print(answer_lst)
            success = True

        return total_answer_lst

    else:
        print("该问题没有回答，返回None")
        return None


def get_sublist_all_elements(input_lst):
    out_lst = []
    for item in input_lst:
        out_lst.extend(item)
    return out_lst

def get_headers(url):
    X_ZSE_93 = '101_3_2.0'
    useragent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'
    sign, cookies = encrypt(X_ZSE_93,''.join(re.sub(r'.*zhihu\.com', '', url)))
    headers = {
        'cookie': f'd_c0={cookies}',
        'user-agent': useragent,
        'x-zse-93': X_ZSE_93,
        'x-zse-96': sign
    }
    return headers


if __name__ == '__main__':
    COOKIE = None
    proxy_account = "fee2dyq3og:2giw3nwhny@103.45.149.120:23128"
    # PROXIES = None
    PROXIES = {"HTTP": "HTTP://" + proxy_account}

    # 20220415-爬取“心理调节”话题得回复
    # question_id_list=['27194444', '38984755', '308275920', '21951584', '22608645', '364386829', '20767147', '21403560', '19679597', '19836269', '20153152', '316204212', '36477128', '22365614', '20426168', '20209387', '20759341', '27471029', '20070406', '21102904', '51953660', '53674410', '20180522', '40002699', '313253074', '29616331', '20789738', '25049123', '22396868', '23282866', '20051430', '27370025', '416520855', '24747546', '25626411', '19645059', '19669370', '21153343', '24371293', '31358240', '347818182', '22585652', '28615080', '30808086', '20957255', '24931238', '24498481', '23608154', '21991429', '22042943', '53063663', '21920970', '19837191', '24340654', '20992510', '19824961', '21064891', '20523909', '29232845', '30100788', '19677262', '34364621', '32134058', '20796753', '21461593', '24961825', '25406616', '21262394', '37674051', '24935778', '24483755', '29346788', '19673439', '23983772', '21091381', '22357357', '26718356', '21416791', '360251615', '19945123', '37727719', '19664834', '22466837', '20316505', '338680917', '26420320', '20496103', '28136693', '20296633', '27717761', '22626736', '38633923', '23002777', '22785405', '280683449', '20950329', '20358871', '20616360', '28580287', '21070731', '297097842', '21644977', '22718330', '29526689', '20968621', '20395658', '20448381', '26607496', '38620091', '35061183', '20789110', '53173829', '26115166', '65953333', '19633167', '35024322', '24312500', '38195280', '20686139', '20432746', '42342303', '39846270', '49966636', '19968811', '20002241', '21412667', '23819435', '26381580', '21025435', '31523163', '23976942', '20092949', '26602178', '24139572', '20509030', '22473809', '19596092', '21825731', '20416237', '309190164', '21031119', '22631639', '26477174', '20519316', '20082652', '314565807', '25863152', '20367993', '28098994', '30071123', '23061690', '21787084', '27291868', '25355116', '26851861', '20336901', '26818538', '19725245', '20815246', '26430231', '21612142', '20017461', '23065717', '418660624', '53046122', '26952431', '20252024', '320551152', '19903161', '25311491', '302891294', '26425227', '24991010', '31101342', '26927807', '19913464', '20069379', '20850248', '31635717', '20470188', '20325361', '19882337', '27552810', '21336869', '22514517', '25000204', '22684817', '23705972', '20571085', '34335298', '38303405']

    # 20220419心理调节下面的回复
    # question_id_list=[ '20789110', '27194444', '38984755', '21951584', '22608645', '364386829', '20767147', '21403560', '19679597', '19836269', '20153152', '36477128', '22365614', '20426168', '20209387', '20759341', '27471029', '20070406', '51953660', '53674410', '20180522', '313253074', '29616331', '20789738', '22396868', '23282866', '20051430', '27370025', '416520855', '24747546', '19645059', '19669370', '21153343', '24371293', '31358240', '22585652', '28615080', '30808086', '20957255', '24931238', '24498481', '23608154', '21991429', '22042943', '53063663', '21920970', '19837191', '24340654', '20992510', '19824961', '21064891', '20523909', '29232845', '30100788', '19677262', '34364621', '32134058', '20796753', '21461593', '24961825', '25406616', '21262394', '37674051', '24935778', '24483755', '29346788', '19673439', '23983772', '21091381', '22357357', '26718356', '21416791', '360251615', '19945123', '37727719', '19664834', '22466837', '20316505', '338680917', '26420320', '20496103', '28136693', '20296633', '27717761', '22626736', '38633923', '23002777', '22785405', '280683449', '20950329', '20358871', '20616360', '28580287', '21070731', '297097842', '21644977', '22718330', '29526689', '20968621', '20395658', '20448381', '26607496', '38620091', '35061183','53173829', '26115166', '65953333', '19633167', '35024322', '24312500', '38195280', '20686139', '20432746', '42342303', '39846270', '49966636', '19968811', '20002241', '21412667', '23819435', '26381580', '21025435', '31523163', '23976942', '20092949', '26602178', '24139572', '20509030', '22473809', '19596092', '21825731', '20416237', '309190164', '21031119', '22631639', '26477174', '20519316', '20082652', '314565807', '25863152', '20367993', '28098994', '30071123', '23061690', '21787084', '27291868', '25355116', '26851861', '20336901', '26818538', '19725245', '20815246', '26430231', '21612142', '20017461', '23065717', '418660624', '53046122', '26952431', '20252024', '320551152', '19903161', '25311491', '302891294', '26425227', '24991010', '31101342', '26927807', '19913464', '20069379', '20850248', '31635717', '20470188', '20325361', '19882337', '27552810', '21336869', '22514517', '25000204', '22684817', '23705972', '20571085', '34335298', '38303405']
    for topic_id in ["19629961","19651260","19684571"]:
        for type_name in ["essence","top_activity"]:
            question_id_list= json_read("F:\Glenn\workspace_for_pycharm\zhihuspider\output\{}\{}_ids.json".format(topic_id,type_name))
            print("topic_id = {}".format(topic_id))
            error_question=[]
            for i,item in enumerate(question_id_list):
                print("{}/{}".format(i,len(question_id_list)))
                try:
                    QUESTION_ID=item

                    dir = os.path.join("./output/answers",topic_id,type_name)
                    ensure_dir(dir)
                    MAX_ANSWER_COUNT = 20
                    ANSWER_COUNT_PROPORTION = 1
                    answer_lst = GetAnswers(question_id=QUESTION_ID,
                                                 answer_count_proportion=ANSWER_COUNT_PROPORTION,
                                                 proxies=PROXIES,
                                                MAX_ATTEMPTS=5
                                            )
                except:
                    error_question.append(item)
                    json_write(error_question,"F:\Glenn\workspace_for_pycharm\zhihuspider\output\{}\{}_error_ids.json".format(topic_id,type_name))
                    continue

                finally:
                    filename=dir + "/" + str(QUESTION_ID) + ".json"
                    ensure_dir(filename)
                    cancate_answer_lst = get_sublist_all_elements(answer_lst)
                    json_write(cancate_answer_lst,filename)
                    # with open(dir + "/" + str(QUESTION_ID) + ".json", 'w', encoding="utf-8") as f:
                    #     print(dir + "/" + str(QUESTION_ID) + ".json")
                    #     json.dump(cancate_answer_lst, f, ensure_ascii=False)

            print(type(answer_lst), len(answer_lst))
            print(type(answer_lst[0]), len(answer_lst[0]))
            print(answer_lst[0])

