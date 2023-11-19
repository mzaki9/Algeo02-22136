import React from 'react';
import './cbir.css'
function Cbir(){
    return(
        <div className='cbir-container'>
            <h1> Konsep Program</h1>
            <p> program  menggunakan algoritma implementasi aljabar vektor  aljabar vektor yang
                 digunakan untuk menggambarkan dan menganalisis data menggunakan pendekatan CBIR
                  (Content-Based Image Retrieval). CBIR yang digunakan dapat dipisah berdasarkan paramternya, yakni
                  parameter tekstur dan warna</p>
            <h2> Parameter Warna</h2>
            <p>
Pada CBIR ini, gambar dibandingkan dengan dataset melalui konversi ke metode histogram warna, 
merepresentasikan frekuensi warna dalam ruang warna. Histogram tidak mengidentifikasi objek 
spesifik atau posisi warna dalam gambar. Pembentukan ruang warna membagi nilai citra ke range kecil, 
membentuk histogram dengan interval sebagai bin, termasuk fitur global dan blok. Hasil nya akan digunakan untuk
 menghitung HSV yang nantinya akan dibandingkan kemiripannya menggunakan cosine similarity</p>

 <h2> Parameter Tekstur</h2>
 <p>CBIR ini menggunakan co-occurrence matrix untuk membandingkan tekstur dengan pemrosesan cepat.
     Matriks ini terbentuk dari gambar I dengan n × m piksel dan parameter offset (Δx,Δy). 
     Dari matriks ini, diekstraksi 6 
     komponen tekstur: contrast, entropy,homogeneity,ASM,Energy, dan Dissimilarity. Vektor yang dihasilkan dari kelima komponen 
     ini digunakan untuk mengukur kemiripan antara gambar. Kemiripan diukur menggunakan Teorema Cosine Similarity
      dalam proses perbandingan gambar.</p>
        </div>
    );
}

export default Cbir;