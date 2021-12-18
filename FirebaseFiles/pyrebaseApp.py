import pyrebase
import os

config = {
  "apiKey": "AIzaSyBXisUZIAW4WBQLosfWX_LBAVhxFNcAIoM",
  "authDomain": "dynocodes.firebaseapp.com",
  "databaseURL": "https://dynocodes-default-rtdb.firebaseio.com",
  "projectId": "dynocodes",
  "storageBucket": "dynocodes.appspot.com",
  "messagingSenderId": "286512270586",
  "appId": "1:286512270586:web:5597d2b532993a8f2c8d43",
  "serviceAccount": "FirebaseFiles/data/dynocodes-firebase-adminsdk-rwgjg-f6f4e8cfae.json"

}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
auth = firebase.auth()
email = "dvghule121@gmail.com"
password = "Lo17800350"





class FBstorage:
  def __init__(self):
    pass

  def saveImage(self,img,name):
    # Upload Image
    val = storage.child("images").child(name).put(img)
    print(val)

    # # Get url of image
    user = auth.sign_in_with_email_and_password(email, password)
    url = storage.child("images").child(name).get_url(user['idToken'])
    print(url)

    return url
  def delete_img(self,img_name):
    user = auth.sign_in_with_email_and_password(email, password)
    if img_name != "":
      try:
        val = storage.delete("images/"+img_name)
      except:
        return -1






