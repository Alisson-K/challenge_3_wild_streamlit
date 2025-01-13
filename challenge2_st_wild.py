import streamlit as st
import pandas as pd 
from datetime import date
from datetime import time
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu

# Sécurisation de notre streamlit 

# Nos données utilisateurs doivent respecter ce format
lesDonneesDesComptes = {'usernames': {'utilisateur': {'name': 'utilisateur',
   'password': 'utilisateurMDP',
   'email': 'utilisateur@gmail.com',
   'failed_login_attemps': 0, # Sera géré automatiquement
   'logged_in': False, # Sera géré automatiquement
   'role': 'utilisateur'},
  'root': {'name': 'root',
   'password': 'rootMDP',
   'email': 'admin@gmail.com',
   'failed_login_attemps': 0, # Sera géré automatiquement
   'logged_in': False, # Sera géré automatiquement
   'role': 'administrateur'}}}

authenticator = Authenticate(
    lesDonneesDesComptes, # Les données des comptes
    "cookie name", # Le nom du cookie, un str quelconque
    "cookie key", # La clé du cookie, un str quelconque
    30, # Le nombre de jours avant que le cookie expire 
)

authenticator.login()

def accueil():
      st.title("Bienvenu sur le contenu réservé aux utilisateurs connectés")


if st.session_state["authentication_status"]:
  accueil()
  # Le bouton de déconnexion
  authenticator.logout("Déconnexion")

elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être remplie')

# Faire un menu intéractif pour accéder à l'ensemble des sections de notre application

# Création du menu qui va afficher les choix qui se trouvent dans la variable options
selection = option_menu(
            menu_title=None,
            options = ["Accueil", "Photos"]
        )

# On indique au programme quoi faire en fonction du choix
if selection == "Accueil":
    st.write("Bienvenue sur la page d'accueil !")
elif selection == "Photos":
    st.write("Bienvenue sur mon album photo")
# ... et ainsi de suite pour les autres pages

# Charger les datasets seaborn
flights = sns.load_dataset('flights')
iris = sns.load_dataset('iris')
penguins = sns.load_dataset('penguins')

st.title("Manipulation de données et création de graphiques")

st.write('___')

# Dictionnaire des dataset 

dataset = st.selectbox("Quel dataset veux tu utiliser ? : ",
['flights','iris','penguins'])

st.write(f"Tu as choisis : {dataset}")

# Affichage dynamique des datasets en fonction de la sélection
if dataset == 'flights':
    st.dataframe(flights)
elif dataset == 'iris':
    st.dataframe(iris)
elif dataset == 'penguins':
    st.dataframe(penguins)

# Sélection du dataset
if dataset == 'flights':
    data = flights
elif dataset == 'iris':
    data = iris
elif dataset == 'penguins':
    data = penguins

# Filtrer les colonnes numériques
numeric_columns = data.select_dtypes(include=['number']).columns

# Vérifier s'il y a des colonnes numériques
if len(numeric_columns) > 1:
    # Sélection des colonnes X et Y
    x_col = st.selectbox("Choisissez la colonne X :", numeric_columns)
    y_col = st.selectbox("Choisissez la colonne Y :", numeric_columns)

    # Choix du type de graphique
    chart_type = st.selectbox("Choisissez un type de graphique :", ["scatter_chart", "bar_chart", "line_chart"])

    # Affichage du graphique
    st.write(f"**Graphique {chart_type}** entre **{x_col}** et **{y_col}** :")
    if chart_type == "scatter_chart":
        st.scatter_chart(data[[x_col, y_col]])
    elif chart_type == "bar_chart":
        st.bar_chart(data[[x_col, y_col]].set_index(x_col))
    elif chart_type == "line_chart":
        st.line_chart(data[[x_col, y_col]].set_index(x_col))

    # Afficher la matrice de corrélation
    if st.checkbox("Afficher la matrice de corrélation des colonnes numériques"):
        st.write("**Matrice de corrélation :**")
        correlation_matrix = data[numeric_columns].corr()
        st.dataframe(correlation_matrix)

        # Heatmap de la matrice de corrélation
        st.write("**Heatmap de la matrice de corrélation :**")
        fig, ax = plt.subplots()
        sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        st.pyplot(fig)
else:
    st.warning("Le dataset sélectionné ne contient pas suffisamment de colonnes numériques pour créer un graphique ou une matrice de corrélation.")