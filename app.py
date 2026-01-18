import streamlit as st
import pandas as pd
import numpy as np
import os

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Pokédex",
    layout="wide"
)

# --------------------------------------------------
# DATA LOADING & CLEANING
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("pokemon.csv")

    # Remove Mega Evolutions
    df = df[~df["Name"].str.contains("Mega", case=False, na=False)]

    # Clean data
    df["Type 2"] = df["Type 2"].fillna("None")
    df = df.drop(columns=["Total"])

    # Ensure ID is numeric
    df["#"] = pd.to_numeric(df["#"])

    stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    df[stats] = df[stats].apply(pd.to_numeric)

    # Feature engineering
    df["total_stats"] = df[stats].sum(axis=1)

    return df, stats


pokedex, stats = load_data()

# --------------------------------------------------
# IMAGE HANDLER (ID BASED)
# --------------------------------------------------
def get_pokemon_image_by_id(pokemon_id):
    image_path = f"images/{pokemon_id}.jpg"
    if os.path.exists(image_path):
        return image_path
    else:
        return "images/placeholder.jpg"


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------
st.sidebar.title("🧭 Pokédex Menu")

page = st.sidebar.radio(
    "Choose a section:",
    ["Search Pokémon", "Rankings", "Visualizations"]
)

# --------------------------------------------------
# SEARCH PAGE
# --------------------------------------------------
if page == "Search Pokémon":
    st.title("🔍 Search Pokémon")

    # Step 1: Text input (user types here)
    query = st.text_input(
        "Start typing Pokémon name:",
        placeholder="e.g. pika, char, bulba..."
    )

    # Step 2: Filter Pokémon live
    if query:
        filtered = pokedex[
            pokedex["Name"].str.contains(query, case=False)
        ]

        if filtered.empty:
            st.warning("No Pokémon found.")
        else:
            # Step 3: Dynamic dropdown (autocomplete feel)
            selected = st.selectbox(
                "Select Pokémon from suggestions:",
                filtered["Name"].values
            )

            pokemon = filtered[filtered["Name"] == selected].iloc[0]
            pokemon_id = int(pokemon["#"])

            col1, col2 = st.columns([1, 2])

            with col1:
                image_path = get_pokemon_image_by_id(pokemon_id)
                if image_path:
                    st.image(image_path, width="stretch")
                else:
                    st.warning("Image not available")

            with col2:
                st.subheader(pokemon["Name"])
                st.write(f"**Pokédex ID:** {pokemon_id}")
                st.write(f"**Type 1:** {pokemon['Type 1']}")
                st.write(f"**Type 2:** {pokemon['Type 2']}")

                st.markdown("### 📊 Stats")
                st.dataframe(
                    pokemon[
                        ["HP", "Attack", "Defense",
                         "Sp. Atk", "Sp. Def", "Speed",
                         "total_stats"]
                    ],
                    use_container_width=True
                )

# --------------------------------------------------
# RANKINGS PAGE
# --------------------------------------------------

elif page == "Rankings":
    st.title("🏆 Pokémon Rankings")

    ranking_metric = st.selectbox(
        "Rank Pokémon by:",
        ["Total Stats", "Attack", "Defense", "Speed", "Power Score"]
    )

    sort_order = st.radio(
        "Sort order:",
        ["Highest → Lowest", "Lowest → Highest"],
        horizontal=True
    )

    ascending = sort_order == "Lowest → Highest"

    type_options = ["All"] + sorted(pokedex["Type 1"].unique().tolist())
    selected_type = st.selectbox("Filter by Type:", type_options)

    top_n = st.slider(
        "How many Pokémon to show?",
        min_value=5,
        max_value=50,
        value=10
    )

    if ranking_metric == "Total Stats":
        ranked = pokedex.sort_values("total_stats", ascending=ascending)
        columns = ["#", "Name", "Type 1", "total_stats"]

    elif ranking_metric == "Attack":
        ranked = pokedex.sort_values("Attack", ascending=ascending)
        columns = ["#", "Name", "Type 1", "Attack"]

    elif ranking_metric == "Defense":
        ranked = pokedex.sort_values("Defense", ascending=ascending)
        columns = ["#", "Name", "Type 1", "Defense"]

    elif ranking_metric == "Speed":
        ranked = pokedex.sort_values("Speed", ascending=ascending)
        columns = ["#", "Name", "Type 1", "Speed"]

    elif ranking_metric == "Power Score":
        ranked = pokedex.sort_values("power_score", ascending=ascending)
        columns = ["#", "Name", "Type 1", "power_score"]

    if selected_type != "All":
        ranked = ranked[ranked["Type 1"] == selected_type]

    def highlight_top_3(row):
        if row.name < 3:
            return ["background-color: #ffd700"] * len(row)
        return [""] * len(row)

    st.subheader(f"Top {top_n} Pokémon by {ranking_metric}")

    st.dataframe(
        ranked[columns]
        .head(top_n)
        .style.apply(highlight_top_3, axis=1),
        use_container_width=True
    )

    selected_from_ranking = st.selectbox(
        "View details for Pokémon:",
        ranked["Name"].head(top_n).values
    )

    pokemon = pokedex[pokedex["Name"] == selected_from_ranking].iloc[0]
    pokemon_id = int(pokemon["#"])

    st.markdown("---")
    st.subheader("🔍 Pokémon Details")

    col1, col2 = st.columns([1, 2])

    with col1:
        image_path = get_pokemon_image_by_id(pokemon_id)
        if image_path:
            st.image(image_path, width="stretch")
        else:
            st.warning("Image not available")

    with col2:
        st.write(f"**Pokédex ID:** {pokemon_id}")
        st.write(f"**Type 1:** {pokemon['Type 1']}")
        st.write(f"**Type 2:** {pokemon['Type 2']}")

        st.markdown("### 📊 Stats")
        st.dataframe(
            pokemon[
                ["HP", "Attack", "Defense",
                 "Sp. Atk", "Sp. Def", "Speed",
                 "total_stats", "power_score"]
            ],
            use_container_width=True
        )


# --------------------------------------------------
# VISUALIZATIONS PAGE (PLACEHOLDER FOR NOW)
# --------------------------------------------------
elif page == "Visualizations":
    st.title("📊 Pokémon Visualizations")
    st.info("Visualizations will be added next 👀")
