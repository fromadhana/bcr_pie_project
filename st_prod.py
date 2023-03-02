"""
author: f.romadhana@gmail.com

"""

#import necessary libraries
import pytz
import time
import pandas as pd
import streamlit as st
from time import sleep
from datetime import datetime
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect

#set page configuration
st.set_page_config(
  page_title="Form Produksi Pie",
  page_icon="👋🏻",
  layout="wide")

#set padding page
st.markdown(f""" <style>
      .block-container{{
        padding-top: 1rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 1rem;
    }} </style> """, unsafe_allow_html=True)

#hide streamlit menu and footer
hide_menu_style = """
          <style>
          #MainMenu {visibility: hidden; }
          footer {visibility: hidden;}
          </style>
          """
st.markdown(hide_menu_style, unsafe_allow_html=True)

#caching 
@st.cache_data
def process_for_index(index: int) -> int:
    sleep(0.5)
    return 2 * index + 1

#display title and caption
st.subheader(":orange[FORM PRODUKSI PIE GURIH90/JOGLO] 🧁")
st.caption("Form ini bertujuan untuk memantau secara sistematis semua produksi pie PT. Bogati Cerita Rasa")

#display streamlit form
with st.form(key= "form_produksi", clear_on_submit=True):
   #datetime now
   tp = st.date_input(label=":orange[Tanggal Produksi] 📅")
   timenow = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d-%m-%Y %H:%M:%S")
   time.sleep(1)
   
   #multiselect for employee attendance
   abs = st.multiselect(":orange[Siapa saja yang masuk hari ini?] 👨🏻‍🍳",
        ['M. Firmansah', 'M. Riyansyah', 
        'Marfiandani', 'Ahmad Maulana', 
        'Firmansyah', 'Indra Danur Wendra'])
   
   #space for visibility input pie brand & set number
   st.title(" ")
   st.title(" ")
   st.title(" ")

   #selectbox for pie brand
   merk = st.selectbox(':orange[Merk yang di produksi?]🎯', ('Pie Gurih90', 'Pie Joglo'))
   
   #selectbox for number of pie sets produced
   set = st.selectbox(':orange[Berapa SET produksi?]💰', list(range(21)))
   
   #number of boxes produced per pie flavor
   st.caption(":orange[Berapa BOX varian rasa yang di produksi?]")
   col1, col2 = st.columns(2)
   with col1:
    st.caption("Pie isi 6 (ENAM)")
    n61 = st.number_input('Original 6', min_value=0, max_value=1000, step=1)
    n62 = st.number_input('Coklat 6', min_value=0, max_value=1000, step=1)
    n63 = st.number_input('Matcha 6', min_value=0, max_value=1000, step=1)
    n64 = st.number_input('Banana 6', min_value=0, max_value=1000, step=1)
    n65 = st.number_input('Strawberry 6', min_value=0, max_value=1000, step=1)
    n66 = st.number_input('Mix 6', min_value=0, max_value=1000, step=1)
   with col2:
    st.caption("Pie isi 8 (DELAPAN)")
    n81 = st.number_input('Original 8', min_value=0, max_value=1000, step=1)
    n82 = st.number_input('Coklat 8', min_value=0, max_value=1000, step=1)
    n83 = st.number_input('Matcha 8', min_value=0, max_value=1000, step=1)
    n84 = st.number_input('Banana 8', min_value=0, max_value=1000, step=1)
    n85 = st.number_input('Strawberry 8', min_value=0, max_value=1000, step=1)
    n86 = st.number_input('Mix 8', min_value=0, max_value=1000, step=1)
    
   #submit button
   submitted = st.form_submit_button(label="Submit", use_container_width=True, type='primary')
   if submitted:
    #sum all number
    sum_p6 = n61 + n62 + n63 + n64 + n65 + n66
    sum_p8 = n81 + n82 + n83 + n84 + n85 + n86
    gt = sum_p8 + sum_p6
    #create dataframe
    df = pd.DataFrame({"Varian Rasa": ["Original", "Coklat", "Matcha", "Banana", "Strawberry", "Mix"], 
                        "Pie isi 6": [n61, n62, n63, n64, n65, n66], 
                        "Pie isi 8": [n81, n82, n83, n84, n85, n86]})
    #CSS to inject contained in a string
    hide_table_row_index = """
          <style>
          thead tr th:first-child {display:none}
          tbody th {display:none}
          </style>
          """
    #inject CSS with markdown
    hide = st.markdown(hide_table_row_index, unsafe_allow_html=True)
    container = st.container()
    container.write(":orange[Total Produksi Varian Rasa]")
    st.table(df)

    #show related information
    st.write(":green[Tanggal/Jam :] {}".format(timenow))
    st.write(":green[Tim Produksi :] {}".format(abs))
    st.write(":green[Merk Produksi :] {}".format(merk))
    st.write(":orange[Jumlah SET :] {}".format(set), "set")
    st.write(":orange[Total Pie isi 6 :] {}".format(sum_p6), "box")
    st.write(":orange[Total Pie isi 8 :] {}".format(sum_p8), "box")
    st.write(":green[GRAND TOTAL :] {}".format(gt), "box")
    st.success('Sukses tercatat! Terima kasih sudah bekerja keras hari ini! Semangat untuk hari esok!', icon="✅")

    #gcp credentials
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], 
        scopes=['https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.readonly', 
                'https://spreadsheets.google.com/feeds'])
    #shillelagh
    connection = connect(":memory:", adapter_kwargs={
      "gsheetsapi" : { 
      "service_account_info": {
              "type" : st.secrets["gcp_service_account"]["type"],
              "project_id" : st.secrets["gcp_service_account"]["project_id"],
              "private_key_id" : st.secrets["gcp_service_account"]["private_key_id"],
              "private_key" : st.secrets["gcp_service_account"]["private_key"],
              "client_email" : st.secrets["gcp_service_account"]["client_email"],
              "client_id" : st.secrets["gcp_service_account"]["client_id"],
              "auth_uri" : st.secrets["gcp_service_account"]["auth_uri"],
              "token_uri" : st.secrets["gcp_service_account"]["token_uri"],
              "auth_provider_x509_cert_url" : st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
              "client_x509_cert_url" : st.secrets["gcp_service_account"]["client_x509_cert_url"]},
              "subject" : st.secrets["gcp_service_account"]["client_email"],},},)
    
    #load to gsheet
    cursor = connection.cursor()
    sheet_url = st.secrets["private_gsheets_url"]
    query = f'INSERT INTO "{sheet_url}" VALUES ("{tp}", "{merk}", "{set}", "{n61}", "{n62}", "{n63}", "{n64}", "{n65}", "{n66}", "{n81}", "{n82}", "{n83}", "{n84}", "{n85}", "{n86}", "{abs}")'
    cursor.execute(query)
    st.balloons()

   else:
    st.warning('Isi jumlah BOX sesuai dengan varian rasa yang di produksi. SEMANGAT!', icon="⚠️")
    st.stop()