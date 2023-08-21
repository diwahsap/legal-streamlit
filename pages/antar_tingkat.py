from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_extras.grid import grid
import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header
from st_pages import add_page_title
from pages.functions_preprocess_data import *
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt
import time
st.set_option('deprecation.showPyplotGlobalUse', False)

add_page_title(layout="wide")

colored_header(
    label="Pilih Perundang-undangan yang akan dibandingkan",
    description="",
    color_name="red-30",
)

df = pd.read_csv('assets/inicsv.csv')
filter_df = df[["Tingkatan", "FileName", "ExtractedText", "cleaned_text", "final_text"]]

all_selaras = pd.read_csv('assets/all_selaras.csv')
# all_selaras = all_selaras.iloc[:, 1:]

# Input field for Tingkatan Perundangan
tingkatan_options = [
    "Peraturan Pemerintah",
    "Peraturan Presiden",
    # "Peraturan Menteri",
    "UU_Perpu"
]

# create column
col1, col2 = st.columns(2)
with col1:
    data1 = st.selectbox("Tipe Perundangan 1", tingkatan_options)
with col2:
    data2 = st.selectbox("Tipe Perundangan 2", tingkatan_options)

selected_df = filter_df.query(f'Tingkatan == "{data1}" or Tingkatan == "{data2}"')
# show dataframe
# st.dataframe(selected_df, use_container_width=True)

start_time = time.time()
# Convert the tf-idf matrix to a dense matrix
tfidf_matrix, feature_names = tfidf(selected_df['final_text'])
tfidf_matrix_dense = tfidf_matrix.toarray()

colored_header(
    label="Visualisasi Heatmap",
    description="",
    color_name="red-30",
)

with st.expander("TF-IDF Matrix"):
    # print to user, text
    st.write("TF-IDF Matrix")
    DTM_df = pd.DataFrame(tfidf_matrix.toarray(), columns = feature_names)
    DTM_df.index = selected_df['FileName']
    st.dataframe(DTM_df, use_container_width=True)
    end_time = time.time()
    execution_time = end_time - start_time

    st.warning(f"Memerlukan waktu {execution_time:.2f} detik untuk dieksekusi.")

# Create the array of cosine similarity values
start_time = time.time()
cosine_similarity_array = cosine_similarity(DTM_df)

# Wrap the array in a pandas DataFrame
cosine_similarity_df = pd.DataFrame(cosine_similarity_array, index=DTM_df.index, columns=DTM_df.index)

data1_file_names = df[df['Tingkatan'] == data1]['FileName'].values
data2_file_names = df[df['Tingkatan'] == data2]['FileName'].values

filtered_df = cosine_similarity_df[data1_file_names]
filtered_df = filtered_df.loc[data2_file_names]

tab_selection = st.radio("Select Tab", ["📈 Chart", "🗃 Data"])

if tab_selection == "📈 Chart":
    plt.figure(figsize=(10, 8))
    sns.heatmap(filtered_df, annot=False, cmap='viridis')
    st.pyplot()
    end_time = time.time()
    execution_time = end_time - start_time

    st.warning(f"Memerlukan waktu {execution_time:.2f} detik untuk dieksekusi.")
else:
    st.dataframe(filtered_df, use_container_width=True)
    end_time = time.time()
    execution_time = end_time - start_time

    st.warning(f"Memerlukan waktu {execution_time:.2f} detik untuk dieksekusi.")

def convert_to_label(score):
    if score < 0.2:
        return 'Tidak Selaras'
    elif score < 0.4:
        return 'Netral'
    else:
        return 'Selaras'

start_time = time.time()
# Apply the function element-wise to the filtered_df DataFrame
label_df = filtered_df.applymap(convert_to_label)

colored_header(
    label="Selaras, Netral, Tidak Selaras",
    description="",
    color_name="red-30",
)

counts = label_df.apply(pd.Series.value_counts).fillna(0)
col1, col2, col3= st.columns(3)
col1.metric("Netral", int(counts.loc['Netral'].sum()))
col2.metric("Selaras", int(counts.loc['Selaras'].sum()))
col3.metric("Tidak Selaras", int(counts.loc['Tidak Selaras'].sum()))

st.write("")
st.dataframe(label_df, use_container_width=True)
end_time = time.time()
execution_time = end_time - start_time
st.warning(f"Memerlukan waktu {execution_time:.2f} detik untuk dieksekusi.")

start_time = time.time()
row_indices, col_indices = np.where(label_df == 'Selaras')
row_names = label_df.index[row_indices]
col_names = label_df.columns[col_indices]
df_selaras = pd.DataFrame({'Perundangan1': row_names, 'Perundangan2': col_names})
# df_selaras

colored_header(
    label="Perundang-undangan yang Memiliki Keselarasan",
    description="",
    color_name="red-30",
)
for i in range(len(df_selaras)):
  res = df_selaras.iloc[i,0]
  df_selaras.loc[i, 'Topic1'] = df['cleaned_text'][df.query('FileName == @res').index[0]][0]

  res2 = df_selaras.iloc[i,1]
  df_selaras.loc[i, 'Topic2'] = df['cleaned_text'][df.query('FileName == @res2').index[0]][0]

st.dataframe(df_selaras[['Perundangan1', 'Perundangan2']], use_container_width=True)
end_time = time.time()
execution_time = end_time - start_time

st.warning(f"Memerlukan waktu {execution_time:.2f} detik untuk dieksekusi.")

# st.dataframe(all_selaras[['Perundangan1', 'Perundangan2']], use_container_width=True)

# last_row_df_selaras = df_selaras.iloc[-1, 0:2]
all_row_df_selaras = all_selaras.iloc[:, 0:2]

# Convert last row to a DataFrame for concatenation
# last_row_df = pd.DataFrame([last_row_df_selaras])
last_row_df = df_selaras[['Perundangan1', 'Perundangan2']]


if data1 == data2:
    pass
else:
    # Check if the last row is not in all_selaras
    if not all_selaras.isin(all_row_df_selaras).any().any():
        # Concatenate the last row DataFrame to all_selaras
        all_selaras = pd.concat([all_selaras, last_row_df], ignore_index=True)
        all_selaras = all_selaras.drop_duplicates(subset = ['Perundangan1', 'Perundangan2'],keep = 'first', inplace=True)

        # Save to CSV
        all_selaras.to_csv('assets/all_selaras.csv', index=False)


# last_row_all_selaras = all_selaras.iloc[-1]
# st.dataframe(last_row_df_selaras, use_container_width=True)
# st.dataframe(last_row_all_selaras, use_container_width=True)