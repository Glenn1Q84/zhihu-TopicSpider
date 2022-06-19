from utils import json_read, json_write,get_files_list,ensure_dir

def get_data_by_filename(filename):
    data = json_read(filename)
    all_Q_ids = []
    Qid2data = dict()
    for item in data:
        id = item.get("question_id")
        if id not in all_Q_ids:
            del item["question_id"]
            Qid2data[str(id)] = item
            all_Q_ids.append(id)
    return Qid2data



if __name__ == '__main__':
    topic_id = "19651260"

    dir_1 = "output/questions/{}/essence/questions_info".format(topic_id)
    dir_2 = "output/questions/{}/top_activity/questions_info".format(topic_id)
    save_dir = "1_concated_data/{}/".format(topic_id)
    ensure_dir(save_dir)
    all_Qid2data = dict()
    for dir in [dir_1,dir_2]:
        files_list = get_files_list(dir)
        for Q_file in files_list:
            Qid2data = get_data_by_filename(Q_file)

            all_Qid2data.update(Qid2data)
    json_write(data=all_Qid2data,filename=save_dir + "questions_id2data.json")


