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
    Cids = []
    answers_id2data = dict()
    # QAS = dict()
    for item in data:
        Aid = item.get("comment_id")
        if Aid not in Cids:
            del item["comment_id"]
            answers_id2data[str(Aid)]=item
            Cids.append(Aid)
            # QAS.update()
    return Cids,answers_id2data





if __name__ == '__main__':
    topic_id = "19684571"
    dir_1 = "output/comments/{}/top_activity".format(topic_id)
    dir_2 = "output/comments/{}/essence".format(topic_id)
    save_dir = "1_concated_data/{}/".format(topic_id)
    ensure_dir(save_dir)

    all_Aids = []
    all_ACid_pairs = dict()
    all_Cids = []

    all_comments_id2data = dict()


    for dir in [dir_1,dir_2]:
        files_list = get_files_list(dir)
        for A_file in files_list:
            Aid = get_question_id_by_filename(A_file)
            if Aid not in all_Aids:
                Cids, comments_id2data = get_answers_by_filename(A_file)
                all_comments_id2data.update(comments_id2data)

                all_ACid_pairs[str(Aid)]=Cids
                all_Cids.extend(Cids)
                all_Aids.append(Aid)
    # print(len(all_Aids))
    # print(len(list(set(all_Aids))))
    # print(len(all_Cids))
    # print(len(list(set(all_Cids))))


    json_write(data=all_comments_id2data,filename=save_dir + "comments_id2data.json")
    json_write(data=all_ACid_pairs,filename=save_dir + "ACid_pairs.json")
