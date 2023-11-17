import numpy as np
import cv2
import time
import os
from multiprocessing import Pool

def img_to_matrix_RGB(image_path):
    img = cv2.imread(image_path)
    img_rgb = img.astype(np.float32)
    img_rgb = np.divide(img_rgb,255.0)
    return img_rgb

def matrix_rgb_to_hist(image):
    # Membagi matrix image menjadi 3 matrix representasi rred, green, blue
    r,g,b = image[:,:,2], image[:,:,1], image[:,:,0]

    # Mencari cmax, cmin, delta
    cmax = np.max(image, axis=2)
    cmin = np.min(image, axis=2)
    delta = np.subtract(cmax,cmin)
    # Inisialisasi matrix h,s,v
    h = np.zeros_like(r)
    s = np.zeros_like(r)

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

    # v = cmax

    quantify(h,s,cmax)

    hist = np.zeros(14)
    hist[0] = np.count_nonzero(h == 0)
    hist[1] = np.count_nonzero(h == 1)
    hist[2] = np.count_nonzero(h == 2)
    hist[3] = np.count_nonzero(h == 3)
    hist[4] = np.count_nonzero(h == 4)
    hist[5] = np.count_nonzero(h == 5)
    hist[6] = np.count_nonzero(h == 6)
    hist[7] = np.count_nonzero(h == 7)

    hist[8] = np.count_nonzero(s == 0)
    hist[9] = np.count_nonzero(s == 1)
    hist[10] = np.count_nonzero(s == 2)

    hist[11] = np.count_nonzero(cmax == 0)
    hist[12] = np.count_nonzero(cmax == 1)
    hist[13] = np.count_nonzero(cmax == 2)

    return hist

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

def main():
    reference_image_path = 'PATH GAMBAR QUERY'
    matrix_reference = img_to_matrix_RGB(reference_image_path)
    m_matrix_reference = create_submatrices(matrix_reference)
    vektor_reference = [matrix_rgb_to_hist(matrix) for matrix in m_matrix_reference]

    dataset_path = 'PATH DATASET'
    dataset_images = os.listdir(dataset_path)

    start_time = time.time()  

    with Pool() as p:
        results = p.map(process_image, [(image_name, dataset_path, vektor_reference) for image_name in dataset_images])

    end_time = time.time() 

    similarity_scores = {image_name: similarity_score for image_name, similarity_score in results}


    sorted_similarity_scores = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=False)
    for image_name, similarity_score in sorted_similarity_scores:
        print(f"Image: {image_name}, Similarity: {similarity_score * 100:.2f}%")

    print("Execution Time: {:.2f} seconds".format(end_time - start_time)) 

if __name__ == "__main__":
    main()