from executive_information_system.step_2.make_db_file import loadDbase,storeDbase

db = loadDbase()
db['sue']['pay'] *= 1.10
print(db['bob']['pay'])
print('=======')
db['Tom']['name'] = 'tom tom'
storeDbase(db)