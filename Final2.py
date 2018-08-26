# Author : Fannie Cai

# This script considers all the products a user has ordered
#
# We train a model computing the probability of reorder on the "train" data
#
# For the submission, we keep the orders that have a probability of
# reorder higher than a threshold

import random as rd
import numpy as np
import pandas as pd
import lightgbm as lgb
import json
IDIR = r"C://Users/facai/Documents/HacktheSix/"


print('loading prior')
priors = pd.read_csv(IDIR + 'order_products__prior.csv', dtype={
            'order_id': np.int32,
            'product_id': np.uint16,
            'add_to_cart_order': np.int16,
            'reordered': np.int8})

print('loading train')
train = pd.read_csv(IDIR + 'order_products__train.csv', dtype={
            'order_id': np.int32,
            'product_id': np.uint16,
            'add_to_cart_order': np.int16,
            'reordered': np.int8})

print('loading orders')
orders = pd.read_csv(IDIR + 'orders.csv', dtype={
        'order_id': np.int32,
        'user_id': np.int32,
        'eval_set': 'category',
        'order_number': np.int16,
        'order_dow': np.int8,
        'order_hour_of_day': np.int8,
        'days_since_prior_order': np.float32})

print('loading products')
products = pd.read_csv(IDIR + 'products.csv', dtype={
        'product_id': np.uint16,
        'aisle_id': np.uint8,
        'department_id': np.uint8},
        usecols=['product_id', 'aisle_id', 'department_id'])

print('priors {}: {}'.format(priors.shape, ', '.join(priors.columns)))
print('orders {}: {}'.format(orders.shape, ', '.join(orders.columns)))
print('train {}: {}'.format(train.shape, ', '.join(train.columns)))
print('products {}: {}'.format(products.shape, ', '.join(products.columns)))


#Find the next possible item for all items
print('computing the next bought items')
nextorder = pd.DataFrame()
nextorder = priors.copy()
nextorder['add_to_cart_order'] = nextorder['add_to_cart_order']-1
nextorder= pd.merge(priors,nextorder, how='left',left_on=['order_id','add_to_cart_order'],right_on=['order_id','add_to_cart_order'])
nextorder = nextorder[np.isfinite(nextorder['product_id_y'])]
nextorder['ID']=nextorder['product_id_x'].map(str)+nextorder['product_id_y'].map(str)
nextorder['I'] = 1

#Calculate the % probability of getting one product verses another
aggregate = nextorder.groupby(['product_id_x', 'product_id_y']).agg({'I': 'sum'})
# Change: groupby state_office and divide by sum
probabilityproduct = aggregate.groupby(level=0).apply(lambda x:
                                                 100 * x / float(x.sum()))
    
   

#Computing Reorder 

print('computing product f')
prods = pd.DataFrame()
prods['orders'] = priors.groupby(priors.product_id).size().astype(np.int32)
prods['reorders'] = priors['reordered'].groupby(priors.product_id).sum().astype(np.float32)
prods['reorder_rate'] = (prods.reorders / prods.orders).astype(np.float32)
print(prods)
print(products)
products = products.join(prods, on='product_id', rsuffix='_')
products.set_index('product_id', drop=False, inplace=True)
del prods



print('add order info to priors')
orders.set_index('order_id', inplace=True, drop=False)
priors = priors.join(orders, on='order_id', rsuffix='_')
priors.drop('order_id_', inplace=True, axis=1)

### user features


print('computing user f')
usr = pd.DataFrame()
usr['average_days_between_orders'] = orders.groupby('user_id')['days_since_prior_order'].mean().astype(np.float32)
usr['nb_orders'] = orders.groupby('user_id').size().astype(np.int16)

users = pd.DataFrame()
users['total_items'] = priors.groupby('user_id').size().astype(np.int16)
users['all_products'] = priors.groupby('user_id')['product_id'].apply(set)
users['total_distinct_items'] = (users.all_products.map(len)).astype(np.int16)
print(users)

users = users.join(usr)
del usr
users['average_basket'] = (users.total_items / users.nb_orders).astype(np.float32)
print('user f', users.shape)

### userXproduct features

print('compute userXproduct f ')
priors['user_product'] = priors.product_id + priors.user_id * 100000
print(priors)

# This was to slow !!
#def last_order(order_group):
#    ix = order_group.order_number.idxmax
#    return order_group.shape[0], order_group.order_id[ix],  order_group.add_to_cart_order.mean()
#userXproduct = pd.DataFrame()
#userXproduct['tmp'] = df.groupby('user_product').apply(last_order)

d= dict()
for row in priors.itertuples():
    z = row.user_product
    if z not in d:
        d[z] = (1,
                (row.order_number, row.order_id),
                row.add_to_cart_order)
    else:
        d[z] = (d[z][0] + 1,
                max(d[z][1], (row.order_number, row.order_id)),
                d[z][2] + row.add_to_cart_order)

print('to dataframe (less memory)')
userXproduct = pd.DataFrame.from_dict(d, orient='index')
del d
userXproduct.columns = ['nb_orders', 'last_order_id', 'sum_pos_in_cart']
userXproduct.nb_orders = userXproduct.nb_orders.astype(np.int16)
userXproduct.last_order_id = userXproduct.last_order_id.map(lambda x: x[1]).astype(np.int32)
userXproduct.sum_pos_in_cart = userXproduct.sum_pos_in_cart.astype(np.int16)

print('user X product f', len(userXproduct))

del priors

### train / test orders ###
print('split orders : train, test')
test_orders = orders[orders.eval_set == 'test']
train_orders = orders[orders.eval_set == 'train']

train.set_index(['order_id', 'product_id'], inplace=True, drop=False)

### build list of candidate products to reorder, with features ###

def features(selected_orders, labels_given=False):
    print('build candidate list')
    order_list = []
    product_list = []
    labels = []
    i=0
    for row in selected_orders.itertuples():
        i+=1
        if i%10000 == 0: print('order row',i)
        order_id = row.order_id
        user_id = row.user_id
        user_products = users.all_products[user_id]
        product_list += user_products
        order_list += [order_id] * len(user_products)
        if labels_given:
            labels += [(order_id, product) in train.index for product in user_products]
        
    df = pd.DataFrame({'order_id':order_list, 'product_id':product_list}, dtype=np.int32)
    labels = np.array(labels, dtype=np.int8)
    del order_list
    del product_list
    
    print('user related features')
    df['user_id'] = df.order_id.map(orders.user_id)
    df['user_total_orders'] = df.user_id.map(users.nb_orders)
    df['user_total_items'] = df.user_id.map(users.total_items)
    df['total_distinct_items'] = df.user_id.map(users.total_distinct_items)
    df['user_average_days_between_orders'] = df.user_id.map(users.average_days_between_orders)
    df['user_average_basket'] =  df.user_id.map(users.average_basket)
    
    print('order related features')
    # df['dow'] = df.order_id.map(orders.order_dow)
    df['order_hour_of_day'] = df.order_id.map(orders.order_hour_of_day)
    df['days_since_prior_order'] = df.order_id.map(orders.days_since_prior_order)
    df['days_since_ratio'] = df.days_since_prior_order / df.user_average_days_between_orders
    
    print('product related features')
    df['aisle_id'] = df.product_id.map(products.aisle_id)
    df['department_id'] = df.product_id.map(products.department_id)
    df['product_id_y']=df.product_id.map(nextorder.product_id_y)
    df['I']=df.product_id.map(nextorder.I)
    df['product_orders'] = df.product_id.map(products.orders).astype(np.int32)
    df['product_reorders'] = df.product_id.map(products.reorders)
    df['product_reorder_rate'] = df.product_id.map(products.reorder_rate)


    print('user_X_product related features')
    df['z'] = df.user_id * 100000 + df.product_id
    df.drop(['user_id'], axis=1, inplace=True)
    df['UP_orders'] = df.z.map(userXproduct.nb_orders)
    df['UP_orders_ratio'] = (df.UP_orders / df.user_total_orders).astype(np.float32)
    df['UP_last_order_id'] = df.z.map(userXproduct.last_order_id)
    df['UP_average_pos_in_cart'] = (df.z.map(userXproduct.sum_pos_in_cart) / df.UP_orders).astype(np.float32)
    df['UP_reorder_rate'] = (df.UP_orders / df.user_total_orders).astype(np.float32)
    df['UP_orders_since_last'] = df.user_total_orders - df.UP_last_order_id.map(orders.order_number)
    df['UP_delta_hour_vs_last'] = abs(df.order_hour_of_day - df.UP_last_order_id.map(orders.order_hour_of_day)).map(lambda x: min(x, 24-x)).astype(np.int8)
    #df['UP_same_dow_as_last_order'] = df.UP_last_order_id.map(orders.order_dow) == \
    #                                              df.order_id.map(orders.order_dow)

    df.drop(['UP_last_order_id', 'z'], axis=1, inplace=True)
    print(df.dtypes)
    print(df.memory_usage())
    return (df, labels)
    

df_train, labels = features(train_orders, labels_given=True)

f_to_use = ['user_total_orders', 'user_total_items', 'total_distinct_items',
       'user_average_days_between_orders', 'user_average_basket',
       'order_hour_of_day', 'days_since_prior_order', 'days_since_ratio',
       'aisle_id', 'department_id', 'product_orders', 'product_reorders',
       'product_reorder_rate', 'UP_orders', 'UP_orders_ratio',
       'UP_average_pos_in_cart', 'UP_reorder_rate', 'UP_orders_since_last',
       'UP_delta_hour_vs_last','product_id_y','I'] # 'dow', 'UP_same_dow_as_last_order'


print('formating for lgb')
d_train = lgb.Dataset(df_train[f_to_use],
                      label=labels,
                      categorical_feature=['aisle_id', 'department_id','product_id_y'])  # , 'order_hour_of_day', 'dow'
del df_train

params = {
    'task': 'train',
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'metric': {'binary_logloss'},
    'num_leaves': 96,
    'max_depth': 10,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.95,
    'bagging_freq': 5
}
ROUNDS = 100

print('light GBM train :-)')
bst = lgb.train(params, d_train, ROUNDS,feature_name=features(test_orders))
# lgb.plot_importance(bst, figsize=(9,20))
del d_train

bst.save_model('model.txt')
model_json = bst.dump_model()
with open('model.json', 'w+') as f: 
    json.dump(model_json, f, indent=4)
#
#### build candidates list for test ###
#print('loading departments')
#department = ['gravy mix','cookies','crackers','bread','pastries','bakery','pickles','jalapenoes','beer','wine','picante','goya','soda','bottle juice','canned juice','rice','dried beans','pasta','candy','snack nuts','asceptics','seafood','pasta sauce','salad dressing','condiments','dried fruit','peanut butter','jam','jelly','canned meat','canned tomatoes','canned pasta','canned beans','canned fruit','market','isotonics','vinegar','flowers','snacks','chips','popcorn','deli','deli meats','tortillas']
#userid=3
#print('load model')
#bst = lgb.Booster(model_file='model.txt') 
#
#
##with open('model.json', 'r') as f: 
##    bst = json.load(f)
#
#test_orders={'order_id':rd.choice([2774568,329954,1528013]),'user_id':userid,'eval_set':'test','order_number':rd.choice([1,4,7]),
#             'order_dow':rd.choice([3,5,2]),'order_hour_of_day':rd.choice([15,12,16]),'days_since_prior_order':rd.choice([11,33,20])}
#test_orders = pd.DataFrame(data=test_orders,index=[0])
#print(test_orders)
#
#def features(selected_orders, labels_given=False):
#    print('build candidate list')
#    order_list = []
#    product_list = []
#    labels = []
#    i=0
#    for row in selected_orders.itertuples():
#        i+=1
#        if i%10000 == 0: print('order row',i)
#        order_id = row.order_id
#        user_id = row.user_id
#        user_products = users.all_products[user_id]
#        product_list += user_products
#        order_list += [order_id] * len(user_products)
#        if labels_given:
#            labels += [(order_id, product) in train.index for product in user_products]
#        
#    df = pd.DataFrame({'order_id':order_list, 'product_id':product_list}, dtype=np.int32)
#    labels = np.array(labels, dtype=np.int8)
#    del order_list
#    del product_list
#    
#    print('user related features')
#    df['user_id'] = df.order_id.map(orders.user_id)
#    df['user_total_orders'] = df.user_id.map(users.nb_orders)
#    df['user_total_items'] = df.user_id.map(users.total_items)
#    df['total_distinct_items'] = df.user_id.map(users.total_distinct_items)
#    df['user_average_days_between_orders'] = df.user_id.map(users.average_days_between_orders)
#    df['user_average_basket'] =  df.user_id.map(users.average_basket)
#    
#    print('order related features')
#    # df['dow'] = df.order_id.map(orders.order_dow)
#    df['order_hour_of_day'] = df.order_id.map(orders.order_hour_of_day)
#    df['days_since_prior_order'] = df.order_id.map(orders.days_since_prior_order)
#    df['days_since_ratio'] = df.days_since_prior_order / df.user_average_days_between_orders
#    
#    print('product related features')
#    df['aisle_id'] = df.product_id.map(products.aisle_id)
#    df['department_id'] = df.product_id.map(products.department_id)
#    df['product_id_y']=df.product_id.map(nextorder.product_id_y)
#    df['I']=df.product_id.map(nextorder.I)
#    df['product_orders'] = df.product_id.map(products.orders).astype(np.int32)
#    df['product_reorders'] = df.product_id.map(products.reorders)
#    df['product_reorder_rate'] = df.product_id.map(products.reorder_rate)
#
#
#    print('user_X_product related features')
#    df['z'] = df.user_id * 100000 + df.product_id
#    df.drop(['user_id'], axis=1, inplace=True)
#    df['UP_orders'] = df.z.map(userXproduct.nb_orders)
#    df['UP_orders_ratio'] = (df.UP_orders / df.user_total_orders).astype(np.float32)
#    df['UP_last_order_id'] = df.z.map(userXproduct.last_order_id)
#    df['UP_average_pos_in_cart'] = (df.z.map(userXproduct.sum_pos_in_cart) / df.UP_orders).astype(np.float32)
#    df['UP_reorder_rate'] = (df.UP_orders / df.user_total_orders).astype(np.float32)
#    df['UP_orders_since_last'] = df.user_total_orders - df.UP_last_order_id.map(orders.order_number)
#    df['UP_delta_hour_vs_last'] = abs(df.order_hour_of_day - df.UP_last_order_id.map(orders.order_hour_of_day)).map(lambda x: min(x, 24-x)).astype(np.int8)
#    #df['UP_same_dow_as_last_order'] = df.UP_last_order_id.map(orders.order_dow) == \
#    #                                              df.order_id.map(orders.order_dow)
#
#    df.drop(['UP_last_order_id', 'z'], axis=1, inplace=True)
#    print(df.dtypes)
#    print(df.memory_usage())
#    return (df, labels)
#
##f_to_use = ['user_total_orders', 'user_total_items', 'total_distinct_items',
##       'user_average_days_between_orders', 'user_average_basket',
##       'order_hour_of_day', 'days_since_prior_order', 'days_since_ratio',
##       'aisle_id', 'department_id', 'product_orders', 'product_reorders',
##       'product_reorder_rate', 'UP_orders', 'UP_orders_ratio',
##       'UP_average_pos_in_cart', 'UP_reorder_rate', 'UP_orders_since_last',
##       'UP_delta_hour_vs_last','product_id_y','I'] # 'dow', 'UP_same_dow_as_last_order'
#df_test, _ = features(test_orders)
#
#print('light GBM predict')
#preds = bst.predict(df_test)
# 
#print(test_orders)
#df_test['pred'] = preds
#
#THRESHOLD = 0.22  #tuned to the crossval
#
#d = dict()
#for row in df_test.itertuples():
#    if row.pred > THRESHOLD:
#        try:
#            d[row.order_id] += ' ' + str(row.product_id)
#        except:
#            d[row.order_id] = str(row.product_id)
#
#for order in test_orders.order_id:
#    if order not in d:
#        d[order] = 'None'
#
#sub = pd.DataFrame.from_dict(d, orient='index')
#
#sub.reset_index(inplace=True)
#sub.columns = ['order_id', 'products']
#
#sub['department']=rd.choice(department)
#print(sub)
#
