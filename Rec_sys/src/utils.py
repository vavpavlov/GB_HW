def prefilter_items(data_train):
    # Оставим только 5000 самых популярных товаров
    popularity = data_train.groupby('item_id')['quantity'].sum().reset_index()
    popularity.rename(columns={'quantity': 'n_sold'}, inplace=True)
    top_5000 = popularity.sort_values('n_sold', ascending=False).head(5000).item_id.tolist()
    #добавим, чтобы не потерять юзеров
    data_train.loc[~data_train['item_id'].isin(top_5000), 'item_id'] = 999999 
    
    
    
    # Уберем самые популярные 
    
    # Уберем самые непопулряные 
    
    # Уберем товары, которые не продавались за последние 12 месяцев
    
    # Уберем не интересные для рекоммендаций категории (department)
    
    # Уберем слишком дешевые товары (на них не заработаем). 1 покупка из рассылок стоит 60 руб. 
    
    # Уберем слишком дорогие товарыs
    
    # ...
    
    return data_train
    

def postfilter_items(data):
    pass


def get_similar_items_recommendation(user, model, item, N=5):
    '''Рекомендуем товары, похожие на топ-N купленных юзером товаров'''
    res = [id_to_itemid[rec[0]] for rec in model.similar_items(itemid_to_id[item], N=N)]
    return res
    
"""


user_rec = """

def get_similar_users_recommendation(user, model, sparse_user_item, item, N=5):
    '''Рекомендуем топ-N товаров'''
    res = [id_to_itemid[rec[0]] for rec in 
                    model.recommend(userid=userid_to_id[user], 
                                    user_items=sparse_user_item,   # на вход user-item matrix
                                    N=N, 
                                    filter_already_liked_items=False, 
                                    filter_items=[itemid_to_id[item]],  
                                    recalculate_user=True)]  
    return res
