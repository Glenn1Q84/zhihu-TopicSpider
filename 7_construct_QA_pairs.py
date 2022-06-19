from utils import json_read, json_write,get_files_list,ensure_dir

def get_question_id_by_filename(filename):
    id = filename.split("/")[-1].split(".")[0]
    return id

# 根据question_id获得answers_id
def get_Aids_by_Qid(Q_filename):
    data = json_read(Q_filename)
    Aids = []
    for item in data:
        Aids.append(item.get("answer_id"))
    return Aids

def get_answers_by_filename(filename):
    data = json_read(filename)
    Aids = []
    answers_id2data = dict()
    # QAS = dict()
    for item in data:
        Aid = item.get("answer_id")
        if Aid not in Aids:
            del item["answer_id"]
            answers_id2data[str(Aid)]=item
            Aids.append(Aid)
            # QAS.update()
    return Aids,answers_id2data





if __name__ == '__main__':
    topic_id = "19651260"
    dir_1 = "output/answers/{}/top_activity".format(topic_id)
    dir_2 = "output/answers/{}/essence".format(topic_id)
    save_dir = "1_concated_data/{}/".format(topic_id)
    ensure_dir(save_dir)

    all_Qids = []
    all_QAid_pairs = dict()
    all_Aids = []

    all_answers_id2data = dict()


    for dir in [dir_1,dir_2]:
        files_list = get_files_list(dir)
        for Q_file in files_list:
            Qid = get_question_id_by_filename(Q_file)

            if Qid not in all_Qids:
                Aids, answers_id2data = get_answers_by_filename(Q_file)
                all_answers_id2data.update(answers_id2data)

                all_QAid_pairs[str(Qid)]=Aids
                all_Aids.extend(Aids)
                all_Qids.append(Qid)
    print(len(all_Aids))
    print(len(list(set(all_Aids))))

    json_write(data=all_answers_id2data,filename=save_dir + "answers_id2data.json")
    json_write(data=all_QAid_pairs,filename=save_dir + "QAid_pairs.json")
