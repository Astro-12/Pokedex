import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Pokédex", layout="wide")

# --------------------------------------------------
# DATA LOADING & CLEANING
# --------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("pokemon.csv")

    # Remove Mega Evolutions
    df = df[~df["Name"].str.contains("Mega", case=False, na=False)]

    df["Type 2"] = df["Type 2"].fillna("None")
    df = df.drop(columns=["Total"])

    df["#"] = pd.to_numeric(df["#"])    

    df = df.drop_duplicates(subset="#", keep="first")

    stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    df[stats] = df[stats].apply(pd.to_numeric)

    # Total stats
    df["total_stats"] = df[stats].sum(axis=1)

    # Power score
    weights = np.array([1.0, 1.3, 1.2, 1.4, 1.3, 1.1])
    df["power_score"] = df[stats].values @ weights

    return df, stats


pokedex, stats = load_data()

# --------------------------------------------------
# IMAGE HANDLER (ID BASED)
# --------------------------------------------------
def get_pokemon_image_by_id(pokemon_id):
    path = f"images/{pokemon_id}.jpg"
    return path if os.path.exists(path) else None

# --------------------------------------------------
# NORMALIZATION
# --------------------------------------------------
def normalize_stats(df, stat_cols):
    return (df[stat_cols] - df[stat_cols].min()) / (
        df[stat_cols].max() - df[stat_cols].min()
    )

# --------------------------------------------------
# RADAR CHART
# --------------------------------------------------
def radar_chart(labels, values_a, values_b, label_a, label_b):
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    values_a = np.append(values_a, values_a[0])
    values_b = np.append(values_b, values_b[0])

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))

    ax.plot(angles, values_a, linewidth=2, label=label_a)
    ax.fill(angles, values_a, alpha=0.25)

    ax.plot(angles, values_b, linewidth=2, label=label_b)
    ax.fill(angles, values_b, alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title("Radar Stat Comparison", pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.4, 1.2))

    return fig

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
st.sidebar.title("🧭 Pokédex Menu")
page = st.sidebar.radio("Choose a section:", ["Search Pokémon", "Rankings","Compare"])

# --------------------------------------------------
# SEARCH PAGE
# --------------------------------------------------
if page == "Search Pokémon":
    st.title("🔍 Search Pokémon")

    query = st.text_input("Start typing Pokémon name:")

    if query:
        filtered = pokedex[pokedex["Name"].str.contains(query, case=False)]

        if filtered.empty:
            st.warning("No Pokémon found.")
        else:
            selected = st.selectbox("Select Pokémon:", filtered["Name"].values)
            pokemon = filtered[filtered["Name"] == selected].iloc[0]
            pid = int(pokemon["#"])

            col1, col2 = st.columns([1, 2])

            with col1:
                img = get_pokemon_image_by_id(pid)
                if img:
                    st.image(img, width="stretch")
                else:
                    st.info("No image")

            with col2:
                st.subheader(pokemon["Name"])
                st.write(f"Type 1: {pokemon['Type 1']}")
                st.write(f"Type 2: {pokemon['Type 2']}")

                with st.expander("📊 View stat radar"):
                    radar_stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
                    fig = radar_chart(
                        radar_stats,
                        pokemon[radar_stats].values,
                        pokemon[radar_stats].values,
                        pokemon["Name"],
                        pokemon["Name"]
                    )
                    st.pyplot(fig, use_container_width=False)

# --------------------------------------------------
# RANKINGS PAGE
# --------------------------------------------------
elif page == "Rankings":
    st.title("🏆 Pokémon Rankings")

    metric = st.selectbox(
        "Rank by:",
        ["Total Stats", "Attack", "Defense", "Speed", "Power Score"]
    )

    ascending = st.radio(
        "Order:",
        ["Highest → Lowest", "Lowest → Highest"],
        horizontal=True
    ) == "Lowest → Highest"

    top_n = st.slider("How many Pokémon?", 5, 30, 10)

    ranked = pokedex.copy()

    if metric == "Total Stats":
        ranked = ranked.sort_values("total_stats", ascending=ascending)
        value_col = "total_stats"
    elif metric == "Attack":
        ranked = ranked.sort_values("Attack", ascending=ascending)
        value_col = "Attack"
    elif metric == "Defense":
        ranked = ranked.sort_values("Defense", ascending=ascending)
        value_col = "Defense"
    elif metric == "Speed":
        ranked = ranked.sort_values("Speed", ascending=ascending)
        value_col = "Speed"
    else:
        ranked = ranked.sort_values("power_score", ascending=ascending)
        value_col = "power_score"

    st.dataframe(
        ranked[["#", "Name", "Type 1", value_col]].head(top_n),
        use_container_width=True
    )

    # --------------------------------------------------
    # CARD GRID
    # --------------------------------------------------
    st.markdown("## 🧩 Top Pokémon Cards")

    cards = ranked.head(top_n)
    cols = st.columns(5)

    for i, (_, row) in enumerate(cards.iterrows()):
        with cols[i % 5]:
            img = get_pokemon_image_by_id(int(row["#"]))
            if img:
                st.image(img, width="stretch")
            st.markdown(f"**{row['Name']}**")
            st.caption(row["Type 1"])

    # --------------------------------------------------
    # COMPARISON
    # --------------------------------------------------
    st.markdown("---")
    st.subheader("📊 Compare Pokémon")

    names = ranked["Name"].head(top_n).values

    colA, colB = st.columns(2)
    with colA:
        p1 = st.selectbox("Pokémon A", names, key="a")
    with colB:
        p2 = st.selectbox("Pokémon B", names, key="b")

    normalize = st.checkbox("⚖️ Normalize stats", value=True)

    poke_a = pokedex[pokedex["Name"] == p1].iloc[0]
    poke_b = pokedex[pokedex["Name"] == p2].iloc[0]

    radar_stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]

    if normalize:
        norm = normalize_stats(pokedex, radar_stats)
        vals_a = norm.loc[poke_a.name, radar_stats].values
        vals_b = norm.loc[poke_b.name, radar_stats].values
    else:
        vals_a = poke_a[radar_stats].values
        vals_b = poke_b[radar_stats].values

    fig = radar_chart(
        radar_stats,
        vals_a,
        vals_b,
        poke_a["Name"],
        poke_b["Name"]
    )

    st.pyplot(fig, use_container_width=False)
