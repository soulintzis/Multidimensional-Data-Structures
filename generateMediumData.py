import random

data = dict()
usernames = list()
articles = list()

num_of_users = int(input('How many users do you want to import(Type "0" to take all the users from the dataset): \n'))

with open("usernames.txt") as f:
    imported_usernames = f.read().split('\n')
    if num_of_users > len(imported_usernames) or num_of_users == 0:
        num_of_users = len(imported_usernames)
    for i, user in enumerate(imported_usernames): 
        usernames.append(user)
        if i == num_of_users:
            break
    f.close()
    print('Usernames imported successfully')

with open("articles.txt") as f:
    imported_articles = f.read().split('\n')
    for article in imported_articles:              
        articles.append(article)
    f.close()
    print('Articles imported successfully')


max_number_of_articles_per_user = int(input('Which is the maximum number of articles per user: \n'))

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
            f.write(key + '?&' + value + '\n')
