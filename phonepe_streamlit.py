#pip install mysql-connector-python
#pip install streamlit plotly mysql-connector-python
#pip install streamlit
#pip install streamlit_extras

import mysql.connector 
import pandas as pd
#import psycopg2
import seaborn as sns
import json
import streamlit as st
import PIL 
from PIL import Image
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import requests
import geopandas as gpd
# connect to the database
import mysql.connector
import pymysql
import numpy as np

#establishing the connection
conn = pymysql.connect(host='127.0.0.1', user='root', password='Aradhana@2509', db='Phonepe_Extract')
# create a cursor object
cursor = conn.cursor()
#st.set_page_config(layout='wide')
icon = Image.open("C:\\Users\\PRANESH\\Downloads\\phonepe-icon.png")
st.set_page_config(page_title= "Phonepe_Project | By KARTHIKA PRIYADHARSHINI",
                page_icon= icon,
                layout= "wide",
                initial_sidebar_state= "expanded",
                #primaryColor="#F63366",
                #backgroundColor="#FFFFFF",
                #secondaryBackgroundColor="#F0F2F6",
                #textColor="#262730",
                #font="sans serif",
                menu_items={'About': """# This app is created by *KARTHIKA PRIYADHARSHINI!*"""})
st.title(':violet[Phonepe Pulse Data Visualization & Exploration ]')

with st.sidebar:
    image=Image.open("C:\\Users\\PRANESH\\Downloads\\PhonePe-Logo.wine.png")
    st.image(image,width = 10,use_column_width="always",clamp=10)
    st.write("MENU")
    option = st.radio(
         'Select anyone to perform',
        ('Home','About','DataAPI','Basic insights'))
    
if option == "Home":
    st.header('PHONEPE_PULSE THE BEAT OF PROGRESS')
    #st.header('_Streamlit_ is :blue[cool] :sunglasses:')
    st.video("C:\\Users\\PRANESH\\Downloads\\pulse-video.mp4")
    
    image=Image.open("C:\\Users\\PRANESH\\Downloads\\decoding-bcg-report.webp")
    st.image(image,width = 10,use_column_width="always",clamp=10)

    
    image=Image.open("C:\\Users\\PRANESH\\Downloads\\bcg-report.webp")
    st.image(image,width = 10,use_column_width="always",clamp=10)

    text_contents = "C:\\Users\\PRANESH\\Downloads\\PhonePe_Pulse_BCG_report.pdf"
    st.download_button('Download Report', text_contents)

    #st.write("phonepe pulse")
    
#---------------------About------------------------#
    
if option == "About":
    st.video("https://youtu.be/c_1H6vivsiA?si=Wkzo5WmQkXgiBc3G")
    st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
    col1,col2 = st.columns(2)
    with col1:
        st.video("C:\\Users\\PRANESH\\Downloads\\upi.mp4")
    with col2:
        image=Image.open("C:\\Users\\PRANESH\\Downloads\\PhonePe-Logo.wine.png")
        st.image(image,width = 10,use_column_width="always",clamp=10)
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

        
    
    st.subheader(":red[AGGREGATED USERS]")
    cursor.execute("select distinct(states),sum(User_Count) as Phonepe_users from aggregated_user group by states order by sum(User_Count) DESC limit 10");
    agg_df = pd.DataFrame(cursor.fetchall(), columns=['States','Phonepe_users'])
    st.write(agg_df)
    fig=px.bar(agg_df, y='Phonepe_users', x='States', text='Phonepe_users', color='States')
# Put bar total value above bars with 2 values of precision
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    st.plotly_chart(fig,use_container_width=True)
    
    st.subheader(":red[MAP USERS]")
    cursor.execute("select distinct(states),sum(Registered_User) as Phonepe_users from map_users group by states order by sum(Registered_User) DESC limit 10");
    map_df = pd.DataFrame(cursor.fetchall(), columns=['States','Phonepe_users'])
    st.write(map_df)
    fig=px.bar(map_df, y='Phonepe_users', x='States', text='Phonepe_users', color='States')
# Put bar total value above bars with 2 values of precision
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    st.plotly_chart(fig,use_container_width=True)
    
    st.subheader(":red[TOP USERS]")
    cursor.execute("select distinct(states),sum(Registered_User)as Phonepe_users,Transaction_Year from top_users group by states,Transaction_Year order by sum(Registered_User) DESC limit 10");
    top_df = pd.DataFrame(cursor.fetchall(), columns=['States','Phonepe_users','Transaction_Year'])
    st.write(top_df)
    fig=px.bar(top_df, y='Phonepe_users', x='States', text='Phonepe_users', color='States')
# Put bar total value above bars with 2 values of precision
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    st.plotly_chart(fig,use_container_width=True)
    
    fig = px.scatter_3d(top_df, x='States', y='Phonepe_users', z='Transaction_Year', color='Transaction_Year',
                   opacity=0.7, width=800, height=400)
    st.plotly_chart(fig,use_container_width=True)
    
    #df=sns.heatmap(top_df.corr(),annot=True,vmin=-1)
    #st.plotly_chart(fig,use_container_width=True)

   
#--------------------HOME---------------------------------------------------------------#

if option == "DataAPI":
    
    image=Image.open("C:\\Users\\PRANESH\\Downloads\\PhonePe_Logo (1).jpg")
    st.image(image,width = 10,use_column_width="always",clamp=10)
    option = st.radio('**Select your option**',('All India', 'State wise','Top Ten categories'),horizontal=True)

# ===================================================       /      All India      /     ===================================================== #

    if option == 'All India':
        tab1, tab2 = st.tabs(['Transaction','User'])

    # -------------------------       /     All India Transaction        /        ------------------ #
        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
               in_tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='in_tr_yr')
            with col2:
               in_tr_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='in_tr_qtr')
            with col3:
               in_tr_tr_typ = st.selectbox('**Select Transaction type**', ('Recharge & bill payments','Peer-to-peer payments',
            'Merchant payments','Financial Services','Others'),key='in_tr_tr_typ')
          # SQL Query

    # Transaction Analysis bar chart query
            cursor.execute(f"SELECT States, Transaction_amount FROM aggregated_transaction WHERE Transaction_Year = '{in_tr_yr}' AND Quarters = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_tab_qry_rslt = cursor.fetchall()
            df_in_tr_tab_qry_rslt = pd.DataFrame(np.array(in_tr_tab_qry_rslt), columns=['State', 'Transaction_amount'])
            df_in_tr_tab_qry_rslt1 = df_in_tr_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_tr_tab_qry_rslt)+1)))

    # Transaction Analysis table query
            cursor.execute(f"SELECT States, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE Transaction_Year = '{in_tr_yr}' AND Quarters = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_anly_tab_qry_rslt = cursor.fetchall()
            df_in_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(in_tr_anly_tab_qry_rslt), columns=['State','Transaction_count','Transaction_amount'])
            df_in_tr_anly_tab_qry_rslt1 = df_in_tr_anly_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_tr_anly_tab_qry_rslt)+1)))

        # Total Transaction Amount table query
            cursor.execute(f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE Transaction_Year = '{in_tr_yr}' AND Quarters = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_am_qry_rslt = cursor.fetchall()
            df_in_tr_am_qry_rslt = pd.DataFrame(np.array(in_tr_am_qry_rslt), columns=['Total','Average'])
            df_in_tr_am_qry_rslt1 = df_in_tr_am_qry_rslt.set_index(['Average'])
            
            # Total Transaction Count table query
            cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE Transaction_Year = '{in_tr_yr}' AND Quarters = '{in_tr_qtr}' AND Transaction_type = '{in_tr_tr_typ}';")
            in_tr_co_qry_rslt = cursor.fetchall()
            df_in_tr_co_qry_rslt = pd.DataFrame(np.array(in_tr_co_qry_rslt), columns=['Total','Average'])
            df_in_tr_co_qry_rslt1 = df_in_tr_co_qry_rslt.set_index(['Average'])

        # --------- / Output  /  -------- #

        # ------    /  Geo visualization dashboard for Transaction /   ---- #
        # Drop a State column from df_in_tr_tab_qry_rslt
            df_in_tr_tab_qry_rslt.drop(columns=['State'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data1 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_tra = [feature['properties']['ST_NM'] for feature in data1['features']]
            state_names_tra.sort()
            # Create a DataFrame with the state names column
            df_state_names_tra = pd.DataFrame({'State': state_names_tra})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_tra['Transaction_amount']=df_in_tr_tab_qry_rslt
            # convert dataframe to csv file
            df_state_names_tra.to_csv('State_trans.csv', index=False)
            # Read csv
            df_tra = pd.read_csv('State_trans.csv')
            # Geo plot
            fig_tra = px.choropleth(
                df_tra,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',locations='State',color='Transaction_amount',color_continuous_scale='thermal',title = 'Transaction Analysis')
            fig_tra.update_geos(fitbounds="locations", visible=False)
            fig_tra.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
            st.plotly_chart(fig_tra,use_container_width=True)

        # ---------   /   All India Transaction Analysis Bar chart  /  ----- #
            df_in_tr_tab_qry_rslt1['State'] = df_in_tr_tab_qry_rslt1['State'].astype(str)
            df_in_tr_tab_qry_rslt1['Transaction_amount'] = df_in_tr_tab_qry_rslt1['Transaction_amount'].astype(float)
            df_in_tr_tab_qry_rslt1_fig = px.bar(df_in_tr_tab_qry_rslt1 , x = 'State', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'thermal', title = 'Transaction Analysis Chart', height = 700,)
            df_in_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(df_in_tr_tab_qry_rslt1_fig,use_container_width=True)

            # -------  /  All India Total Transaction calculation Table   /   ----  #
            st.header(':violet[Total calculation]')

            col4, col5 = st.columns(2)
            with col4:
                st.subheader('Transaction Analysis')
                st.dataframe(df_in_tr_anly_tab_qry_rslt1)
            with col5:
                st.subheader('Transaction Amount')
                st.dataframe(df_in_tr_am_qry_rslt1)
                st.subheader('Transaction Count')
                st.dataframe(df_in_tr_co_qry_rslt1)
            
            
    # ---------------------------------------       /     All India User        /        ------------------------------------ #
        with  tab2:
            col1, col2 = st.columns(2)
            with col1:
               in_us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='in_us_yr')
            with col2:
               in_us_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='in_us_qtr')
        
        # SQL Query

        # User Analysis Bar chart query
            cursor.execute(f"SELECT States, SUM(User_Count) FROM aggregated_user WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}' GROUP BY States;")
            in_us_tab_qry_rslt = cursor.fetchall()
            df_in_us_tab_qry_rslt = pd.DataFrame(np.array(in_us_tab_qry_rslt), columns=['States', 'User Count'])
            df_in_us_tab_qry_rslt1 = df_in_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_in_us_tab_qry_rslt)+1)))

            # Total User Count table query
            cursor.execute(f"SELECT SUM(User_Count), AVG(User_Count) FROM aggregated_user WHERE Year = '{in_us_yr}' AND Quarter = '{in_us_qtr}';")
            in_us_co_qry_rslt = cursor.fetchall()
            df_in_us_co_qry_rslt = pd.DataFrame(np.array(in_us_co_qry_rslt), columns=['Total','Average'])
            df_in_us_co_qry_rslt1 = df_in_us_co_qry_rslt.set_index(['Average'])

        # ---------  /  Output  /  -------- #

        # ------    /  Geo visualization dashboard for User  /   ---- #
        # Drop a State column from df_in_us_tab_qry_rslt
            df_in_us_tab_qry_rslt.drop(columns=['States'], inplace=True)
            # Clone the gio data
            url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
            response = requests.get(url)
            data2 = json.loads(response.content)
            # Extract state names and sort them in alphabetical order
            state_names_use = [feature['properties']['ST_NM'] for feature in data2['features']]
            state_names_use.sort()
            # Create a DataFrame with the state names column
            df_state_names_use = pd.DataFrame({'State': state_names_use})
            # Combine the Gio State name with df_in_tr_tab_qry_rslt
            df_state_names_use['User Count']=df_in_us_tab_qry_rslt
            # convert dataframe to csv file
            df_state_names_use.to_csv('State_user.csv', index=False)
            # Read csv
            df_use = pd.read_csv('State_user.csv')
            # Geo plot
            fig_use = px.choropleth(
                df_use,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',locations='State',color='User Count',color_continuous_scale='thermal',title = 'User Analysis')
            fig_use.update_geos(fitbounds="locations", visible=False)
            fig_use.update_layout(title_font=dict(size=33),title_font_color='#6739b7', height=800)
            st.plotly_chart(fig_use,use_container_width=True)

            # ----   /   All India User Analysis Bar chart   /     -------- #
            df_in_us_tab_qry_rslt1['State'] = df_in_us_tab_qry_rslt1['States'].astype(str)
            df_in_us_tab_qry_rslt1['User Count'] = df_in_us_tab_qry_rslt1['User Count'].astype(int)
            df_in_us_tab_qry_rslt1_fig = px.bar(df_in_us_tab_qry_rslt1 , x = 'State', y ='User Count', color ='User Count', color_continuous_scale = 'thermal', title = 'User Analysis Chart', height = 700,)
            df_in_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(df_in_us_tab_qry_rslt1_fig,use_container_width=True)

            # -----   /   All India Total User calculation Table   /   ----- #
            st.header(':violet[Total calculation]')

            col3, col4 = st.columns(2)
            with col3:
                st.subheader('User Analysis')
                st.dataframe(df_in_us_tab_qry_rslt1)
            with col4:
                st.subheader('User Count')
                st.dataframe(df_in_us_co_qry_rslt1)
# ==============================================          /     State wise       /             ============================================== #
    elif option =='State wise':

    # Select tab
        tab3, tab4 = st.tabs(['Transaction','User'])

    # ---------------------------------       /     State wise Transaction        /        ------------------------------- # 
        with tab3:
            col1, col2,col3 = st.columns(3)
            with col1:
                st_tr_st = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='st_tr_st')
            with col2:
                st_tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='st_tr_yr')
            with col3:
                st_tr_qtr = st.selectbox('**Select Quarter**', ('1','2','3','4'),key='st_tr_qtr')
            
        # SQL Query

            # Transaction Analysis bar chart query
            cursor.execute(f"SELECT Transaction_type, Transaction_amount FROM aggregated_transaction WHERE States = '{st_tr_st}' AND Transaction_Year = '{st_tr_yr}' AND Quarters = '{st_tr_qtr}';")
            st_tr_tab_bar_qry_rslt = cursor.fetchall()
            df_st_tr_tab_bar_qry_rslt = pd.DataFrame(np.array(st_tr_tab_bar_qry_rslt), columns=['Transaction_type', 'Transaction_amount'])
            df_st_tr_tab_bar_qry_rslt1 = df_st_tr_tab_bar_qry_rslt.set_index(pd.Index(range(1, len(df_st_tr_tab_bar_qry_rslt)+1)))

            # Transaction Analysis table query
            cursor.execute(f"SELECT Transaction_type, Transaction_count, Transaction_amount FROM aggregated_transaction WHERE States = '{st_tr_st}' AND Transaction_Year = '{st_tr_yr}' AND Quarters = '{st_tr_qtr}';")
            st_tr_anly_tab_qry_rslt = cursor.fetchall()
            df_st_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(st_tr_anly_tab_qry_rslt), columns=['Transaction_type','Transaction_count','Transaction_amount'])
            df_st_tr_anly_tab_qry_rslt1 = df_st_tr_anly_tab_qry_rslt.set_index(pd.Index(range(1, len(df_st_tr_anly_tab_qry_rslt)+1)))

            # Total Transaction Amount table query
            cursor.execute(f"SELECT SUM(Transaction_amount), AVG(Transaction_amount) FROM aggregated_transaction WHERE States = '{st_tr_st}' AND Transaction_Year = '{st_tr_yr}' AND Quarters = '{st_tr_qtr}';")
            st_tr_am_qry_rslt = cursor.fetchall()
            df_st_tr_am_qry_rslt = pd.DataFrame(np.array(st_tr_am_qry_rslt), columns=['Total','Average'])
            df_st_tr_am_qry_rslt1 = df_st_tr_am_qry_rslt.set_index(['Average'])
            
            # Total Transaction Count table query
            cursor.execute(f"SELECT SUM(Transaction_count), AVG(Transaction_count) FROM aggregated_transaction WHERE States = '{st_tr_st}' AND Transaction_Year ='{st_tr_yr}' AND Quarters = '{st_tr_qtr}';")
            st_tr_co_qry_rslt = cursor.fetchall()
            df_st_tr_co_qry_rslt = pd.DataFrame(np.array(st_tr_co_qry_rslt), columns=['Total','Average'])
            df_st_tr_co_qry_rslt1 = df_st_tr_co_qry_rslt.set_index(['Average'])

            # ---------  /  Output  /  -------- #

            # -----    /   State wise Transaction Analysis bar chart   /   ------ #
            df_st_tr_tab_bar_qry_rslt1['Transaction_type'] = df_st_tr_tab_bar_qry_rslt1['Transaction_type'].astype(str)
            df_st_tr_tab_bar_qry_rslt1['Transaction_amount'] = df_st_tr_tab_bar_qry_rslt1['Transaction_amount'].astype(float)
            df_st_tr_tab_bar_qry_rslt1_fig = px.bar(df_st_tr_tab_bar_qry_rslt1 , x = 'Transaction_type', y ='Transaction_amount', color ='Transaction_amount', color_continuous_scale = 'thermal', title = 'Transaction Analysis Chart', height = 500,)
            df_st_tr_tab_bar_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(df_st_tr_tab_bar_qry_rslt1_fig,use_container_width=True)

            # ------  /  State wise Total Transaction calculation Table  /  ---- #
            st.header(':violet[Total calculation]')

            col4, col5 = st.columns(2)
            with col4:
                st.subheader('Transaction Analysis')
                st.dataframe(df_st_tr_anly_tab_qry_rslt1)
            with col5:
                st.subheader('Transaction Amount')
                st.dataframe(df_st_tr_am_qry_rslt1)
                st.subheader('Transaction Count')
                st.dataframe(df_st_tr_co_qry_rslt1)
            # -----------------------------------------       /     State wise User        /        ---------------------------------- # 
        with tab4:
            col5, col6 = st.columns(2)
            with col5:
                st_us_st = st.selectbox('**Select State**',('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam', 'bihar', 
                'chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat', 'haryana', 'himachal-pradesh', 
                'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 
                'meghalaya', 'mizoram', 'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim', 'tamil-nadu', 'telangana', 
                'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),key='st_us_st')
            with col6:
                st_us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='st_us_yr')
            
            # SQL Query

            # User Analysis Bar chart query
            cursor.execute(f"SELECT Quarter, SUM(User_Count) FROM aggregated_user WHERE States = '{st_us_st}' AND Year = '{st_us_yr}' GROUP BY Quarter;")
            st_us_tab_qry_rslt = cursor.fetchall()
            df_st_us_tab_qry_rslt = pd.DataFrame(np.array(st_us_tab_qry_rslt), columns=['Quarter', 'User Count'])
            df_st_us_tab_qry_rslt1 = df_st_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_st_us_tab_qry_rslt)+1)))

            # Total User Count table query
            cursor.execute(f"SELECT SUM(User_Count), AVG(User_Count) FROM aggregated_user WHERE States = '{st_us_st}' AND Year = '{st_us_yr}';")
            st_us_co_qry_rslt = cursor.fetchall()
            df_st_us_co_qry_rslt = pd.DataFrame(np.array(st_us_co_qry_rslt), columns=['Total','Average'])
            df_st_us_co_qry_rslt1 = df_st_us_co_qry_rslt.set_index(['Average'])

            # ---------  /  Output  /  -------- #

            # -----   /   All India User Analysis Bar chart   /   ----- #
            df_st_us_tab_qry_rslt1['Quarter'] = df_st_us_tab_qry_rslt1['Quarter'].astype(int)
            df_st_us_tab_qry_rslt1['User Count'] = df_st_us_tab_qry_rslt1['User Count'].astype(int)
            df_st_us_tab_qry_rslt1_fig = px.bar(df_st_us_tab_qry_rslt1 , x = 'Quarter', y ='User Count', color ='User Count', color_continuous_scale = 'thermal', title = 'User Analysis Chart', height = 500,)
            df_st_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
            st.plotly_chart(df_st_us_tab_qry_rslt1_fig,use_container_width=True)

            # ------    /   State wise User Total User calculation Table   /   -----#
            st.header(':violet[Total calculation]')

            col3, col4 = st.columns(2)
            with col3:
                st.subheader('User Analysis')
                st.dataframe(df_st_us_tab_qry_rslt1)
            with col4:
                st.subheader('User Count')
                st.dataframe(df_st_us_co_qry_rslt1)
# ==============================================          /     Top categories       /             =========================================== #
    else:
        tab5, tab6 = st.tabs(['Transaction','User'])

    # ---------------------------------------       /     All India Top Transaction        /        ---------------------------- #
        with tab5:
            top_tr_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='top_tr_yr')

        # SQL Query

        # Top Transaction Analysis bar chart query
        cursor.execute(f"SELECT States, SUM(Transaction_amount) As Transaction_amount FROM top_transaction WHERE Transaction_Year = '{top_tr_yr}' GROUP BY States ORDER BY Transaction_amount DESC LIMIT 10;")
        top_tr_tab_qry_rslt = cursor.fetchall()
        df_top_tr_tab_qry_rslt = pd.DataFrame(np.array(top_tr_tab_qry_rslt), columns=['State', 'Top Transaction amount'])
        df_top_tr_tab_qry_rslt1 = df_top_tr_tab_qry_rslt.set_index(pd.Index(range(1, len(df_top_tr_tab_qry_rslt)+1)))

        # Top Transaction Analysis table query
        cursor.execute(f"SELECT States, SUM(Transaction_amount) as Transaction_amount, SUM(Transaction_count) as Transaction_count FROM top_transaction WHERE Transaction_Year = '{top_tr_yr}' GROUP BY States ORDER BY Transaction_amount DESC LIMIT 10;")
        top_tr_anly_tab_qry_rslt = cursor.fetchall()
        df_top_tr_anly_tab_qry_rslt = pd.DataFrame(np.array(top_tr_anly_tab_qry_rslt), columns=['States', 'Top Transaction amount','Total Transaction count'])
        df_top_tr_anly_tab_qry_rslt1 = df_top_tr_anly_tab_qry_rslt.set_index(pd.Index(range(1, len(df_top_tr_anly_tab_qry_rslt)+1)))

        # ---------  /  Output  /  -------- #

        # -----   /   All India Transaction Analysis Bar chart   /   ----- #
        df_top_tr_tab_qry_rslt1['State'] = df_top_tr_tab_qry_rslt1['State'].astype(str)
        df_top_tr_tab_qry_rslt1['Top Transaction amount'] = df_top_tr_tab_qry_rslt1['Top Transaction amount'].astype(float)
        df_top_tr_tab_qry_rslt1_fig = px.bar(df_top_tr_tab_qry_rslt1 , x = 'State', y ='Top Transaction amount', color ='Top Transaction amount', color_continuous_scale = 'thermal', title = 'Top Transaction Analysis Chart', height = 600,)
        df_top_tr_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_top_tr_tab_qry_rslt1_fig,use_container_width=True)

        # -----   /   All India Total Transaction calculation Table   /   ----- #
        st.header(':violet[Total calculation]')
        st.subheader('Top Transaction Analysis')
        st.dataframe(df_top_tr_anly_tab_qry_rslt1)


    # -------------------------       /     All India Top User        /        ------------------ #
        with tab6:
            top_us_yr = st.selectbox('**Select Year**', ('2018','2019','2020','2021','2022'),key='top_us_yr')

        # SQL Query

        # Top User Analysis bar chart query
        cursor.execute(f"SELECT States, SUM(Registered_User) AS Top_user FROM top_user WHERE Transaction_Year='{top_us_yr}' GROUP BY States ORDER BY Top_user DESC LIMIT 10;")
        top_us_tab_qry_rslt = cursor.fetchall()
        df_top_us_tab_qry_rslt = pd.DataFrame(np.array(top_us_tab_qry_rslt), columns=['States', 'Total User count'])
        df_top_us_tab_qry_rslt1 = df_top_us_tab_qry_rslt.set_index(pd.Index(range(1, len(df_top_us_tab_qry_rslt)+1)))

        # ---------  /  Output  /  -------- #

        # -----   /   All India User Analysis Bar chart   /   ----- #
        df_top_us_tab_qry_rslt1['States'] = df_top_us_tab_qry_rslt1['States'].astype(str)
        df_top_us_tab_qry_rslt1['Total User count'] = df_top_us_tab_qry_rslt1['Total User count'].astype(float)
        df_top_us_tab_qry_rslt1_fig = px.bar(df_top_us_tab_qry_rslt1 , x = 'States', y ='Total User count', color ='Total User count', color_continuous_scale = 'thermal', title = 'Top User Analysis Chart', height = 600,)
        df_top_us_tab_qry_rslt1_fig.update_layout(title_font=dict(size=33),title_font_color='#6739b7')
        st.plotly_chart(df_top_us_tab_qry_rslt1_fig,use_container_width=True)

        # -----   /   All India Total Transaction calculation Table   /   ----- #
        st.header(':violet[Total calculation]')
        st.subheader('Total User Analysis')
        st.dataframe(df_top_us_tab_qry_rslt1)


#---------------------Basic Insights ------------------#

if option == "Basic insights":
    st.title("BASIC INSIGHTS")
    st.write("----")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--",
               "Top 10 states based on year and amount of transaction",
               "List 10 states based on states and amount of transaction",
               "Top 5 Transaction_Type based on Transaction_Amount",
               "Top 10 Registered-users based on States and District",
               "Top 10 Districts based on states and Count of transaction",
               "List 10 Districts based on states and amount of transaction",
               "List 10 Transaction_Count based on Districts and states",
               "Top 10 RegisteredUsers based on states and District"]
    
               #1
               
    select = st.selectbox("Select the option",options)
    if select=="Top 10 states based on year and amount of transaction":
        cursor.execute("SELECT DISTINCT States, Transaction_Year, SUM(Transaction_Amount) AS Total_Transaction_Amount FROM top_transaction GROUP BY States, Transaction_Year ORDER BY Total_Transaction_Amount DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(), columns=['States','Transaction_Year', 'Transaction_Amount'])
        st.write(df)
        st.title("Top 10 states & amount of transaction")
        st.bar_chart(data=df,x="States",y="Transaction_Amount")
            
            #2
            
    elif select=="List 10 states based on states and amount of transaction":
        cursor.execute("SELECT DISTINCT States, SUM(Transaction_Count) as Total FROM top_transaction GROUP BY States ORDER BY Total ASC LIMIT 10");
        df2 = pd.DataFrame(cursor.fetchall(),columns=['States','Total_Transaction'])
        st.write(df2)
        st.title("List 10 states based on states and amount of transaction")
        #st.bar_chart(data=df2,x="States",y="Total_Transaction")
        fig=px.bar(df2, y='Total_Transaction', x='States', text='Total_Transaction', color='States')
# Put bar total value above bars with 2 values of precision
        fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
        st.plotly_chart(fig,use_container_width=True)
        

        
            
            #3
            
    elif select == "Top 5 Transaction_Type based on Transaction_Amount":
        cursor.execute("SELECT DISTINCT Transaction_Type, SUM(Transaction_Amount) AS Amount FROM aggregated_transaction GROUP BY Transaction_Type ORDER BY Amount DESC LIMIT 5")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_Type', 'Transaction_Amount'])
        st.write(df)
        st.title("Top 5 Transaction_Type based on Transaction_Amount")
        st.bar_chart(data=df, x="Transaction_Type", y="Transaction_Amount")
        

            #4
            
    elif select=="Top 10 Registered-users based on States and District":
        cursor.execute("SELECT DISTINCT States, District, SUM(Registered_User) AS Users FROM map_users GROUP BY States, District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','District','Registered_User'])
        st.write(df)
        st.title("Top 10 Registered-users based on States and District")
        #st.bar_chart(data=df,x="State",y="Registered_User")
        fig=px.bar(df, y='Registered_User', x='State', text='Registered_User', color='State')
# Put bar total value above bars with 2 values of precision
        fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
        st.plotly_chart(fig,use_container_width=True)
        
            
            #5
            
    elif select=="Top 10 Districts based on states and Count of transaction":
        cursor.execute("SELECT DISTINCT States,District,SUM(Transaction_Count) AS Counts FROM map_transaction GROUP BY States,District ORDER BY Counts DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','District','Transaction_Count'])
        st.write(df)
        st.title("Top 10 Districts based on states and Count of transaction")
        #st.bar_chart(data=df,x="States",y="Transaction_Count")
        fig=px.bar(df, y='Transaction_Count', x='States', text='Transaction_Count', color='States')
# Put bar total value above bars with 2 values of precision
        fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
        st.plotly_chart(fig,use_container_width=True)
            
            #6
            
    elif select=="List 10 States based on transaction year and amount of transaction":
        cursor.execute("SELECT DISTINCT States,Transaction_year,SUM(Transaction_Amount) AS Amount FROM aggregated_transaction GROUP BY States, Transaction_year ORDER BY Amount ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','Transaction_year','Transaction_Amount'])
        st.write(df)
        st.title("Least 10 Districts based on states and amount of transaction")
        st.bar_chart(data=df,x="States",y="Transaction_Amount")
            
            #s#7
            
    elif select=="List 10 Transaction_Count based on Districts and states":
        cursor.execute("SELECT DISTINCT States, District, SUM(Transaction_Count) AS Counts FROM map_transaction GROUP BY States,District ORDER BY Counts ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['States','District','Transaction_Count'])
        st.write(df)
        st.title("List 10 Transaction_Count based on Districts and states")
        st.bar_chart(data=df,y="States",x="Transaction_Count")
            
            #8
             
    elif select=="Top 10 RegisteredUsers based on states and District":
        cursor.execute("SELECT DISTINCT States,District, SUM(Registered_User) AS Users FROM map_users GROUP BY States,District ORDER BY Users DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns = ['States','District','Registered_User'])
        st.write(df)
        st.title("Top 10 RegisteredUsers based on states and District")
        st.bar_chart(data=df,y="States",x="Registered_User")
        



    

    
      
      
   
