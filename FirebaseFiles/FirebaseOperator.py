import firebase_admin
import os
from firebase_admin import db
import json
import datetime
from FirebaseFiles import pyrebaseApp

imgoperator = pyrebaseApp.FBstorage()
databaseURL = "https://dynocodes-default-rtdb.firebaseio.com"
cred_obj = firebase_admin.credentials.Certificate(
    'FirebaseFiles/data/dynocodes-firebase-adminsdk-rwgjg-f6f4e8cfae.json')

default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': databaseURL
})
# default_app = firebase_admin.initialize_app()

with open("FirebaseFiles/data/projects.json", "r") as f:
    file_contents = json.load(f)


def isinlist(name, itemlist):
    a = False
    p = 0
    for n, i in enumerate(itemlist):

        if i["name"] == name:
            a = True
            p = n
            break

    return a, p


class FirebaseOperatorClass:
    def __init__(self):
        try:
            self.ref = db.reference("/items")
            self.projects = self.ref.get()
            self.Data = self.projects


        except:
            self.Data = file_contents["items"]


    def loadData(self):
        return self.Data

    def addProject(self, project):
        itemlist = self.projects
        if itemlist != None:
            a, p = isinlist(project["name"], itemlist)
            if a:
                itemlist.pop(p)
                FirebaseOperatorClass.remove_project(self,p)
                itemlist.insert(p, project)

            else:
                itemlist.append(project)

        else:
            itemlist = []
            itemlist.append(project)

        self.ref.set(itemlist)
        self.projects = self.ref.get()

        with open("FirebaseFiles/data/projects.json", "w") as f:
            json.dump({"items": itemlist}, f)

    def remove_project(self, index):
        print("index", index)
        if index != None:
            index_to_remove = int(index)
            itemlist = self.projects

            imgs_list = itemlist[index_to_remove]["imgs_names"]
            for i in imgs_list:
                imgoperator.delete_img(i)
            imgoperator.delete_img(itemlist[index_to_remove]["img_name"])

            itemlist.pop(index_to_remove)
            print("mission succesful", itemlist)
            try:
                self.ref.set(itemlist)
                self.projects = self.ref.get()
            except:
                with open("FirebaseFiles/data/projects.json", "w") as f:
                    json.dump({"items": itemlist}, f)
            return 1

            # except Exception as e:
            #     print("failed", e)
            #     return None

        else:
            return None

    def addmsg(self,msg):
        self.ref = db.reference("/")
        self.ref.child("msgs").push(msg)

    def refresh(self):
        self.ref = db.reference("/")
        self.ref.child("items").set(file_contents["items"])
        self.ref.child("msgs").push("")





if __name__ == "__main__":
    pass
