import firebase_admin

cred_obj = firebase_admin.credentials.Certificate('F:/hclproject/pscproj/static/hcl-project-1-service-account.json')
default_app = firebase_admin.initialize_app(cred_obj,{'databaseURL':'https://hcl-project-1-572c9-default-rtdb.firebaseio.com/'})


from firebase_admin import db

ref = db.reference("/")

import json
with open("movies-data.json","r") as f:
    file_contents = json.load(f)
    print('file-content',file_contents)
ref.set(file_contents)