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
    def post(self): #post method
        #file validty
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400
        file = request.files['file'] #the file
        if file.filename == '':
            return {'error': 'No selected file'}, 400

        if (os.path.exists('../uploads')): #delete if there was already a folder
            shutil.rmtree('../uploads')
        os.makedirs('../uploads') #create folder
        file.save('../uploads/' + file.filename) #save file

        return {'message': 'File uploaded successfully'}, 201
    
class MultiImageResource(Resource):
    def post(self):
        #file validty v1
        if 'files' not in request.files:
            return {'error': 'No file part'}, 400

        files = request.files.getlist('files') #the array of file

        if (os.path.exists('../DataSet')): #delete if there was already a folder
            shutil.rmtree('../DataSet')
        os.makedirs('../DataSet') #create folder
        for file in files:
            #validity v2
            if file.filename == '':
                return {'error': 'No selected file'}, 400

            # validity v3 (remove duplicate)
            if (not (os.path.exists('../DataSet/'+file.filename))):
                file.save('../DataSet/' + file.filename)

        return {'message': 'File uploaded successfully'}, 201 

# Add resources to the API
api.add_resource(ImageUploadResource, '/upload')
api.add_resource(MultiImageResource,'/multiupload')

if __name__ == '__main__':
    app.run(debug=True)

