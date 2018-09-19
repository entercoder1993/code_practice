from executive_information_system.step_2.make_db_file import loadDbase,storeDbase

db = loadDbase()
for key in db:
    print(key,'=>\n  ',db[key])
print(db['sue']['name'])