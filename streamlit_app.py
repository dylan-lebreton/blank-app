import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Initialisation de la liste des logements
logements = []

# Ajout d'un logement
def ajouter_logement(nom, frais_fixes, frais_variables):
    logements.append({
        'Nom': nom,
        'Frais fixes (€)': frais_fixes,
        'Frais variables mensuels (€)': frais_variables
    })

# Interface utilisateur pour ajouter des logements
st.title("Comparaison des coûts cumulés des logements")
st.header("Ajouter un logement")

nom = st.text_input("Nom du logement", value=f"Logement {len(logements) + 1}")
frais_fixes = st.number_input("Frais fixes (€)", min_value=0.0, value=0.0, step=0.01)
frais_variables = st.number_input("Frais variables mensuels (€)", min_value=0.0, value=1000.0, step=0.01)

if st.button("Ajouter le logement"):
    ajouter_logement(nom, frais_fixes, frais_variables)

# Conversion des données en DataFrame
df_logements = pd.DataFrame(logements)

if not df_logements.empty:
    st.write("Logements ajoutés :")
    st.dataframe(df_logements)

    # Choix de la date de début et de fin
    date_debut = st.date_input("Date de début", value=pd.Timestamp.today())
    date_fin = st.date_input("Date de fin", value=pd.Timestamp.today() + pd.DateOffset(months=60))

    # Choix du pas de temps
    pas_de_temps = st.selectbox("Choisissez le pas de temps", ["Jour", "Semaine", "Mois", "Année"])

    # Mapping des fréquences pour Pandas
    freq_mapping = {"Jour": "D", "Semaine": "W", "Mois": "M", "Année": "A"}

    # Générer l'index datetime basé sur le pas de temps choisi
    index_temps = pd.date_range(start=date_debut, end=date_fin, freq=freq_mapping[pas_de_temps])

    # Calcul du coût cumulé pour chaque logement
    df_cout_cumule = pd.DataFrame(index=index_temps)
    for i, logement in df_logements.iterrows():
        cout_cumule = logement['Frais fixes (€)'] + logement['Frais variables mensuels (€)'] * np.arange(len(index_temps))
        df_cout_cumule[logement['Nom']] = cout_cumule

    # Tracé interactif avec Plotly
    fig = px.line(df_cout_cumule, x=df_cout_cumule.index, y=df_cout_cumule.columns, title="Comparaison des coûts cumulés des logements")
    st.plotly_chart(fig)

else:
    st.write("Aucun logement n'a été ajouté pour le moment.")