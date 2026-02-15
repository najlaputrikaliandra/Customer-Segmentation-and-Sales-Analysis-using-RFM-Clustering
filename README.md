<h1 align="center">Segmenlytics: Customer Segmentation & Marketing Intelligence</h1>

Ini adalah proyek machine learning capstone project Asah 2025 dari tim capstone A25-CS310 dengan usecase Customer Segmentation for Personalized Retail Marketing.
Didalam repositori ini, anda dapat menjelajahi seluruh proses analisis berdasarkan daftar isi yang tersedia.

---

## Table of Contents
- [About the Project](#about-the-project)
- [How to Use](#how-to-use)
- [Analysis Method](#analysis-method)
- [Customer Segments](#customer-segments)
- [Project Deliverables](#project-deliverables)
- [Results & Insights](#results--insights)

---

## About the Project
Retail businesses perlu memahami perilaku pelanggan secara mendalam untuk meningkatkan efektivitas strategi pemasaran, retensi, dan customer lifetime value.  
Untuk menjawab kebutuhan tersebut, proyek ini mengembangkan analisis **RFM (Recency, Frequency, Monetary)** yang dikombinasikan dengan **K-Means Clustering** untuk memetakan pola transaksi pelanggan secara objektif.

Pendekatan ini membantu menjawab beberapa pertanyaan penting:

- Bagaimana perilaku pelanggan direpresentasikan melalui fitur RFM?  
- Berapa jumlah klaster optimal untuk segmentasi pelanggan?  
- Strategi pemasaran apa yang relevan untuk setiap segmen?

Proyek ini berfokus pada pembuatan notebook analisis lengkap, visualisasi mendalam, dan dashboard yang menampilkan segmentasi serta insight yang dapat langsung diterapkan oleh bisnis ritel.

---

## How to Use

1. Buka notebook analisis RFM.
2. Lakukan proses data cleaning (disesuaikan dengan dataset).
3. Jalankan seluruh sel untuk:
   - Menghitung nilai RFM
   - Melakukan clustering dengan K-Means
     
4. Untuk melihat hasil dalam bentuk dashboard visualisasi:
   - Pastikan Streamlit sudah terinstall, jika belum jalankan perintah:
     ```bash
     pip install streamlit
   - Pastikan library Plotly sudah terinstall. Jika belum, jalankan perintah:
     ```bash
     pip install plotly
   - Masuk ke folder dashboard.
   - Jalankan perintah:
     ```bash
     streamlit run app.py

5. Dashboard menampilkan:
   - Hasil segmentasi pelanggan
   - Distribusi RFM
   - Customer persona tiap segmen
   - Insight pemasaran

6. Gunakan insight yang dihasilkan untuk mendukung strategi bisnis
   dan pengambilan keputusan.

---

## Analysis Method

### 1. RFM Analysis

- **Recency** — kapan terakhir kali pelanggan bertransaksi  
- **Frequency** — seberapa sering mereka bertransaksi  
- **Monetary** — total nilai transaksi  

RFM memberikan gambaran yang kuat mengenai nilai dan perilaku pelanggan.

### 2. K-Means Clustering

K-Means digunakan untuk mengelompokkan pelanggan berdasarkan skor RFM.  
Penentuan jumlah klaster menggunakan:

- Elbow Method  
- Silhouette Score  

Pendekatan ini memungkinkan segmentasi pelanggan yang objektif dan mudah dijelaskan secara bisnis.

---

## Customer Segments

Proyek ini menghasilkan empat segmen utama:

### **1. Active Customers**  
Pelanggan yang masih aktif dan cukup sering bertransaksi.

### **2. At-Risk Customers**  
Pelanggan yang sebelumnya aktif namun kini jarang membeli.

### **3. Active Big Spenders**  
Pelanggan aktif dengan nilai transaksi tinggi.

### **4. At-Risk Big Spenders**  
Pelanggan bernilai tinggi namun mulai jarang bertransaksi.

Segmentasi ini membantu bisnis memprioritaskan budget pemasaran dengan lebih efektif.

---

## Project Deliverables

Berikut adalah deliverables yang dihasilkan dari implementasi proyek ini:

- [Notebook Analisis RFM + Clustering](https://colab.research.google.com/drive/1hcAufmGZjffsnw7O5kDjvSGYrFDg-Gum?usp=sharing)
- [Dashboard Visualisasi Segmentasi](https://drive.google.com/drive/folders/16u09Rj4sNo9O1-HIu-IY1caBYbNTozIo?usp=sharing)
- Insight dan Rekomendasi Strategi Pemasaran
- [Dataset Retail](https://drive.google.com/file/d/1ogfkwMq3RFJL0dNMbFhwzyQvGOuX1TN6/view?usp=sharing)

---

## Results & Insights

Beberapa insight penting:

- **Segmen At-Risk** perlu strategi retensi untuk mencegah churn.  
- **Big Spenders** cocok untuk program loyalitas premium.  
- **Active Customers** merupakan target ideal untuk cross-selling atau upselling.  
- Personalization lebih efektif karena segmentasi berbasis data RFM.

Pendekatan RFM + K-Means dipilih karena fleksibel, relevan dengan industri ritel, dan mudah diadaptasi untuk berbagai kebutuhan bisnis.

---
