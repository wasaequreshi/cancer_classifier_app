import os
import pickle
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect
#from flask_frozen import Freezer
import json
from matplotlib.image import imread
import cv2
import numpy
import nsvision as nv
import requests
app = Flask(__name__)
#freezer = Freezer(app)

Bootstrap(app)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST' and request.files['file'].filename != '':
      
      SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
      file_path = os.path.join(SITE_ROOT, "model", "model.pickle")
      classifier = pickle.load(open( file_path, "rb" ))
      f = request.files['file'].read()
      f_open = open('./temp', 'wb')
      f_open.write(f)
    #   data = classifier.predict(f)
      #data = 0
      #image = cv2.imdecode(numpy.fromstring(f.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)

      #image = cv2.imread(temp, cv2.IMREAD_COLOR)
      #image_resized = cv2.resize(image, (50, 50), interpolation=cv2.INTER_LINEAR)
      #image_resized = [[image_resized]]
      image = nv.imread('./temp',resize=(50,50),normalize=True)
      #image = nv.imread('./temp')
      image = nv.expand_dims(image,axis=0)
      data = json.dumps({"signature_name": "serving_default", "instances": image.tolist()})
      headers = {"content-type": "application/json"}

      json_response = requests.post('http://localhost:8502/v1/models/saved_model:predict', data=data, headers=headers)
      print(json_response)
      data = int(json_response.json()['predictions'][0][0])
      print(json_response.json()['predictions'][0]) 
      label = ['Malignant','Benign']
      data = label[data]
      os.remove('./temp')
      return render_template('uploader.html', value=data)
   else:
      return render_template('uploader.html')

if __name__ == '__main__':
    app.run(debug=True)
    #freezer.freeze()
