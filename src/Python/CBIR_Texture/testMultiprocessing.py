import cv2
import numpy as np
import time
import os
from multiprocessing import Pool

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


def main():
    reference_image_path = 'isi REFERENCE IMAGE'
    reference_image = cv2.imread(reference_image_path)
    reference_vector = cbirTexture(reference_image)

    dataset_path = 'isi folder dataset'
    dataset_images = os.listdir(dataset_path)

    start_time = time.time()  

    with Pool() as p:
        results = p.map(process_image, [(image_name, dataset_path, reference_vector) for image_name in dataset_images])

    end_time = time.time() 

    similarity_scores = {image_name: similarity_score for image_name, similarity_score in results}


    sorted_similarity_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    for image_name, similarity_score in sorted_similarity_scores:
        print(f"Image: {image_name}, Similarity: {similarity_score * 100:.2f}%")

    print("Execution Time: {:.2f} seconds".format(end_time - start_time)) 

if __name__ == "__main__":
    main()





