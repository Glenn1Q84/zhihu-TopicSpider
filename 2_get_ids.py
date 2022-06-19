from utils import json_read,json_write,ensure_dir
import os
def getfiles(pathdir):
    filenames=os.listdir(pathdir)
    return filenames

def dereplication(input_list):
    out = list(set(input_list))
    return out

def dicts2ids(dicts_list):
    out_id = []
    for item in dicts_list:
        out_id.append(item["question_id"])
    return out_id
if __name__ == '__main__':
    for topic_id in ["19629961","19651260","19684571"]:
        pathdir =os.path.join("output",topic_id,"top_activity","questions_info")
        filenames = getfiles(pathdir)
        out_1 =[]
        for filename in filenames:
            dicts_list = json_read(os.path.join(pathdir,filename))
            out_ids = dicts2ids(dicts_list)
            out_1.extend(out_ids)
        print(len(out_1))
        out_2 = dereplication(out_1)
        print(len(out_2))
        save_dir = os.path.join("output",topic_id)
        ensure_dir(save_dir)
        json_write(data=out_2,filename=save_dir+"\\top_activity_ids.json")



