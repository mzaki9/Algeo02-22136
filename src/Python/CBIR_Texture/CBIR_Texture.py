import cv2
import numpy as np

def cbirTexture(image):
    # Hitung gambar grayscale dengan rumus yang diberikan

    greyImage = 0.29 * image[..., 2] + 0.587 * image[..., 1] + 0.114 * image[..., 0]

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
    homogenity = 0
    for i in range(glcmNorm.shape[0]):
        for j in range(glcmNorm.shape[1]):
            homogenity += glcmNorm[i, j] / (1 + (i - j) ** 2)
    return homogenity

def CalculateEntropy(glcmNorm):
    entropy = 0
    for i in range(glcmNorm.shape[0]):
        for j in range(glcmNorm.shape[1]):
            #Agar tidak log 0
            if glcmNorm[i, j] > 0:
                entropy += glcmNorm[i, j] * np.log2(glcmNorm[i, j])
    entropy = -entropy
    return entropy

def calculateContrast(glcmNorm):
    contrast = 0
    for i in range(glcmNorm.shape[0]):
        for j in range(glcmNorm.shape[1]):
            contrast += ((i - j) ** 2) * glcmNorm[i, j]
    return contrast

def cosineSim(vector1, vector2):
    dotProduct = np.dot(vector1, vector2)
    A = np.sqrt(np.sum(vector1 ** 2))
    B = np.sqrt(np.sum(vector2 ** 2))
<<<<<<< HEAD
    return dotProduct / (A * B)
=======
    return dotProduct / (A * B)
>>>>>>> edec8c38e967eb958f6498edefe14b6f301d20af
