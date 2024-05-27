import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import sys
import os


#page setup
st.set_page_config(page_title='Data Profiling',layout='wide')

def get_filesize(file):
    size_bytes = sys.getsizeof(file)
    size_mb = size_bytes / (1024**2)
    return size_mb

def validate_file(file):
    filename=file.name
    name,ext = os.path.splitext(filename)
    if ext in ('.csv','.xlsx'):
        return ext
    else:
        return False

#sidebar
with st.sidebar:
    upload_file= st.file_uploader("Upload .csv, .xlsx files not exceeding 10 MB")
    if upload_file is not None:
        st.write('Modes of operation')
        minimal = st.checkbox('Do you want minimal report?')
        display_mode = st.radio("Display mode:",
                                options=('Primary','Dark','Orange'))
        
        if display_mode == 'Dark':
            dark_mode = True
            orange_mode = False
        elif display_mode == 'Orange':
            dark_mode = False
            orange_mode= True
        else:
            dark_mode=False
            orange_mode=False
    
    
    
if upload_file is not None:
    st.title('Data Profiling')
    ext=validate_file(upload_file)
    if ext:
        filesize=get_filesize(upload_file)
        if filesize <=10:
            #load data
            if ext == '.csv':
                df=pd.read_csv(upload_file)
            else:
                xl_file = pd.ExcelFile(upload_file)
                sheet_tuple = tuple(xl_file.sheet_names)
                sheet_name = st.sidebar.selectbox('Select the sheet',sheet_tuple)
                df = xl_file.parse(sheet_name)
            st.subheader('Uploaded Dataset Sample')
            st.dataframe(df.head())
            #to generate report
            st.markdown('---')
            with st.spinner('Generating Report'):
                pr=ProfileReport(df,minimal=minimal,
                                dark_mode=dark_mode,
                                orange_mode=orange_mode)
            
            st_profile_report(pr)
        else:
            st.error('Maximum allowed file size is 10MB. You have uploaded file with {filesize} MB filesize')
    else:
        st.error('Kindly upload only .csv or .xlsx files only')
else:
    st.title('Data Profiling')
    st.info('Upload Your data in the left sidebar to generate profiling')