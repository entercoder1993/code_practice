# 记录
bob = {'name': 'Bob Smith', 'age': 42, 'pay': 10000, 'job': 'dev'}
sue = {'name': 'Sue Jones', 'age': 42, 'pay': 30000, 'job': 'hdw'}

# 数据库
db = {}
db['bob'] = bob
db['sue'] = sue

if __name__ == '__main__':
    for key in db:
        print(key,'=>\n',db[key])