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
        'Frais fixes mensuels (€)': frais_fixes,
        'Frais variables mensuels (€)': frais_variables
    })

# Interface utilisateur pour ajouter des logements
st.title("Comparaison des coûts cumulés des logements")
st.header("Ajouter un logement")

nom = st.text_input("Nom du logement", value=f"Logement {len(st.session_state['logements']) + 1}")
frais_fixes = st.number_input("Frais fixes mensuels (€)", min_value=0.0, value=0.0, step=0.01)
frais_variables = st.number_input("Frais variables mensuels (€)", min_value=0.0, value=1000.0, step=0.01)

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
        # Création d'une série de frais mensuels appliqués chaque mois
        frais_fixes_series = pd.Series(logement['Frais fixes mensuels (€)'], 
                                       index=pd.date_range(start=date_debut, end=date_fin, freq='MS')).reindex(index_temps, method='ffill').fillna(0)
        
        # Création d'une série de frais variables journaliers
        frais_variables_series = pd.Series(logement['Frais variables mensuels (€)'], 
                                           index=pd.date_range(start=date_debut, end=date_fin, freq='MS')).reindex(index_temps, method='ffill').fillna(0)
        
        # Coût cumulé = Somme des frais fixes mensuels et des frais variables mensuels
        cout_cumule = frais_fixes_series.cumsum() + frais_variables_series.cumsum()
        
        df_cout_cumule[logement['Nom']] = cout_cumule

    # Tracé interactif avec Plotly
    fig = px.line(df_cout_cumule, x=df_cout_cumule.index, y=df_cout_cumule.columns, title="Comparaison des coûts cumulés des logements")
    st.plotly_chart(fig)

else:
    st.write("Aucun logement n'a été ajouté pour le moment.")