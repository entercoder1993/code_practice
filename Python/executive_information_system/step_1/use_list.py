bob = ['Bob Smith',42,30000,'software']
sue = ['Sue Jones',45,40000,'hardware']

'''
使用List
'''

# 使用索引获取数据
print(bob[0],sue[2])

# 通过字段获取数据
print(bob[0].split()[-1])
sue[2] *= 1.25
print(sue)
print("-------------------------------------------")

'''
数据库列表
'''

# 列表people就是我们当前使用的数据库
people = [bob,sue]
for person in people:
    print(person)

# 列表解析式
pays = [person[2] for person in people]
print(pays)

# map
pays = map((lambda x:x[2]),people)
print(list(pays))

# 生成器表达式
print(sum(person[2] for person in people))

# 向数据库添加记录，使用append和extend
people.append(['Tom',50,0,None])
print(len(people))
print(people[-1][0])
print("-------------------------------------------")

'''
Field标签
'''

# 字段名和字段值关联，这样可读性更好
NAME,AGE,PAY = range(3)
print(bob[NAME])
print(bob[AGE])

# 使用元祖解决关联性随记录结构改变而需要进行维护的问题
bob = [['name','Bob Smith'],['age',42],['pay',10000]]
sue = [['name','Sue Jones'],['age',52],['pay',20000]]
people = [bob,sue]
print(people)

# 但仍需通过为止获取字段
for person in people:
    print(person[0][1],person[2][1])
peoples = [person[0][1] for person in people]
print(peoples)

# 可以通过字段的名字来获取我们想要的(通过循环使用元祖赋值来拆开键值对
for person in people:
    for (name,value) in person:
        if name == 'name':
            print(value)

# 创建函数获取值

def field(record,label):
    for (fname,fvalue) in record:
        if fname == label:
            return fvalue

value = field(sue,'pay')
print(value)

for rec in people:
    print(field(rec,'age'))

print("-------------------------------------------")

'''
使用字典
'''

# 使用字典关联属性和值
bob = {'name':'Bob Smith','age':42,'pay':10000,'job':'dev'}
sue = {'name':'Sue Jones','age':54,'pay':20000,'job':'hdv'}
print(bob['name'],sue['age'])
print(bob['name'].split()[-1])
sue['pay'] *= 1.10
print(sue['pay'])

# 其他建立字典的方法
bod = dict(name='Bob Smith',age=42,pay=30000,job='dev')
sue = dict(name='Sue Jones',age=54,pay=40000,job='hdw')
print(bob)

# 填字典(字典的键是伪随机排列的)
sue = {}
sue['name'] = 'Sue Jones'
sue['age'] = 42
sue['pay'] = 30000
sue['job'] = 'hdw'
print(sue)

# 使用zip函数
names = ['name','age','pay','job']
values = ['Bob Smith',42,20000,'dev']
l1 = list(zip(names,values))
bob = dict(zip(names,values))
print(bob)

# 通过一个键序列和所致键的可选初始值创建字典(便于初始化空字典)
fields = ('name','age','job','pay')
record = dict.fromkeys(fields,'?')
print(record)

# 字典列表
people = [bob,sue]
for person in people:
    print(person['name'],person['pay'],sep=', ')

for person in people:
    if person['name'] == 'Sue Jones':
        print(person['pay'])

# 列表解析和map
names = [person['name'] for person in people]
print(names)
# 生成式
print(list(map((lambda x:x['name']),people)))
x = sum(person['pay'] for person in people)
print(x)

print("-------------------------------------------")

'''
嵌套结构

Python的所有符合数据结构可以任意层次低互相嵌套，因此可以轻易地构造相当复杂的信息结构，只需要按照对象的语法输入。
'''
bob2 = {
    'name':{'first':'Bob','last':'Smith'},
    'age':42,
    'job':['software','writeing'],
    'pay':(40000,50000)
}
print(bob2['name']['last'])
print(bob2['pay'][1])
for job in bob2['job']:print(job)
bob2['job'].append('network')

# 字典的字典
# 外层的字典是数据库，内层嵌套的字典是数据库中的记录，基于字典的数据可以使用符号建来存储和获取记录
db = {}
db['sue'] = sue
db['bob'] = bob
print(db['sue']['name'])
db['bob']['pay'] = 5000 # 存储
print(db['bob']['pay'])  # 获取
import pprint
pprint.pprint(db)

# 使用键索引访问所有对象
for key in db:
    print(db[key]['name'].split()[-1])
    db[key]['pay'] *= 1.10
    print(db[key]['pay'])

# 使用迭代字典的集合访问记录
for record in db.values():
    print(record['pay'])
x = [rec['name'] for rec in db.values()]
print(x)

# 添加记录
db['tom'] = dict(name='Tom',age=50,job=None,pay=0)
print(db)
print(list(db.keys()))
# 类似SQL进行查询
print([rec['name'] for rec in db.values() if rec['age'] >=45])