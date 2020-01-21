import json

# json_data = {}

# with open('Datasets/reviews.json', 'r',  encoding='utf-8') as f:
#     json_data = f.read()

try:
    with open('Datasets/reviews.json', 'r',  encoding='utf-8') as json_file:
        temp = json_file.read()
        obj = json.loads(temp)
    json_file.close()
except FileNotFoundError:
    print('Something went wrong!')

for item in obj.items():
    for x in item:
        print(x)
