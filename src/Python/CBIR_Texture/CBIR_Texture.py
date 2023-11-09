import cv2
import numpy as np
import time
import os

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

    greyImage = 0.29 * decompressed_image[..., 2] + 0.587 * decompressed_image[..., 1] + 0.114 * decompressed_image[..., 0]

    greyImage = greyImage.astype(np.uint8)

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
    print(contrast)
    return contrast

def cosineSim(vector1, vector2):
    dotProduct = np.dot(vector1, vector2)
    A = np.sqrt(np.sum(vector1 ** 2))
    B = np.sqrt(np.sum(vector2 ** 2))
    return dotProduct / (A * B)
<<<<<<< HEAD
=======


def main():
    path1 = 'ref 1'
    path2 = 'ref 2'
    image1 = cv2.imread(path1)
    image2 = cv2.imread(path2)
    start_time = time.time()
    vector1 = cbirTexture(image1)
    vector2 = cbirTexture(image2)
    hasil = cosineSim(vector1, vector2)
    persentase_kesamaan = (hasil)*100

    # Print persentase kesamaan
    print("Persentase Kesamaan (dalam persen):", persentase_kesamaan)
    end_time = time.time()
    print("Execution Time: {:.2f} seconds".format(end_time - start_time))  

if __name__ == "__main__":
    main()

    


>>>>>>> 7fb78aebfcf1675ba95accdec6b0febd79c74d8c
