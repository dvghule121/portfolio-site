import json
import os
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')


@app.route('/test')
def testpage():
    return render_template("contactme.html")


def isinlist(name, itemlist):
    a = False
    p = 0
    for n, i in enumerate(itemlist):

        if i["name"] == name:
            a = True
            p = n
            break

    return a, p


@app.route('/form')
def upload():
    return render_template("form.html")


@app.route('/details/<name>', methods=["GET", "POST"])
def details(name):
    with open("static/data/projects.json") as f:
        data = json.load(f)
        itemList = data["items"]
        project_dict = itemList[0]

        for i in itemList:
            if i["name"] == name:
                project_dict = i
                break

    return render_template("project-detail.html", name=project_dict)


@app.route('/')
def start():
    return render_template("index.html")


@app.route("/form", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["disc"]
        img = request.files["img"]
        password = request.form["pass"]
        link = request.form["link"]
        youtube = request.form["yt"]
        git = request.form["github"]

        img_1 = request.files["img-1"]
        img_2 = request.files["img-2"]
        img_3 = request.files["img-3"]

        lib_1 = request.form["lib-1"]
        lib_2 = request.form["lib-2"]
        lib_3 = request.form["lib-3"]
        lib_4 = request.form["lib-4"]
        lib_5 = request.form["lib-5"]
        lib_6 = request.form["lib-6"]

        imgs = [img_1, img_2, img_3]
        img_list = []

        for i in imgs:
            if i.filename != "":
                filename_save_ = "static/styles/images/Projects/" + i.filename
                filename_save_img = "styles/images/Projects/" + i.filename
                i.save(filename_save_)
                img_list.append(filename_save_img)

        try:

            lib_list = [lib_1, lib_2, lib_3, lib_4, lib_5, lib_6]
            filename = "styles/images/Projects/" + img.filename
            filename_save = "static/styles/images/Projects/" + img.filename

            img.save(filename_save)

            project = {"name": name,
                       "desc": description,
                       "img": filename,
                       "link": link,
                       "gitrepo": git,
                       "yt": youtube,
                       "libs": lib_list,
                       "imgs": img_list
                       }

            if password == "2006" and project["name"] != "":
                items = dict()
                with open("static/data/projects.json") as f:
                    data = dict()
                    data = json.load(f)
                    itemlist = data["items"]

                    a, p = isinlist(project["name"], itemlist)

                    if a:
                        itemlist[p] = project

                    else:
                        itemlist.append(project)

                    items["items"] = itemlist

                with open("static/data/projects.json", 'w') as f:
                    json.dump(items, f)

                return redirect("/#pr-pg")

            else:
                msg = "cant add project please Type correct password "
                return render_template("success.html", name=name, msg=msg)
        except :
            msg = "cant add project some internal error happpened"
            return render_template("success.html", name=name, msg=msg)



@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save("2.png")
        return render_template("success.html", name=f.filename)


if __name__ == '__main__':
    app.run(debug=True)
