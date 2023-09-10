import json
import os

from flask import Flask, request, render_template, redirect, jsonify

import FirebaseFiles.FirebaseOperator
import FirebaseFiles.FirebaseOperator as fo
import FirebaseFiles.pyrebaseApp as imgsaver
import SpeechToText

try:
    Operator = fo.FirebaseOperatorClass()

except:
    pass

app = Flask(__name__)


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    # Get the bytearray of speech data from the request
    audio_bytes = request.get_data()

    # Convert the bytearray to text using the bytearray_to_text function
    text = SpeechToText.bytearray_to_text(audio_bytes)

    # Return the text as a JSON response
    return jsonify({'text': text})


@app.route('/cv')
def mycv():
    return render_template('cv.html')


@app.route('/share/<p_b>/<blog>')
def share(p_b, blog):
    title = blog
    summary = 'Read this amazing blog by Dynocodes \n' + 'https://dynocodes.herokuapp.com/test/' + blog
    link = f'https://dynocodes.herokuapp.com/{p_b}/{blog}'
    all_wrapped = {"summary": summary, "link": link, "title": title}
    return render_template('share.html', cont=all_wrapped)


@app.route('/form')
def upload():
    return render_template("form.html")


@app.route('/form-b')
def upload_():
    return render_template("blogwriting.html")


@app.route('/blogs/<name>')
def test(name):
    data = Operator.load_blog()
    itemList = data[name]
    print(data)

    return render_template("blog.html", name=itemList)


@app.route('/projects/<name>', methods=["GET", "POST"])
def details(name):
    data = Operator.loadData()
    print(data)
    itemList = data
    print(data)

    for i in itemList:
        if i["name"] == name:
            project_dict = i
            break

    return render_template("project-detail.html", name=project_dict)


@app.route('/')
def start():
    data = FirebaseFiles.FirebaseOperator.FirebaseOperatorClass().loadData()
    blogs = Operator.load_blog()
    blogs_list = list()
    for i in blogs:
        blogs_list.append(blogs[i])

    print(blogs_list)
    if data != None:
        return render_template("index.html", data=data, blog=blogs_list, length=len(data))
    else:
        return render_template("index.html", data=data, length=0, this="Project name")


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
                imgtoFB = imgsaver.FBstorage()
                url = imgtoFB.saveImage(imgs[i], img_name)
                img_list.append(url)
                imgs_names.append(img_name)

            else:
                img_list.append("")
                imgs_names.append("")

        lib_list = [lib_1, lib_2, lib_3, lib_4, lib_5, lib_6]

        imgtoFB = imgsaver.FBstorage()
        url_profile = imgtoFB.saveImage(img, img.filename)

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

    return render_template("remove_project.html", name_list=name_list, len=len(name_list))


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


@app.route("/form-b", methods=["GET", "POST"])
def addBlog():
    if request.method == "POST":
        name = request.form["heading"]
        main_disk = request.form["main-disc"]

        head_1 = request.form["sub-1-name"]
        disc_1 = request.form["sub-1-disc"]

        head_2 = request.form["sub-2-name"]
        disc_2 = request.form["sub-2-disc"]

        head_3 = request.form["sub-3-name"]
        disc_3 = request.form["sub-3-disc"]

        head_4 = request.form["sub-4-name"]
        disc_4 = request.form["sub-4-disc"]

        lib_1 = request.form["lib-1"]
        lib_2 = request.form["lib-2"]
        lib_3 = request.form["lib-3"]
        lib_4 = request.form["lib-4"]

        img = request.form["img-link"]

        password = request.form["pass"]

        blog = {
            "name": name,
            "main_disk": main_disk,
            "img": img,
            "sub_topics": [
                {"name": head_1,
                 "para": disc_1},
                {"name": head_2,
                 "para": disc_2},
                {"name": head_3,
                 "para": disc_3},
                {"name": head_4,
                 "para": disc_4}

            ],
            "topics": [lib_1, lib_2, lib_3, lib_4]
        }

        if password == "2006":
            Operator.add_blog(blog)
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

        msg = {"name": name,
               "email": email,
               "msg": msgs}

        try:
            Operator.addmsg(msg)
            return render_template("success.html", name=name, msg="Thank you for your valuable responce")

        except Exception as e:
            msg = "cant add project  " + e
            return render_template("success.html", name=name, msg=msg)




# # Your schedule data
# with open("schedule.json", "r") as f:
#     scheduleData = json.load(f)
scheduleData = Operator.load_schedule()
scheduleData = json.loads(scheduleData)

# Generate schedule data with combined empty blocks
combinedScheduleData = []
currentEmptyBlock = None

for hour_key, event in scheduleData.items():
    # Convert the hour key to a string to ensure consistency
    hour_str = str(hour_key)

    if currentEmptyBlock and hour_str != currentEmptyBlock.get('end_time'):
        # Add the combined empty block to the schedule
        combinedScheduleData.append(currentEmptyBlock)
        currentEmptyBlock = None

    if hour_str in scheduleData:
        # Add the scheduled event to the schedule
        combinedScheduleData.append(scheduleData[hour_str])
    else:
        if not currentEmptyBlock:
            # Start a new empty block
            currentEmptyBlock = {
                'title': 'Free Time',
                'start_time': hour_str,
                'end_time': None,
                'tasks': []
            }

# If there's an empty block at the end of the day, add it
if currentEmptyBlock:
    combinedScheduleData.append(currentEmptyBlock)

@app.route('/schedule')
def schedule():
    return render_template('schedule.html', scheduleData=combinedScheduleData)

@app.route('/schedule/json')
def schedule_json():
    # Calculate and add the free blocks
    with open("static/data/schedule.json", "r") as f :
        schedule_data = json.loads(f)

    return jsonify(schedule_data)


if __name__ == '__main__':
    app.run(debug=True, port=8000)
