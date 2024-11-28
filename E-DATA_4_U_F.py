import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup as bs
from requests import get
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit.components.v1 as components

# Titre principal avec une esthétique modernisée
st.markdown("""
    <h1 style='text-align: center; font-size: 3rem; color: #4A90E2; font-family: Arial, sans-serif; margin-bottom: 20px;'>
    E-DATA ANIMALS FOR YOU
    </h1>
""", unsafe_allow_html=True)

# Description avec un formatage clair
st.markdown("""
    <div style='font-family: Arial, sans-serif; font-size: 1rem; color: #333; line-height: 1.6;'>
        <p>This application allows you to easily collect and visualize data for poultry, dogs, sheep, and other animals for free.</p>
        <p>You have the option to choose between collecting data using <b>BeautifulSoup</b> or a <b>web scraper</b>.</p>
        <ul>
            <li><b>Python libraries:</b> base64, pandas, streamlit, requests, bs4</li>
            <li><b>Data source:</b> <a href='https://sn.coinafrique.com/' target='_blank' style='color: #4A90E2;'>CoinAfrique</a></li>
        </ul>
    </div>
""", unsafe_allow_html=True)

# Fonction pour générer des graphiques avec une meilleure apparence
def plot_bar_chart(df, title, xlabel, figsize=(8, 5)):
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=figsize)
    top_values = df.Name.value_counts()[:5]
    sns.barplot(x=top_values.index, y=top_values.values, ax=ax, palette="Blues_d")
    ax.set_title(title, fontsize=14, color="#4A90E2", weight='bold', pad=15)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.set_xticklabels(top_values.index, rotation=45, fontsize=10)
    sns.despine()
    return fig

# Fonction pour ajouter un arrière-plan
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Fonction pour convertir un DataFrame en CSV
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

# Fonction pour afficher les données et permettre leur téléchargement
def load(dataframe, title, key, key1):
    st.markdown("""
        <style>
        div.stButton > button {{
            background-color: #4A90E2;
            color: white;
            font-size: 1rem;
            border-radius: 5px;
            padding: 10px 20px;
            border: none;
        }}
        div.stButton > button:hover {{
            background-color: #357ABD;
        }}
        </style>
    """, unsafe_allow_html=True)

    if st.button(title, key1):
        st.subheader('Display data dimension')
        st.write(f'Data dimension: {dataframe.shape[0]} rows and {dataframe.shape[1]} columns.')
        st.dataframe(dataframe, width=900, height=400)

        csv = convert_df(dataframe)
        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='Data.csv',
            mime='text/csv',
            key=key
        )

# Fonction CSS pour personnaliser l'apparence
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Fonction pour scraper les données sur les animaux
def load_animaux_data(mul_page):
    df = pd.DataFrame()
    for page in mul_page:
        url = f'https://sn.coinafrique.com/categorie/autres-animaux?page={page}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')
        data = []
        for container in containers:
            try:
                Name = container.find('p', class_='ad__card-description').text.strip()
                price = container.find('p', class_='ad__card-price').text.strip().replace(' ', '').replace('CFA', '')
                adress = container.find('p', class_='ad__card-location').span.text.strip()
                img_link = container.find('a', class_='card-image ad__card-image waves-block waves-light').img['src']
                dic = {'Name': Name, 'price': price, 'adress': adress, 'img_link': img_link}
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
    return df

def load_Vollailes_data(mul_page):
    df = pd.DataFrame()
    for page in mul_page:
        url = f'https://sn.coinafrique.com/categorie/poules-lapins-et-pigeons?page={page}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')
        data = []
        for container in containers:
            try:
                Name = container.find('p', class_='ad__card-description').text.strip()
                price = container.find('p', class_='ad__card-price').text.strip().replace(' ', '').replace('CFA', '')
                adress = container.find('p', class_='ad__card-location').span.text.strip()
                img_link = container.find('a', class_='card-image ad__card-image waves-block waves-light').img['src']
                dic = {'Name': Name, 'price': price, 'adress': adress, 'img_link': img_link}
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
    return df

def load_sheep_data(mul_page):
    df = pd.DataFrame()
    for page in mul_page:
        url = f'https://sn.coinafrique.com/categorie/moutons?page={page}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')
        data = []
        for container in containers:
            try:
                Name = container.find('p', class_='ad__card-description').text.strip()
                price = container.find('p', class_='ad__card-price').text.strip().replace(' ', '').replace('CFA', '')
                adress = container.find('p', class_='ad__card-location').span.text.strip()
                img_link = container.find('a', class_='card-image ad__card-image waves-block waves-light').img['src']
                dic = {'Name': Name, 'price': price, 'adress': adress, 'img_link': img_link}
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
    return df  

def load_Dogs_data(mul_page):
    df = pd.DataFrame()
    for page in mul_page:
        url = f'https://sn.coinafrique.com/categorie/chiens?page={page}'
        res = get(url)
        soup = bs(res.text, 'html.parser')
        containers = soup.find_all('div', class_='col s6 m4 l3')
        data = []
        for container in containers:
            try:
                Name = container.find('p', class_='ad__card-description').text.strip()
                price = container.find('p', class_='ad__card-price').text.strip().replace(' ', '').replace('CFA', '')
                adress = container.find('p', class_='ad__card-location').span.text.strip()
                img_link = container.find('a', class_='card-image ad__card-image waves-block waves-light').img['src']
                dic = {'Name': Name, 'price': price, 'adress': adress, 'img_link': img_link}
                data.append(dic)
            except:
                pass
        DF = pd.DataFrame(data)
        df = pd.concat([df, DF], axis=0).reset_index(drop=True)
    return df  



# Interface utilisateur avec amélioration des couleurs et de l'organisation
st.sidebar.markdown("""
    <h2 style='font-family: Arial, sans-serif; color: #4A90E2; font-size: 1.5rem;'>
    User Input Features
    </h2>
""", unsafe_allow_html=True)

mul_page = st.sidebar.multiselect(
    'Select pages to scrape',
    list(range(1, 601)),  
    default=[1]
)

Choices = st.sidebar.selectbox(
    'Options', 
    ['Scrape data using BeautifulSoup', 'Download scraped data using Web Scraper', 
     'Dashboard of the data', 'Fill the form', 'Descriptive Statistics']
)

add_bg_from_local('img.jpg')
#local_css('style.css')
# Afficher les donnees de beautifulsoup avec le nombre de page souhaite
if Choices == 'Scrape data using BeautifulSoup':
    if not mul_page:
        st.warning("Please select at least one page.")
    else:
        st.info(f"Scraping pages: {mul_page}")

        animaux_data_mul_page = load_animaux_data(mul_page)
        dogs_data_mul_pag = load_Dogs_data(mul_page)
        poultry_data_mul_pag = load_Vollailes_data(mul_page)
        sheep_data_mul_pag = load_sheep_data(mul_page)

        load(animaux_data_mul_page, 'Others animals data', '1', '101')
        load(dogs_data_mul_pag, 'Dogs data', '2', '102')
        load(poultry_data_mul_pag, 'Poultry data', '3', '103')
        load(sheep_data_mul_pag, 'Sheep data', '4', '104')
# Afficher les donnees de web scrapper non nettoyeees
elif Choices == 'Download scraped data using Web Scraper':
    Animals = pd.read_csv('Autres_Animaux_WS.csv')
    Dogs = pd.read_csv('Dogs_WS.csv')
    Sheep = pd.read_csv('Mouton_WS.csv')
    Poultry = pd.read_csv('Volailles_WS.csv')

    load(Animals, 'Others animals data', '1', '101')
    load(Dogs, 'Dogs data', '2', '102')
    load(Sheep, 'Sheep data', '3', '103')
    load(Poultry, 'Poultry data', '4', '104')
#  Pour voir les graphiques des donnees de web scrapper nettoyeees
elif Choices == 'Dashboard of the data':
    df1 = pd.read_csv('Autres_Animaux_Data_Cleaned.csv')
    df2 = pd.read_csv('Dogs_Data_Cleaned.csv')
    df3 = pd.read_csv('Moutons_Data_Cleaned.csv')
    df4 = pd.read_csv('Volailles_Data_Cleaned.csv')

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_bar_chart(df1, '5 Best Selling Animal Types', 'Others Animals'))

    with col2:
        st.pyplot(plot_bar_chart(df2, '5 Best Selling Dog Types', 'Dogs'))

    col3, col4 = st.columns(2)
    with col3:
        st.pyplot(plot_bar_chart(df3, '5 Best Selling Sheep Types', 'Sheep'))

    with col4:
        st.pyplot(plot_bar_chart(df4, '5 Best Selling Poultry Types', 'Poultry'))

elif Choices == 'Descriptive Statistics':
    st.header("Descriptive Statistics")

    df_animals = pd.read_csv('Autres_Animaux_Data_Cleaned.csv')
    df_dogs = pd.read_csv('Dogs_Data_Cleaned.csv')
    df_sheep = pd.read_csv('Moutons_Data_Cleaned.csv')
    df_poultry = pd.read_csv('Volailles_Data_Cleaned.csv')

    category = st.selectbox('Choose a category:', ['Others Animals', 'Dogs', 'Sheep', 'Poultry'])

    if category == 'Others Animals':
        st.write(df_animals.describe())
    elif category == 'Dogs':
        st.write(df_dogs.describe())
    elif category == 'Sheep':
        st.write(df_sheep.describe())
    elif category == 'Poultry':
        st.write(df_poultry.describe())


else:
    components.html("""
    <iframe src="https://ee.kobotoolbox.org/i/y3pfGxMz" width="800" height="1100"></iframe>
    """, height=1100, width=800)

