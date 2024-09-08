import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Initialisation des logements dans la session Streamlit
if 'logements' not in st.session_state:
    st.session_state['logements'] = []

# Ajout d'un logement
def ajouter_logement(nom, frais_fixes, frais_variables):
    st.session_state['logements'].append({
        'Nom': nom,
        'Frais d\'agence (€)': frais_fixes,  # Frais fixes = Frais d'agence (ordonnée à l'origine)
        'Loyer mensuel (€)': frais_variables  # Frais variables = Loyer mensuel
    })

# Interface utilisateur pour ajouter des logements
st.title("Comparaison des coûts cumulés des logements")
st.header("Ajouter un logement")

nom = st.text_input("Nom du logement", value=f"Logement {len(st.session_state['logements']) + 1}")
frais_fixes = st.number_input("Frais d'agence (€)", min_value=0.0, value=0.0, step=0.01)
frais_variables = st.number_input("Loyer mensuel (€)", min_value=0.0, value=1000.0, step=0.01)

if st.button("Ajouter le logement"):
    ajouter_logement(nom, frais_fixes, frais_variables)

# Conversion des données en DataFrame
df_logements = pd.DataFrame(st.session_state['logements'])

if not df_logements.empty:
    st.write("Logements ajoutés :")
    st.dataframe(df_logements)

    # Dates par défaut pour la simulation
    date_debut = pd.to_datetime("2024-10-21")
    date_fin = pd.to_datetime("2026-12-31")

    # Générer l'index datetime avec un pas journalier
    index_temps = pd.date_range(start=date_debut, end=date_fin, freq='D')

    # Calcul du coût cumulé pour chaque logement
    df_cout_cumule = pd.DataFrame(index=index_temps)

    for i, logement in df_logements.iterrows():
        # Frais d'agence ajoutés une seule fois à t=0 (ordonnée à l'origine)
        frais_agence = logement['Frais d\'agence (€)']
        
        # Frais variables mensuels (loyer) appliqués chaque mois
        frais_mensuels_series = pd.Series(logement['Loyer mensuel (€)'], 
                                          index=pd.date_range(start=date_debut, end=date_fin, freq='MS')).reindex(index_temps, method='ffill').fillna(0)

        # Calcul du coût cumulé : frais d'agence (une fois) + loyer cumulé à chaque mois
        cout_cumule = frais_agence + frais_mensuels_series.cumsum()

        # Ajouter la courbe du logement dans le DataFrame
        df_cout_cumule[logement['Nom']] = cout_cumule

    # Tracé interactif avec Plotly
    fig = px.line(df_cout_cumule, x=df_cout_cumule.index, y=df_cout_cumule.columns, title="Comparaison des coûts cumulés des logements")
    st.plotly_chart(fig)

else:
    st.write("Aucun logement n'a été ajouté pour le moment.")