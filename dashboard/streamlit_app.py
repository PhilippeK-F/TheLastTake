import sys
sys.path.insert(0, '..')

import pandas as pd
import streamlit as st

from src.loaders.load_csv import load_csv
from src.analysis.clean import clean
from src.analysis.analyze import (
    compute_kpis,
    films_par_statut,
    evolution_carriere,
    top_films_par_personne,
    films_par_cas,
    note_avant_apres_pic,
    films_par_decennie,
)
from src.analysis.visualize import (
    plot_evolution_carriere,
    plot_note_par_statut,
    plot_films_par_cas,
    plot_comparaison_personnes,
    plot_decennie,
    plot_scatter_note_annee,
)

st.set_page_config(
    page_title="TheLastTake",
    page_icon="🎬",
    layout="wide",
)

st.title("TheLastTake")
st.markdown("Analyse des carrières cinématographiques : ascension, apogée et disparition (1980–2024)")

@st.cache_data
def load_data() -> pd.DataFrame:
    return load_csv("/app/data/processed/thelasttake_clean.csv")

df_raw = load_data()
df = clean(df_raw)

# ---------------------------------------------------------------------------
# Sidebar — filtres
# ---------------------------------------------------------------------------
st.sidebar.header("Filtres")

personnes = sorted(df["personne"].dropna().unique().tolist())
selected_personnes = st.sidebar.multiselect("Personne", options=personnes, default=personnes)
df = df[df["personne"].isin(selected_personnes)]

cas = df["cas"].dropna().unique().tolist()
selected_cas = st.sidebar.multiselect("Type de cas", options=cas, default=cas)
df = df[df["cas"].isin(selected_cas)]

types = df["type_personne"].dropna().unique().tolist()
selected_types = st.sidebar.multiselect("Type", options=types, default=types)
df = df[df["type_personne"].isin(selected_types)]

decennies = sorted(df["decennie"].dropna().unique().tolist())
selected_decennies = st.sidebar.multiselect("Décennie", options=decennies, default=decennies)
df = df[df["decennie"].isin(selected_decennies)]

# ---------------------------------------------------------------------------
# KPIs
# ---------------------------------------------------------------------------
st.subheader("Indicateurs clés")
kpis = compute_kpis(df)
cols = st.columns(len(kpis))
for col, (label, value) in zip(cols, kpis.items()):
    col.metric(label=label, value=value)

st.divider()

# ---------------------------------------------------------------------------
# Onglets
# ---------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Carrières", "Comparaisons", "Données brutes"])

with tab1:
    st.subheader("Évolution d'une carrière")
    personne_select = st.selectbox("Choisir une personne", options=personnes)
    fig = plot_evolution_carriere(df, personne_select)
    st.pyplot(fig)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Note moyenne par statut de carrière")
        fig = plot_note_par_statut(df)
        st.pyplot(fig)
    with col2:
        st.subheader("Films par décennie")
        fig = plot_decennie(df)
        st.pyplot(fig)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Note moyenne par personne")
        fig = plot_comparaison_personnes(df)
        st.pyplot(fig)
    with col2:
        st.subheader("Films par type de cas")
        fig = plot_films_par_cas(df)
        st.pyplot(fig)

    st.divider()

    st.subheader("Notes dans le temps par type de cas")
    fig = plot_scatter_note_annee(df)
    st.pyplot(fig)

with tab3:
    cols_display = ["personne", "film", "annee", "note_tmdb",
                    "nb_votes_tmdb", "cas", "franchise_cle",
                    "statut_carriere", "decennie"]
    st.dataframe(df[cols_display].sort_values(["personne", "annee"]),
                 use_container_width=True)

    with st.expander("Voir toutes les colonnes"):
        st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Télécharger CSV", csv, "thelasttake_export.csv", "text/csv")