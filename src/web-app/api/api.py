from flask import Flask, request, send_file
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import cv2
import numpy as np
from multiprocessing import Pool
import time
import os
import shutil
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
CORS(app, resources={r"/cbirwarna": {"origins": "http://localhost:3000"}})
CORS(app, resources={r"/cbirtexture": {"origins": "http://localhost:3000"}})
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

        if (os.path.exists('../uploads/')): #delete if there was already a folder
            shutil.rmtree('../uploads/')
        os.makedirs('../uploads/') #create folder
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

class CBIRTextureResource(Resource):
    def get(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_directory)

        reference_images_path = '../uploads/'


        reference_images = os.listdir(reference_images_path)


        reference_image_name = reference_images[0]
        reference_image_path = os.path.join(reference_images_path, reference_image_name)


        reference_image = cv2.imread(reference_image_path)
        reference_vector = cbirTexture(reference_image)

        dataset_path = '../DataSet/'
        dataset_images = os.listdir(dataset_path)

        start_time = time.time()  

        with Pool() as p:
            results = p.map(process_image_texture, [(image_name, dataset_path, reference_vector) for image_name in dataset_images])

        end_time = time.time() 

        similarity_scores = {image_name: similarity_score for image_name, similarity_score in results if similarity_score >= 0.6}

        sorted_similarity_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        response_data = [[ image_name, similarity_score * 100] for image_name, similarity_score in sorted_similarity_scores]

        execution_time = end_time - start_time

        return jsonify({'results': response_data, 'execution_time': execution_time})


class CBIRWarnaResource(Resource):
    def get(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_directory)

        reference_image_path = '../uploads/'

        reference_images = os.listdir(reference_image_path)

        reference_image_name = reference_images[0]
        reference_image_path = os.path.join(reference_image_path, reference_image_name)
        matrix_reference = img_to_matrix_RGB(reference_image_path)
        m_matrix_reference = create_submatrices(matrix_reference)
        vektor_reference = [matrix_rgb_to_hist(matrix) for matrix in m_matrix_reference]

        dataset_path = '../DataSet/'
        dataset_images = os.listdir(dataset_path)
        start_time = time.time()  

        with Pool() as p:
            results = p.map(process_image, [(image_name, dataset_path, vektor_reference) for image_name in dataset_images])
        end_time = time.time() 

        similarity_scores = {image_name: similarity_score for image_name, similarity_score in results if similarity_score >= 0.6}


        sorted_similarity_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
        response_data = [[image_name, similarity_score * 100] for image_name, similarity_score in sorted_similarity_scores]
        
        execution_time = end_time - start_time

        return jsonify({'results': response_data, 'execution_time': execution_time})




# Add resources to the API
api.add_resource(CBIRWarnaResource, '/cbirwarna')
api.add_resource(CBIRTextureResource, '/cbirtexture')
api.add_resource(ImageUploadResource, '/upload')
api.add_resource(MultiImageResource,'/multiupload')

if __name__ == '__main__':
    app.run(debug=True)


def compress_image(image, compression_scale=0.75, quality=85):
    # Mengkompresi gambar dengan skala tertentu
    compressed_image = cv2.resize(image, (0, 0), fx=compression_scale, fy=compression_scale)
    _, compressed_image_data = cv2.imencode('.jpg', compressed_image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
    return compressed_image_data

def cbirTexture(image):
    
    # Kompresi gambar sebelum diproses
    compressed_image_data = compress_image(image, compression_scale=0.7, quality=80)

    # Mendekompresi gambar
    decompressed_image = cv2.imdecode(compressed_image_data, cv2.IMREAD_COLOR)

    greyImage = cv2.cvtColor(decompressed_image, cv2.COLOR_BGR2GRAY)



    #buat matrix framework
    coOccurence = np.zeros((256, 256))

    #isi matrix coOccurence
    for i in range(greyImage.shape[0]):
        for j in range(greyImage.shape[1] - 1):
            coOccurence[greyImage[i, j], greyImage[i, j + 1]] += 1

    transposeCo = np.transpose(coOccurence)
    symMatrix = np.add(coOccurence, transposeCo)

    #cari matrix yang telah di normalisasi
    if np.sum(symMatrix) > 0:
        glcmNorm = symMatrix / np.sum(symMatrix)


    #hitung contrastnya
    contrast = calculateContrast(glcmNorm)

    #hitung Homogenity
    homogenity = calculateHomogenity(glcmNorm)

    #hitung Entropy
    entropy = CalculateEntropy(glcmNorm)

    vector = np.array([contrast, homogenity, entropy])
    return vector

def calculateHomogenity(glcmNorm):
    # homogenity = 0
    # for i in range(glcmNorm.shape[0]):
    #     for j in range(glcmNorm.shape[1]):
    #         homogenity += glcmNorm[i, j] / (1 + (i - j) ** 2)

    i, j = np.indices(glcmNorm.shape)

    # Hitung homogeneity
    homogeneity = np.sum(glcmNorm / (1. + (i - j) ** 2))

    return homogeneity

def CalculateEntropy(glcmNorm):
    # entropy = 0
    # for i in range(glcmNorm.shape[0]):
    #     for j in range(glcmNorm.shape[1]):
    #         #Agar tidak log 0
    #         if glcmNorm[i, j] > 0:
    #             entropy += glcmNorm[i, j] * np.log2(glcmNorm[i, j])
    # entropy = -entropy

    positive_glcmNorm = glcmNorm[glcmNorm > 0]

    # Hitung entropy
    entropy = -np.sum(positive_glcmNorm * np.log2(positive_glcmNorm))
    return entropy

def calculateContrast(glcmNorm):
    # contrast = 0
    # for i in range(glcmNorm.shape[0]):
    #     for j in range(glcmNorm.shape[1]):
    #         contrast += ((i - j) ** 2) * glcmNorm[i, j]

    i, j = np.indices(glcmNorm.shape)

    # Hitung contrast
    contrast = np.sum(((i - j) ** 2) * glcmNorm)
    return contrast

def cosineSim(vector1, vector2):
    dotProduct = np.dot(vector1, vector2)
    A = np.sqrt(np.sum(vector1 ** 2))
    B = np.sqrt(np.sum(vector2 ** 2))
    return dotProduct / (A * B)


def process_image(args):
    image_name, dataset_path, reference_vector = args
    image_path = os.path.join(dataset_path, image_name)
    image = cv2.imread(image_path)
    image_vector = cbirTexture(image)
    similarity_score = cosineSim(reference_vector, image_vector)
    return (image_name, similarity_score)

def img_to_matrix_RGB(image_path):
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_rgb = img_rgb.astype(np.float32)
    img_rgb = np.array(img_rgb)
    img_rgb = np.divide(img_rgb,255.0)
    return img_rgb

def matrix_rgb_to_hist(image):
    # Membagi matrix image menjadi 3 matrix representasi rred, green, blue
    r,g,b = image[:,:,0], image[:,:,1], image[:,:,2]

    # Mencari cmax, cmin, delta
    cmax = np.max(image, axis=2)
    cmin = np.min(image, axis=2)
    delta = np.subtract(cmax,cmin)
    # Inisialisasi matrix h,s,v
    h = np.zeros_like(r)
    s = np.zeros_like(r)
    v = np.zeros_like(r)

    # Membuat mask untuk r g b untuk h
    mask_r = np.logical_and(delta !=0, cmax==r)
    mask_g = np.logical_and(delta !=0, cmax==g)
    mask_b = np.logical_and(delta !=0, cmax==b)

    # Menghitung nilai h
    h[delta == 0] = 0
    h[mask_r] = 60*(((g[mask_r] -b[mask_r])/(delta[mask_r]))%6)
    h[mask_g] = 60*(((b[mask_g] -r[mask_g])/(delta[mask_g]))+2)
    h[mask_b] = 60*(((r[mask_b] -g[mask_b])/(delta[mask_b]))+4)

    # Hitung nilai s
    s[cmax == 0] = 0
    s[cmax != 0] = (delta[cmax != 0]) / (cmax[cmax != 0])

    # Hitung nilai v
    v = np.maximum.reduce([r,g,b])

    quantify(h,s,v)

    h = h.astype(np.uint8)
    s = s.astype(np.uint8)
    v = v.astype(np.uint8)

    hist_h = cv2.calcHist([h], [0], None, [8], [0, 8]).flatten()
    hist_s = cv2.calcHist([s], [0], None, [3], [0, 3]).flatten()
    hist_v = cv2.calcHist([v], [0], None, [3], [0, 3]).flatten()

    return np.concatenate((hist_h, hist_s, hist_v))

def quantify(h,s,v):
    # Quantify h
    h[h > 315] = 0
    h[np.logical_and(h > 0, h <= 25)] = 1
    h[np.logical_and(h > 25, h <= 40)] = 2
    h[np.logical_and(h > 40, h <= 120)] = 3
    h[np.logical_and(h > 120, h <= 190)] = 4
    h[np.logical_and(h > 190, h <= 270)] = 5
    h[np.logical_and(h > 270, h <= 295)] = 6
    h[np.logical_and(h > 295, h <= 315)] = 7

    # Quantify s
    s[s >= 0.7] = 2
    s[np.logical_and(s >= 0.2, s < 0.7)] = 1
    s[s < 0.2] = 0

    # Quantify v
    v[v >= 0.7] = 2
    v[np.logical_and(v >= 0.2, v < 0.7)] = 1
    v[v < 0.2] = 0


def create_submatrices(matrix):
    return [matrix[i:i+matrix.shape[0]//4, j:j+matrix.shape[1]//4]
            for i in range(0, matrix.shape[0], matrix.shape[0]//4)
            for j in range(0, matrix.shape[1], matrix.shape[1]//4)]

def cosinesim(vector_A, vector_B):
    dot_product = np.dot(vector_A, vector_B)
    norm_A = np.linalg.norm(vector_A)
    norm_B = np.linalg.norm(vector_B)
    return dot_product / (norm_A * norm_B) if norm_A * norm_B != 0 else 0

def CBIR_Warna(img_path_1, img_path_2):
    Matrix1 = img_to_matrix_RGB(img_path_1)
    Matrix2 = img_to_matrix_RGB(img_path_2)

    m_matriks = create_submatrices(Matrix1)
    n_matriks = create_submatrices(Matrix2)

    vektor1 = [matrix_rgb_to_hist(matrix) for matrix in m_matriks]
    vektor2 = [matrix_rgb_to_hist(matrix) for matrix in n_matriks]

    similarity = [cosinesim(vektor1[i], vektor2[i]) for i in range(len(vektor1))]

    result = sum(similarity) / len(similarity) if len(similarity) != 0 else 0
    return result

def process_image(args):
    image_name, dataset_path, vektor_reference = args
    image_path = os.path.join(dataset_path, image_name)
    matrix = img_to_matrix_RGB(image_path)
    n_matrix = create_submatrices(matrix)
    vektor = [matrix_rgb_to_hist(matrix) for matrix in n_matrix]

    similarity = [cosinesim(vektor_reference[i], vektor[i]) for i in range(len(vektor_reference))]
    similarity_score = sum(similarity) / len(similarity) if len(similarity) != 0 else 0

    return (image_name, similarity_score)

def process_image_texture(args):
    image_name, dataset_path, reference_vector = args
    image_path = os.path.join(dataset_path, image_name)
    image = cv2.imread(image_path)
    image_vector = cbirTexture(image)
    similarity_score = cosineSim(reference_vector, image_vector)
    return (image_name, similarity_score)
