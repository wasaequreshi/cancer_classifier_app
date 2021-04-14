import os
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect
import json
import nsvision as nv
import requests

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST' and request.files['file'].filename != '':
      
      f = request.files['file'].read()
      f_open = open('./temp', 'wb')
      f_open.write(f)

      image = nv.imread('./temp',resize=(50,50),normalize=True)
      image = nv.expand_dims(image,axis=0)
      
      data = json.dumps({"signature_name": "serving_default", "instances": image.tolist()})
      headers = {"content-type": "application/json"}

      json_response = requests.post('http://localhost:8502/v1/models/saved_model:predict', data=data, headers=headers)

      label = ['Malignant','Benign']
      data = int(json_response.json()['predictions'][0][0])
      data = label[data]
      os.remove('./temp')

      return render_template('uploader.html', value=data)
   else:
      return render_template('uploader.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
