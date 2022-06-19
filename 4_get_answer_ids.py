# import re
import os
import json

def parse_xml(xml_file):
    pass
#返回路径列表
def get_files_list(raw_dir):
    files_list = []
    for filepath,dirnames,filenames in os.walk(raw_dir):
        for filename in filenames:
            files_list.append(filepath+'/'+filename)
    return files_list

def get_answer_id_list(files_list):
    answer_id_list = []
    for item in files_list:
        # print(item)
        with open(item,'r', encoding="utf-8") as f:
            answers_list = json.load(f)
            for answers in answers_list:
                # print(answers)
                # print(answers["answer_id"])

                answer_id_list.append(answers["answer_id"])
    return answer_id_list


def cut_list(answer_id_list, cut_len):
    """
    将列表拆分为指定长度的多个列表
    :param answer_id_list: 初始列表
    :param cut_len: 每个列表的长度
    :return: 一个二维数组 [[x,x],[x,x]]
    """
    if len(answer_id_list) > cut_len:
        for i in range(int(len(answer_id_list) / cut_len)):
            cut_a = answer_id_list[cut_len * i:cut_len * (i + 1)]
            with open("../data/answersid"+str(i)+".json", 'w', encoding="utf-8") as f:
                json.dump(cut_a, f, ensure_ascii=False)

# "19629961","19651260","19684571"
# essence,top_activity
if __name__ == '__main__':
    raw_dir = "output/answers/19629961/top_activity"
    file_list = get_files_list(raw_dir)
    answer_id_list=[]
    answerid_list = get_answer_id_list(file_list)
    answer_id_list = list(set(answerid_list))
    with open("output/answers/19629961/top_activity/answersid_top1.json",'w', encoding="utf-8") as f:
        json.dump(answer_id_list, f, ensure_ascii=False)
    # cut_list(answer_id_list,100000)

    print(len(answer_id_list))

# answersid_ess1.json(4700) 已爬
dir = "output/comments/19629961/essence"

# answersid_ess2.json(38217) 已爬
dir = "output/comments/19651260/essence"

# answersid_ess3.json(48000) 已爬
dir = "output/comments/19684571/essence"

# answersid_top1.json(3435) 已爬
dir = "output/comments/19629961/top_activity"

# answersid_top2.json(21030) 已爬
dir = "output/comments/19651260/top_activity"

# answersid_top3.json(11157)
dir = "output/comments/19684571/top_activity"


