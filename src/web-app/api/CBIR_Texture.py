from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flask_cors import CORS
import cv2
import os
import numpy as np
from multiprocessing import Pool
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

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


def process_image_texture(args):
    image_name, dataset_path, reference_vector = args
    image_path = os.path.join(dataset_path, image_name)
    image = cv2.imread(image_path)
    image_vector = cbirTexture(image)
    similarity_score = cosineSim(reference_vector, image_vector)
    return (image_name, similarity_score)


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
            results = p.map(process_image, [(image_name, dataset_path, reference_vector) for image_name in dataset_images])

        end_time = time.time() 

        similarity_scores = {image_name: similarity_score for image_name, similarity_score in results if similarity_score >= 0.6}

        sorted_similarity_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=False)
        response_data = [{'image_name': image_name, 'similarity_score': similarity_score * 100} for image_name, similarity_score in sorted_similarity_scores]

        execution_time = end_time - start_time

        return jsonify({'results': response_data, 'execution_time': execution_time})




api.add_resource(CBIRTextureResource, '/cbirtexture')


