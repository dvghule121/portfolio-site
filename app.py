import json
import os
import time

from flask import Flask, request, render_template, redirect
import FirebaseFiles.FirebaseOperator as fo
import FirebaseFiles.pyrebaseApp as imgsaver


try:
    Operator = fo.FirebaseOperatorClass()

except:
    pass

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')


@app.route('/test')
def testpage():
    pass


@app.route('/form')
def upload():
    return render_template("form.html")


@app.route('/details/<name>', methods=["GET", "POST"])
def details(name):
    data = Operator.loadData()
    itemList = data
    print(data)

    for i in itemList:
        if i["name"] == name:
            project_dict = i
            break

    return render_template("project-detail.html", name=project_dict)


@app.route('/')
def start():
    data = Operator.loadData()
    print(data)
    if data != None:
        return render_template("index.html", data=data, length=len(data))
    else:
        return render_template("index.html", data=data,length=0, this="Project name")


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
        imgs_names = []
        img_list = []

        for i in range(3):
            if imgs[i].filename != "":
                img_name = imgs[i].filename
                filename_save_ = "static/styles/images/Projects/" + imgs[i].filename
                imgs[i].save(filename_save_)
                imgtoFB = imgsaver.FBstorage()
                url = imgtoFB.saveImage(filename_save_, img_name)
                time.sleep(4)
                os.remove(filename_save_)
                print('removed')

                img_list.append(url)
                imgs_names.append(img_name)
            else:
                img_list.append("")
                imgs_names.append("")

        lib_list = [lib_1, lib_2, lib_3, lib_4, lib_5, lib_6]

        filename_save = "static/styles/images/Projects/" + img.filename
        img.save(filename_save)
        imgtoFB = imgsaver.FBstorage()
        url_profile = imgtoFB.saveImage(filename_save, img.filename)
        time.sleep(4)
        os.remove(filename_save)

        project = {"name": name,
                   "desc": description,
                   "img_name": img.filename,
                   "img": url_profile,
                   "link": link,
                   "gitrepo": git,
                   "yt": youtube,
                   "libs": lib_list,
                   "imgs": img_list,
                   "imgs_names": imgs_names
                   }

        if password == "2006" and project["name"] != "":
            Operator.addProject(project)
            return redirect("/#pr-pg")

        else:
            msg = "cant add project please Type correct password "
            return render_template("success.html", name=name, msg=msg)

        # msg = "cant add project some internal error happpened"
        # return render_template("success.html", name=name, msg=msg)


@app.route("/remove-project")
def rem_project_page():
    data = Operator.loadData()
    itemList = data
    project_dict = itemList[0]
    name_list = []

    for i in itemList:
        pr_name = i["name"]
        name_list.append(pr_name)

    return render_template("remove_project.html", name_list=name_list, len= len(name_list))


@app.route("/remove-project", methods=["GET", "POST"])
def rem_project():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["pass"]
        print(name)

        if password == "2006":
            Operator.remove_project(name)
            return redirect("/#pr-pg")

        else:
            msg = "cant add project please Type correct password "
            return render_template("success.html", name=name, msg=msg)

        # msg = "cant add project some internal error happpened"
        # return render_template("success.html", name=name, msg=msg)


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save("2.png")
        return render_template("success.html", name=f.filename)
@app.route('/msg', methods=['POST'])
def msgin():
    if request.method == 'POST':
        name = request.form["fname"]
        email = request.form["email"]
        msgs = request.form["subject"]

        msg = {"name":name,
               "email":email,
               "msg":msgs}

        try:
            Operator.addmsg(msg)
            return render_template("success.html", name=name, msg="Thank you for your valuable responce")

        except Exception as e:
            msg = "cant add project  " + e
            return render_template("success.html", name=name, msg=msg)


if __name__ == '__main__':
    app.run(debug=False)

