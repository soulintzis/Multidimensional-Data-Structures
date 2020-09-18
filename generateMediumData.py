import random

data = dict()
usernames = list()
articles = list()

with open("usernames.txt") as f:
    imported_usernames = f.read().split('\n')
    for user in imported_usernames:              
        usernames.append(user)
    f.close()
    print('Usernames imported successfully')

with open("articles.txt") as f:
    imported_articles = f.read().split('\n')
    for article in imported_articles:              
        articles.append(article)
    f.close()
    print('Articles imported successfully')

max_number_of_articles_per_user = 10

for user in usernames: 
    num_articles = random.randint(1, max_number_of_articles_per_user)
    users_articles = []
    for i in range(num_articles):
        article_pos = random.randint(0, len(articles) - 1)
        users_articles.append(articles[article_pos])
    data[user] = users_articles

with open('dataset.txt','w') as f:
    for key, values in data.items():
        for value in values:
            f.write(key + ':' + value + '\n')
