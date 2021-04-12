import os
import pickle
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request, redirect
from flask_frozen import Freezer

app = Flask(__name__)
freezer = Freezer(app)

Bootstrap(app)
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST' and request.files['file'] != None:
      
      SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
      file_path = os.path.join(SITE_ROOT, "model", "model.pickle")
      classifier = pickle.load(open( file_path, "rb" ))
      f = request.files['file']
    #   data = classifier.predict(f)
      data = 0
      if data == 0:
          data = "Malignant"
      else:
          data = "Benign"
      return render_template('uploader.html', value=data)
   else:
      return render_template('uploader.html')

if __name__ == '__main__':
    # app.run(debug=True)
    freezer.freeze()