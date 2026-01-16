import streamlit as st
import pandas as pd
import numpy as np

st.sidebar.title("Pokédex Menu")

page = st.sidebar.radio(
    "Choose a section:",
    ["Search Pokemon", "Rankings", "Visualizations"]
)

@st.cache_data
def load_data():
    df = pd.read_csv("pokemon.csv")
    df["Type 2"] = df["Type 2"].fillna("None")
    df = df.drop(columns=["Total"])

    stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    df[stats] = df[stats].apply(pd.to_numeric)

    df["total_stats"] = df[stats].sum(axis=1)
    return df, stats

pokedex, stats = load_data()

# SEARCH PAGE
if page == "Search Pokemon":
    st.title("🔍 Search Pokémon")

    query = st.text_input("Enter Pokémon name:")

    if query:
        results = pokedex[pokedex["Name"].str.contains(query, case=False)]

        if results.empty:
            st.warning("No Pokémon found.")
        else:
            selected = st.selectbox(
                "Select Pokémon",
                results["Name"]
            )

            pokemon = results[results["Name"] == selected].iloc[0]

            st.subheader(selected)
            st.write(pokemon)

#RANKINGS PAGE
elif page == "Rankings":
    st.title("🏆 Pokémon Rankings")
    st.write("Choose how you want to rank Pokémon")
    
    ranking_metric = st.selectbox(
        "Rank Pokémon by:",
        ["Total Stats", "Attack", "Defense", "Speed"]
    )

    top_n = st.slider(
        "How many Pokémon to show?",
        min_value=5,
        max_value=50,
        value=10
    )
    if ranking_metric == "Total Stats":
        ranked = pokedex.sort_values("total_stats", ascending=False)
        columns = ["Name", "Type 1", "total_stats"]

    elif ranking_metric == "Attack":
        ranked = pokedex.sort_values("Attack", ascending=False)
        columns = ["Name", "Type 1", "Attack"]

    elif ranking_metric == "Defense":
        ranked = pokedex.sort_values("Defense", ascending=False)
        columns = ["Name", "Type 1", "Defense"]

    elif ranking_metric == "Speed":
        ranked = pokedex.sort_values("Speed", ascending=False)
        columns = ["Name", "Type 1", "Speed"]

    st.subheader(f"Top {top_n} Pokémon by {ranking_metric}")
    st.dataframe(
        ranked[columns].head(top_n),
        use_container_width=True
    )
# VISUALIZATIONS PAGE 
elif page == "Visualizations":
    st.title("📊 Pokémon Visualizations")
    st.info("Visualizations page coming next 📈")
