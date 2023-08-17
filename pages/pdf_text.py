import streamlit as st
import json
from pages.functions_add_data import convert_pdf_to_txt_file, displayPDF
from streamlit_extras.colored_header import colored_header
from st_pages import add_page_title
from pages.preprocess import *
import pandas as pd

df_current = pd.read_csv('assets/inicsv.csv')

add_page_title(layout="wide")

colored_header(
    label="1. Upload Data",
    description="",
    color_name="violet-70",
)

html_temp = """
            <div style="background-color:{};padding:1px">
            
            </div>
            """

pdf_file = st.file_uploader("Load your PDF", type=['pdf', 'png', 'jpg'])

if pdf_file:
    colored_header(
        label="2. Tipe Perundang-undangan",
        description="",
        color_name="violet-70",
    )

    # Input field for Tingkatan Perundangan
    tingkatan_options = [
        "Peraturan Pemerintah",
        "Peraturan Presiden",
        "Peraturan Menteri",
        "UU_Perpu"
    ]
    tingkatan_perundangan = st.selectbox("2. Tipe Perundangan", tingkatan_options)

    hide = """
    <style>
    footer{
        visibility: hidden;
            position: relative;
    }
    .viewerBadge_container__1QSob{
        visibility: hidden;
    }
    #MainMenu{
        visibility: hidden;
    }
    <style>
    """
    st.markdown(hide, unsafe_allow_html=True)
    
    # Submit button
    if st.button("Submit"):
        if pdf_file:
            path = pdf_file.read()
            file_extension = pdf_file.name.split(".")[-1]
            
            if file_extension == "pdf":
                colored_header(
                    label="3. Cek Data",
                    description="",
                    color_name="violet-70",
                )
                # Display document
                with st.expander("Display document"):
                    displayPDF(path)

                # Convert PDF to text
                text_data_f, nbPages = convert_pdf_to_txt_file(pdf_file)
                totalPages = "Pages: "+str(nbPages)+" in total"

                st.info(totalPages)
                
                # Create a dictionary to store data
                data = {
                    "Tingkatan": tingkatan_perundangan,
                    "ExtractedText": text_data_f,
                    "FileName": pdf_file.name  # Adding the filename to the data
                }
                
                # Convert dictionary to JSON
                json_data = json.dumps(data, indent=4)

                df = pd.DataFrame([[data['Tingkatan'], data['FileName'], data['ExtractedText']]],
                                    columns=['Tingkatan', 'FileName', 'ExtractedText'])
                
                df_preprocess = preprocessing_text(df)
                concat = pd.concat([df_current, df_preprocess], ignore_index=True)
                concat.to_csv('assets/inicsv.csv', index=False)
                
                # Display JSON
                # st.text("Raw Data in JSON format:")
                # st.text(json_data)

                # In dataframe format, before
                # st.text("Data in Dataframe format, before preprocess:")
                # df = pd.DataFrame([[data['Tingkatan'], data['FileName'], data['ExtractedText']]], 
                #                     columns=['Tingkatan', 'FileName', 'ExtractedText'])
                # df
                
                # # In dataframe format after preprocess
                # st.text("Data in Dataframe format, after preprocess:")
                # a = preprocessing_text(df)
                # a

                # button
                # if st.button("Submit to Database"):
                #     st.error("Do you really, really, wanna do this?")
                # st.download_button("Download txt file", text_data_f)   

                # colored_header(
                #     label="5. Unduh atau Kirim?",
                #     description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                #     color_name="violet-70",
                # )
                
                # st.download_button("Download txt file", text_data_f)
                # # Create a placeholder to display the extracted text
                # text_placeholder = st.empty()

                # if st.button('Submit to Database'):
                #     a = pd.DataFrame([[data['Tingkatan'], data['FileName'], data['ExtractedText']]], 
                #                     columns=['Tingkatan', 'FileName', 'ExtractedText'])
                #     b = preprocessing_text(a)
                #     b
                #     st.write('Data submitted to database')

                # colored_header(
                #     label="TESTT TESTTT",
                #     description="Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                #     color_name="violet-70",
                # )
                
                # a = df = pd.DataFrame([[data['Tingkatan'], data['FileName'], data['ExtractedText']]], 
                #   columns=['Tingkatan', 'FileName', 'ExtractedText'])
                # a
                # b = preprocessing_text(a)
                # b