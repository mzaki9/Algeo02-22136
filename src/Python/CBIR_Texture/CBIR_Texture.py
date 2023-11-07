import cv2
import numpy as np
import time
import os


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
    return dotProduct / (A * B)


def main():
    reference_image_path = 'ISI REFERENSI'
    reference_image = cv2.imread(reference_image_path)
    reference_vector = cbirTexture(reference_image)

    dataset_path = 'ISI PATH DATASET'
    dataset_images = os.listdir(dataset_path)

    similarity_scores = {}

    start_time = time.time()

    for image_name in dataset_images:
        image_path = os.path.join(dataset_path, image_name)
        image = cv2.imread(image_path)
        image_vector = cbirTexture(image)
        similarity_score = cosineSim(reference_vector, image_vector)
        similarity_scores[image_name] = similarity_score

    end_time = time.time()

    execution_time = end_time - start_time
    print("Execution Time: {:.2f} seconds".format(execution_time))


    sorted_similarity_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    for image_name, similarity_score in sorted_similarity_scores:
        print(f"Image: {image_name}, Similarity: {similarity_score * 100:.2f}%")

if __name__ == "__main__":
    main()

    


