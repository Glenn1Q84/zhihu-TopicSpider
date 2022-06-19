from Package import GetAnswerComments
import json
import time
import os





def get_sublist_all_elements(input_lst):
    out_lst = []
    for item in input_lst:
        out_lst.extend(item)
    return out_lst

def ensure_dir(filename):
    (path, name) = os.path.split(filename)
    if not os.path.exists(path):
        os.makedirs(path)
        print(path, " is created")
    else:
        print(path, " already exists")
if __name__ == '__main__':
    COOKIE = None
    HEADERS = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'cookie': COOKIE,
        'Connection': 'close'
    }

    # ANSWER_ID = 322704508
    proxy_account = "fee2dyq3og:2giw3nwhny@103.45.149.120:23128"
    # PROXIES = None
    PROXIES = {"HTTP": "HTTP://" + proxy_account}
    # PROXIES = None
    dir = "output/comments/19684571/essence"
    OFFSET = 0
    MAX_ATTEMPTS = 20

with open("output/comments/answersid_ess3.json", 'r', encoding="utf-8") as f:
        answersid_list = json.load(f)
        start_num=11079

        MAX_ATTEMPTS = 5
        for i,ANSWER_ID in enumerate(answersid_list):
            if i >= start_num:

                attempts = 0
                success = False
                while attempts < MAX_ATTEMPTS and not success:
                    try:
                        print("当前时间：{}，正在获取第{}个回复的评论".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), i))
                        # 总评论的个数
                        main_comments_count, total_comments_counts= GetAnswerComments.GetAnswerCommentsInfo(answer_id=ANSWER_ID,headers=HEADERS,proxies=PROXIES)
                        #print(main_comments_count,total_comments_counts)
                        if total_comments_counts>0 :

                            comments = GetAnswerComments.GetTotal_answers_Comments(answer_id=ANSWER_ID,num_comments = total_comments_counts, headers=HEADERS,proxies=PROXIES,MAX_ATTEMPTS=MAX_ATTEMPTS)
                            # print(comments)
                            # cancate_comments_lst = get_sublist_all_elements(comments)
                            print("爬取的完整评论：")
                            # print(comments)
                            filename=dir + "/" + str(ANSWER_ID) + ".json"
                            ensure_dir(filename)
                            with open(filename, 'w', encoding="utf-8") as f:
                                print(dir + "/" + str(ANSWER_ID) + ".json")
                                json.dump(comments, f, ensure_ascii=False)
                        success = True
                    except:
                        attempts = attempts + 1
                        print("获取第{}条回复失败，休息20秒.......".format(i))
                        time.sleep(20)
                        print("继续获取{},attempts={}".format(i, attempts))
                        if attempts == MAX_ATTEMPTS:
                            print("获取ｉ={}失败，跳过本次回复".format(i))
                            i = i+1
                            break

