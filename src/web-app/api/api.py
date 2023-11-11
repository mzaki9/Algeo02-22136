from flask import Flask, request, send_file
from flask_restful import Api, Resource
import os
import shutil
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['MAX_CONTENT_LENGTH'] = 5000 * 1024 * 1024
class ImageUploadResource(Resource):
    def post(self):
        # Check if the POST request has a file part
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400

        file = request.files['file']

        # If the user does not select a file, the browser may submit an empty part without a filename
        if file.filename == '':
            return {'error': 'No selected file'}, 400

        # Save the uploaded file to a folder\
        if (os.path.exists('../uploads')):
            shutil.rmtree('../uploads')
        os.makedirs('../uploads')
        file.save('../uploads/' + file.filename)

        return {'message': 'File uploaded successfully'}, 201
class MultiImageResource(Resource):
    def post(self):
        # Check if the POST request has a file part
        if 'files' not in request.files:
            return {'error': 'No file part'}, 400

        files = request.files.getlist('files')
        if (os.path.exists('../DataSet')):
            shutil.rmtree('../DataSet')
        os.makedirs('../DataSet')
        for file in files:
            # If the user does not select a file, the browser may submit an empty part without a filename
            if file.filename == '':
                return {'error': 'No selected file'}, 400

            # Save the uploaded file to a folder\
            if (not (os.path.exists('../DataSet/'+file.filename))):
                file.save('../DataSet/' + file.filename)

        return {'message': 'File uploaded successfully'}, 201 

# Add resources to the API
api.add_resource(ImageUploadResource, '/upload')
api.add_resource(MultiImageResource,'/multiupload')

if __name__ == '__main__':
    app.run(debug=True)

