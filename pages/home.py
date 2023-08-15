import streamlit as st
from streamlit_extras.colored_header import colored_header
from st_pages import add_page_title
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space

add_page_title(layout="wide")

colored_header(
    description="Welcome to Our Projects, Satria Data 2023!",
    label="Text Analytics menggunakan Metode TF-IDF untuk Mengidentifikasi Keselarasan Peraturan Perundang-undangan dalam Lingkup Investasi di Indonesia",
    color_name="violet-70",
)

st.sidebar.success("SD2023040000171")

col1, col2 = st.columns([5, 3])
with col2:
    st.image('assets/metodologi.png', use_column_width=True)

with col1:
    st.markdown("""
                Penelitian ini bertujuan untuk menganalisis keselarasan peraturan perundang-undangan dalam lingkup investasi di Indonesia menggunakan metode Text Analytics dengan memanfaatkan Term Frequency-Inverse Document Frequency (TF-IDF). Peraturan perundang-undangan memiliki peran penting dalam sistem hukum suatu negara namun kompleksitas masalah yang dihadapi masyarakat seringkali membuat peraturan harus diperbarui dan direvisi sehingga sulit untuk menilai konsistensi dan keselarasannya. Proses manual yang sering dilakukan oleh ahli hukum dan pihak terkait memakan waktu, sumber daya, dan dapat mengakibatkan kesalahan manusia. Oleh karena itu, metode text analytics menjadi solusi menarik untuk mengotomatisasi proses tersebut. Metode TF-IDF digunakan untuk mengidentifikasi istilah dan frasa yang paling penting dalam peraturan perundang-undangan sehingga memberikan wawasan tentang koherensi dan konsistensi teks hukum. Dalam penelitian ini, dataset yang digunakan adalah kumpulan berkas peraturan perundang-undangan yang ada di Indonesia dengan empat tingkatan, yaitu Undang-undang, Peraturan Pemerintah, Peraturan Presiden, dan Peraturan Menteri. Tahapan yang dilakukan meliputi ekstraksi teks atau Optical Character Recognition (OCR), preprocessing, penghitungan TF-IDF, Document-Term Matrix, dan penghitungan similarity menggunakan cosine. Hasil analisis keselarasan peraturan-peraturan dalam bentuk output yang informatif, seperti grafik visualisasi, memberikan wawasan berharga bagi para pemangku kebijakan dalam mengoptimalkan sistem perundang-undangan di bidang investasi. Terdapat 16 klaster yang ditemukan dalam peraturan perundang-undangan masing-masing memiliki istilah dan frasa yang sangat relevan dalam klaster tersebut. 
    """)


df = pd.read_csv('assets/inicsv.csv')

# add_vertical_space(2)

st.metric("Jumlah Data", len(df.index))
st.metric("Jenis Peraturan", df['Tingkatan'].nunique())