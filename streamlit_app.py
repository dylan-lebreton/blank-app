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
        'Frais variables journaliers (€)': frais_variables / 30  # Conversion mensuelle en journalière
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

    # Définir les dates par défaut
    date_debut = pd.to_datetime("2024-10-21")
    date_fin = pd.to_datetime("2026-12-31")

    # Générer l'index datetime basé sur un pas de temps journalier
    index_temps = pd.date_range(start=date_debut, end=date_fin, freq='D')

    # Calcul du coût cumulé pour chaque logement
    df_cout_cumule = pd.DataFrame(index=index_temps)
    for i, logement in df_logements.iterrows():
        cout_cumule = logement['Frais fixes (€)'] + logement['Frais variables journaliers (€)'] * np.arange(len(index_temps))
        df_cout_cumule[logement['Nom']] = cout_cumule

    # Tracé interactif avec Plotly
    fig = px.line(df_cout_cumule, x=df_cout_cumule.index, y=df_cout_cumule.columns, title="Comparaison des coûts cumulés des logements")
    st.plotly_chart(fig)

else:
    st.write("Aucun logement n'a été ajouté pour le moment.")