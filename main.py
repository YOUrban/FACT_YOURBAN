# Fichier: main.py
import streamlit as st
from streamlit_searchbox import st_searchbox
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud



LOGO_URL_LARGE = "images/logo_big.png"
LOGO_URL_SMALL = "images/logoYBsmall.png"

st.logo(
    LOGO_URL_LARGE,
    link="https://go-yourban.com/wp-content/uploads/2023/06/yourban.png",
    icon_image=LOGO_URL_SMALL,
)


# Configuration de la page
st.set_page_config(page_title="Demo Yourban x FACT", layout="wide")


# Barre latérale de navigation
def sidebar_navigation():
    page = st.sidebar.radio("Menu", ["Accueil", "Dashboard de tendances", "Explorez sur la carte"])
    return page

# Page d'Accueil
def home_page():
    st.markdown("""
## Bienvenue sur l'application de suivi de la demande en locaux commerciaux en France ! 🏢📊

Dans le cadre d'un partenariat innovant entre **YOUrban** et la **FACT** (Fédération des Acteurs du Commerce Territorial), nous avons développé une application interactive pour analyser les **évolutions des recherches de locaux commerciaux** à travers toute la France. 🇫🇷✨

#### 🎯 Objectifs de l'application :
- **Explorer les dynamiques locales** de recherche pour des locaux commerciaux.
- Identifier les **villes les plus recherchées** pour un projet d'installation.
- Suivre les tendances sur une **carte interactive** et un **dashboard intuitif**.

#### 📊 Quelques résultats clés :
Explorez les **villes les plus recherchées** pour des locaux commerciaux. Classez les selon le **volume de recherche**, l'**interet** ou la **croissance** des recherches, en ***cliquant sur le haut de colonne***.
""")
    df_ranking_cities = pd.read_csv("data/ranking_cities.csv").sort_values(by="Recherches sur 12 mois", ascending=False)
    st.data_editor(df_ranking_cities[df_ranking_cities["Index d'intérêt"]!=0], use_container_width = True, hide_index=True, num_rows=8)
    st.markdown("""
#### 🚀 Fonctionnement :
1. **Dashboard interactif** : Visualisez des graphiques et des statistiques pour comprendre les tendances de recherche.
2. **Carte dynamique** : Explorez les recherches par ville ou région grâce à des visualisations claires et détaillées.
3. **Classements en temps réel** : Découvrez les **villes les plus attractives** en matière de recherches pour des locaux commerciaux.

#### 🌟 Découvrez par vous-même !
Explorez les données et identifiez les opportunités pour vos projets commerciaux. Cet outil a été conçu pour vous fournir **les clés nécessaires à une prise de décision éclairée**.

N'hésitez pas à naviguer et à profiter des insights exclusifs que nous mettons à votre disposition. Bonne exploration ! 🗺️💼
""")
    
# Page de recherche de prospect
def dashboard():

    st.markdown("""
## Explorez les tendances de recherche pour des locaux commerciaux en France 🏢📈

Bienvenue sur le **dashboard interactif**, votre outil clé pour analyser et comprendre les **évolutions de la demande en locaux commerciaux** à travers toute la France ! 🇫🇷✨
""")
    
    df = pd.read_csv("data/results_france.csv")
    columns_months = list(df.columns[-55:-6])

    df_wc = pd.read_csv("data/results_france_wordcloud.csv")

    #st.area_chart(df_france_total.columns[-55:-6])
    tags = st.pills("Sélectionnez le type de recherche à analyser :", options=["Total", "Achat", "Location"], default="Total")

    

# Display a KPI
    # Étape 2 : Filtrer les données selon le choix de l'utilisateur
    if tags:

        # Inject custom CSS for shadow effect
        
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Recherches sur les 12 derniers mois", format(int(df[df["Tag"]==tags]["somme_last_12_months"]), ",").replace(",", " "))
        col2.metric("Croissance vs 2023", str(round(float(df[df["Tag"]==tags]["growth_2023vs2024"])*100))+"%")
        col3.metric("Croissance vs 2022", str(round(float(df[df["Tag"]==tags]["growth_2022vs2024"])*100))+"%")


        filtered_df = df[df["Tag"]==tags]

        # Transformation pour que `TAG` soit l'index
        filtered_df = filtered_df.set_index("Tag")[columns_months].transpose()
        

        # Étape 3 : Affichage avec st.area_chart
        st.area_chart(filtered_df)

        df_wc_filtered = df_wc[(df_wc["Tag"]==tags)|(tags=="Total")]
        if not df_wc_filtered.empty:
            # Étape 3 : Créer un dictionnaire {mot: valeur}
            word_freq = dict(zip(df_wc_filtered["Keyword"], df_wc_filtered["yearly_average"]))

            # Étape 4 : Générer le WordCloud
            wc = WordCloud(
                background_color="white",
                colormap="viridis",
                max_words=100,
                width=800,
                height=400
            ).generate_from_frequencies(word_freq)

            # Étape 5 : Afficher le WordCloud avec Matplotlib
            fig, ax = plt.subplots()
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)


    else:
        st.warning("Veuillez sélectionner au moins une série à afficher.")

    st.markdown("""
#### 🎯 Que pouvez-vous faire avec ce dashboard ?
- **Visualiser les tendances globales** : Suivez l'évolution de toutes les recherches liées aux locaux commerciaux.
- **Segmenter par type de besoin** :
  - 🏠 **Acheter un local** : Identifiez les villes où la demande d'achat est la plus forte.
  - 📄 **Louer un local** : Repérez les zones avec un fort intérêt pour la location.
- **Comparer les tendances** : Analysez comment les recherches évoluent dans différentes régions ou villes.

#### 🔍 Comment utiliser ce dashboard ?
1. Sélectionnez un **type de recherche** : Toutes les recherches (Total), achat ou location.
2. Explorez les **graphiques d'évolution** pour identifier les pics de demande ou les tendances à long terme.
""")
        
# Page d'affichage de la liste de prospects
def map():
    st.markdown("""
## Plongez au cœur des recherches pour des locaux commerciaux avec la carte interactive 🗺️📊

Cette interface vous offre une **vision géographique détaillée** des tendances de recherche pour des locaux commerciaux partout en France 🇫🇷. Grâce à notre carte interactive, vous pouvez explorer les **volumes de recherche**, l’**intérêt relatif** et l’**évolution entre 2023 et 2024** pour chaque région et ville.
""")

    col1, col2, col3 = st.columns(3)
    col1.metric("Villes analysées", "+ 2 500")
    col2.metric("Recherches en ligne étudiées", "+ 1.5M")
    col3.metric("Période étudiée", "4 ans")

    option_1 = st.pills(
        "Sélectionnez le type de recherche à analyser :",
        ["Toutes les recherches concernant un local commercial", "Achat d'un local commercial", "Location d'un local commercial"],
        default = "Toutes les recherches concernant un local commercial"
    )

    option_2 = st.pills(
        "Choisissez un indicateur :",
        ["📊 Volumes de recherches", "👍 Proportion d'interet", "📈 Evolution des recherches entre 2023 et 2024"],
        default = "📊 Volumes de recherches"
    )

    dict_equiv = {
        "Toutes les recherches concernant un local commercial" : "total", 
        "Achat d'un local commercial":"achat", 
        "Location d'un local commercial":"location",
        "📊 Volumes de recherches":"vabs", 
        "👍 Proportion d'interet":"index", 
        "📈 Evolution des recherches entre 2023 et 2024":"evol_23vs24"
    }

    map_file = f"maps/map_{dict_equiv[option_2]}_{dict_equiv[option_1]}.html"

    # Chargement et affichage de la carte
    with open(map_file, "r") as f:
        st.components.v1.html(f.read(), height=600)

    st.markdown("""
#### 🌟 Que pouvez-vous découvrir sur la carte ?
1. **Volumes de recherche** : Identifiez les zones avec le plus grand nombre de recherches pour des locaux commerciaux. Les grandes agglomérations comme **Paris**, **Lyon** et **Marseille** affichent des volumes impressionnants. 🏙️
2. **Intérêt relatif** : Analysez l’intérêt local en comparant le nombre de recherches au **nombre d’habitants**. Certaines petites villes comme **Gruissan** ou **Arcachon** présentent un **fort intérêt proportionnel**. 📈

#### 🛠️ Comment utiliser cette interface ?
1. **Choisissez un indicateur** : Volumes de recherche, intérêt relatif, ou évolution annuelle.
2. Zoomez et déplacez-vous sur la carte pour explorer les données par région ou par ville.
3. Cliquez sur une zone pour obtenir des informations détaillées.

#### 🔍 Pourquoi cette carte est-elle utile ?
- Identifiez rapidement les **zones les plus dynamiques**.
- Comparez l’attractivité des villes et des régions en fonction de plusieurs critères.
- Suivez les tendances émergentes pour anticiper les opportunités commerciales.

#### 🚀 À vous de jouer !
Naviguez, explorez, et laissez la **donnée géolocalisée** vous guider dans vos décisions. Cette carte interactive a été conçue pour être **simple d’utilisation**, mais aussi **puissante et riche en insights**. Bonne exploration ! 🎯🌍
""")
      

# Logique principale de l'application
def main():
    page = sidebar_navigation()
    
    if page == "Accueil":
        home_page()
    elif page == "Dashboard de tendances":
        dashboard()
    elif page == "Explorez sur la carte":
        map()

if __name__ == "__main__":
    main()
