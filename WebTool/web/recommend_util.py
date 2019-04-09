import heapq
from keras.layers import Embedding, Flatten, Multiply, Dense, Input
from keras.models import Model
import keras
keras.backend.clear_session()
import numpy as np


def get_recommend_model(num_users, num_items, latent_dim=8):
    """
    获得NCF模型定义
    :param num_users:
    :param num_items:
    :param latent_dim:
    :return:
    """
    user_input = Input(shape=(1,), dtype='int32', name='user_input')
    item_input = Input(shape=(1,), dtype='int32', name='item_input')
    MF_Embedding_User = Embedding(input_dim=num_users, output_dim=latent_dim, name='user_embedding', input_length=1)
    MF_Embedding_Item = Embedding(input_dim=num_items, output_dim=latent_dim, name='item_embedding', input_length=1)
    user_latent = Flatten()(MF_Embedding_User(user_input))
    item_latent = Flatten()(MF_Embedding_Item(item_input))
    predict_vector = Multiply()([user_latent, item_latent])
    prediction = Dense(1, activation='sigmoid', name='prediction')(predict_vector)

    model = Model(inputs=[user_input, item_input], outputs=prediction)

    return model


def load_dict_map(file_name, is_inverse=False):
    """

    :param file_name:
    :param is_inverse: 判断key是真实id，还是训练id
    :return: 训练id与真实id的字典，key为训练id，value为真实id(is_inverse参数为False时)
    """
    dict_map = {}
    with open(file_name, encoding='UTF-8') as f:
        line = f.readline()
        while line != None and line != '':
            info_list = line.split('\t')
            if is_inverse:
                dict_map[info_list[1].strip('\n')] = info_list[0]
            else:
                dict_map[info_list[0]] = info_list[1].strip('\n')
            line = f.readline()
    return dict_map


def load_negative_file(filename):
    """
    加载负样本文件
    :param self:
    :param filename:
    :return: 返回一个列表list，每一个位置为i的元素也是个列表，包含了stu_id为i的学生未曾有过交互的book
    """
    negativeList = []
    with open(filename, "r") as f:
        line = f.readline()
        while line != None and line != "":
            arr = line.split("\t")
            negatives = []
            for x in arr[1:]:
                negatives.append(int(x))
            negativeList.append(negatives)
            line = f.readline()
    return negativeList


stu_dict = load_dict_map('./web/recommend_data/B5_stuDic.txt')
print([(k, v) for k, v in stu_dict.items()][0:5])
stu_inverse_dict = load_dict_map('./web/recommend_data/B5_stuDic.txt', is_inverse=True)
print([(k, v) for k, v in stu_inverse_dict.items()][0:5])
book_dict = load_dict_map('./web/recommend_data/B5_bookDic.txt')
negativeList = load_negative_file('./web/recommend_data/B5.negative')

book_dict2 = {}
with open('./web/recommend_data/B5.txt', encoding='UTF-8') as f:
    for line in f:
        if line == '':
            continue
        book_loc = line.split(';')[2]
        if not (book_loc in book_dict2):
            book_dict2[book_loc] = 1
        else:
            book_dict2[book_loc] += 1


def get_hot_book(topK):
    """
    获取借阅量前topK的书籍列表
    :param topK:
    :return:
    """
    global book_dict2
    print('===================util method==================', topK)
    klarget_loc_list = heapq.nlargest(topK, book_dict2.keys(), key=book_dict2.get)
    klarget_count_list = [book_dict2[loc] for loc in klarget_loc_list]
    return klarget_loc_list, klarget_count_list


# topk_loc_list, topk_count_list = get_hot_book(20)


def get_recommend_list(idr):
    """
    针对一个用户id，返回推荐列表
    :param idx:
    :return:
    """
    global negativeList, model
    items = negativeList[idr]
    print(idr)
    print("22222222222222222222", len(items))
    # Get prediction scores
    map_item_score = {}
    users = np.full(len(items), idr, dtype='int32').reshape(-1, 1)
    print(users.shape)
    # 得到所有这99个item的预估分
    print(model.summary())
    print("=================朱大竞==============", model.predict([np.array([1]), np.array([1])], batch_size=1))
    predictions = model.predict([users, np.array(items).reshape(-1, 1)], batch_size=199)
    for i in range(len(items)):
        item = items[i]
        map_item_score[item] = predictions[i]

    # Evaluate top rank list
    ranklist = heapq.nlargest(5, map_item_score, key=map_item_score.get)
    return ranklist


if __name__ == '__main__':
    # 测试代码
    pass
    # stu_dict = load_dict_map('./recommend_data/B5_stuDic.txt')
    # print(stu_dict['4432'])
    # model = get_recommend_model(11767, 20089)
    # model.load_weights('./trained_model/test2.h5')
    # print(model.predict([np.array([1]), np.array([1])], batch_size=1))

# 注意: 在模块不当主模块运行的时候，当前工作路径与当主模块运行时的工作路径不一定一样
# print(os.getcwd())


model = get_recommend_model(11767, 20089)
model.load_weights('./web/trained_model/test2.h5')
# 测试代码
print("=================朱大竞==============", model.predict([np.array([1]), np.array([1])], batch_size=1))

