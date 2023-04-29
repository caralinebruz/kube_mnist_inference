#!/usr/bin/env python3

"""Simple Python Flask Application"""
from flask import Flask, request
import os
import model as model

UPLOAD_FOLDER = os.environ.get('UPLOAD_DIR')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

port = int(os.getenv("PORT"))



# uses https://stackoverflow.com/questions/44926465/upload-image-in-flask

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        file1.save(path)

        # model.get_model()
        infer = model.inference(path)

        return infer

        return 'ok'
    return '''
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file1">
      <input type="submit">
    </form>
    '''



#@app.route('/')
# def hello_world():

#     model.get_model()

#     return 'Hello NYU Cloud and Machine Learning Students! I am running on port ' + str(port)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)

