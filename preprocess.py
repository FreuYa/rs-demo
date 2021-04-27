import pandas as pd

# 年龄字段数值化
def age_map(age):
    if age >= 1 and age <= 7: return 1
    if age >= 8 and age <=16: return 2
    if age >=17 and age <= 29: return 3
    if age >= 30 and age <= 39: return 4
    if age >= 40 and age <= 49: return 5
    if age >= 50 and age <= 59: return 6
    if age >= 60: return 7

#  occupation字段数值化
def occupations_map(occupation):
    occupations_dict = {'technician': 1,
     'other': 0,
     'writer': 2,
     'executive': 3,
     'administrator': 4,
     'student': 5,
     'lawyer': 6,
     'educator': 7,
     'scientist': 8,
     'entertainment': 9,
     'programmer': 10,
     'librarian': 11,
     'homemaker': 12,
     'artist': 13,
     'engineer': 14,
     'marketing': 15,
     'none': 16,
     'healthcare': 17,
     'retired': 18,
     'salesman': 19,
     'doctor': 20}
    return occupations_dict[occupation]

# 用户信息
unames = ['user_id', 'gender', 'age', 'occupation', 'zip-code']
users = pd.read_table('./users.dat', sep='::', 
                      header=None, names=unames, engine='python')
nones = users[users['occupation'] == 'none']
users = users.drop(nones.index)
users['gender'] = users['gender'].map({'M':1, 'F':0})
users['age'] = users['age'].apply(lambda age : age_map(age))
users['occupation'] = users['occupation'].apply(lambda occupation : occupations_map(occupation))
# 处理好的数据保存，留待后续直接使用
users.to_csv('./u_result.csv')


# 评分信息
rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('./ratings.dat', sep='::', header=None, names=rnames, engine='python')

#电影信息
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('./movies.dat', sep='::', header=None, names=mnames, engine='python')

# merge
data=pd.merge(pd.merge(ratings,users),movies)


#分组
ratings_by_title = data.groupby('title').size()
#数据过滤
active_titles = ratings_by_title.index[ratings_by_title >= 250]
#数据筛选
mean_ratings = mean_ratings.loc[active_titles]


mean_ratings=data.pivot_table('rating',index=["title"],columns=["gender"],aggfunc='mean')
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)

# 评分分歧
mean_ratings['diff'] = mean_ratings['M'] - mean_ratings['F']
sorted_by_diff = mean_ratings.sort_values(by='diff')
sorted_by_diff[:10]
