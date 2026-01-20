import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Pokédex",
    layout="wide"
)

# ==================================================
# DATA LOADING
# ==================================================
@st.cache_data
def load_data():
    """
    Loads the cleaned Pokémon dataset.

    REQUIRED CSV COLUMNS:
    - #
    - Name
    - base_name   -> canonical Pokémon name (e.g. Charizard)
    - form        -> 'base', 'Mega Charizard X', 'Normal Forme', etc.

    IMPORTANT:
    We NEVER infer forms from Name.
    The CSV decides everything.
    """

    df = pd.read_csv("pokemon_cleaned.csv")

    # Safety cleaning
    df["Type 2"] = df["Type 2"].fillna("None")
    df["base_name"] = df["base_name"].fillna("")
    df["form"] = df["form"].fillna("base")

    df["#"] = pd.to_numeric(df["#"], errors="coerce")

    stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    df[stats] = df[stats].apply(pd.to_numeric, errors="coerce")

    # Derived stats
    df["total_stats"] = df[stats].sum(axis=1)

    weights = np.array([1.0, 1.3, 1.2, 1.4, 1.3, 1.1])
    df["power_score"] = df[stats].values @ weights

    # Base Pokémon only (used when toggle is OFF)
    base_df = df[
    (df["form"] == "base") &
    (df["Name"] == df["base_name"]) &
    (df["image_file"] == df["#"].astype(int).astype(str) + ".jpg")
].copy()

    return base_df, df, stats

def comparison_bar_chart(stats, df):
    """
    Grouped bar chart for multiple Pokémon comparison
    """
    fig, ax = plt.subplots(figsize=(5, 4))

    x = np.arange(len(stats))
    width = 0.8 / len(df)

    for i, (_, row) in enumerate(df.iterrows()):
        ax.bar(
            x + i * width,
            row[stats].values,
            width,
            label=row["Name"]
        )

    ax.set_xticks(x + width * (len(df) - 1) / 2)
    ax.set_xticklabels(stats, rotation=45, ha="right")
    ax.set_ylabel("Stat Value")
    ax.set_title("Stat Comparison (Bar Chart)")
    ax.legend(fontsize=8)

    return fig
base_df, full_df, STATS = load_data()

# ==================================================
# FORM NORMALIZATION (CRITICAL)
# ==================================================
def normalize_form_for_image(form: str) -> str:
    """
    Converts CSV form names into image-safe filenames.

    Examples:
    - 'Normal Forme' -> 'normal'
    - 'Attack Forme' -> 'attack'
    - 'Mega Charizard X' -> 'mega-x'
    - 'Therian Forme' -> 'therian'
    """

    if form == "base":
        return "base"

    form = form.lower()
    form = form.replace("forme", "")
    form = form.replace("form", "")
    form = form.replace("mega", "mega")
    form = form.strip()

    replacements = {
    # Deoxys
    "normal": "normal",
    "attack": "attack",
    "defense": "defense",
    "speed": "speed",

    # Forces of Nature
    "therian": "therian",
    "incarnate": "incarnate",

    # Shaymin
    "land": "land",
    "sky": "sky",

    # Kyurem
    "black": "black",
    "white": "white",

    # Mega
    "mega x": "mega-x",
    "mega y": "mega-y",
    "x": "mega-x",
    "y": "mega-y"
}

    for key, val in replacements.items():
        if key in form:
            return val

    return form.replace(" ", "-")


# ==================================================
# IMAGE HANDLER
# ==================================================
def get_pokemon_image(pokemon_id, form):
    """
    Universal image resolver.

    Rules:
    - Base: images/{id}.jpg
    - Form: images/{id}-{normalized_form}.jpg
    """

    if form != "base":
        form_slug = normalize_form_for_image(form)
        form_path = f"images/{pokemon_id}-{form_slug}.jpg"
        if os.path.exists(form_path):
            return form_path

    base_path = f"images/{pokemon_id}.jpg"
    if os.path.exists(base_path):
        return base_path

    return "images/placeholder.jpg"


# ==================================================
# VISUALIZATION FUNCTIONS
# ==================================================
def radar_chart(labels, values_list, names):
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    angles = np.append(angles, angles[0])

    # SMALLER FIGURE
    fig, ax = plt.subplots(
        figsize=(3, 3),   # 👈 key change
        subplot_kw=dict(polar=True)
    )

    for values, name in zip(values_list, names):
        values = np.append(values, values[0])
        ax.plot(angles, values, linewidth=2, label=name)
        ax.fill(angles, values, alpha=0.15)

    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_title("Stat Radar", fontsize=12)
    ax.tick_params(labelsize=9)

    ax.legend(
        loc="upper right",
        bbox_to_anchor=(1.25, 1.15),
        fontsize=8
    )

    return fig



def bar_chart(stats, values, name):
    """Simple bar chart"""

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.bar(stats, values)
    ax.set_title(name)
    ax.set_ylabel("Stat Value")
    ax.set_xticks(range(len(stats)))
    ax.set_xticklabels(stats, rotation=45, ha="right")

    return fig


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================
st.sidebar.title("🧭 Pokédex Menu")

page = st.sidebar.radio(
    "Navigate",
    ["Search Pokémon", "Rankings", "Pokémon Comparison"]
)

# ==================================================
# SEARCH POKÉMON PAGE
# ==================================================
if page == "Search Pokémon":
    st.title("Search Pokémon")

    include_forms = st.toggle("Include Mega / Alternate Forms")

    # IMPORTANT:
    # When toggle is OFF → ONLY base_df
    # When toggle is ON  → full_df
    data = full_df if include_forms else base_df

    query = st.text_input("Start typing Pokémon name")

    if query:
        filtered = data[
            data["base_name"].str.contains(query, case=False, na=False)
        ]

        if not filtered.empty:
            selected_base = st.selectbox(
                "Select Pokémon",
                sorted(filtered["base_name"].unique())
            )

            # FORMS LOGIC (THIS FIXES YOUR BUG)
            if include_forms:
                pokemon_rows = full_df[full_df["base_name"] == selected_base]
            else:
                pokemon_rows = base_df[base_df["base_name"] == selected_base]

            chart_type = st.selectbox(
                "Stat Visualization Type",
                ["Radar Chart", "Bar Chart"]
            )

            cols = st.columns(len(pokemon_rows))

            for col, (_, row) in zip(cols, pokemon_rows.iterrows()):
                with col:
                    img = get_pokemon_image(row["#"], row["form"])
                    st.image(img, width=140)

                    st.markdown(f"**{row['Name']}**")

                    st.dataframe(
                        row[STATS + ["total_stats", "power_score"]]
                        .to_frame(name="Value"),
                        use_container_width=True
                    )

                    with st.expander("📊 Stat Visualization"):
                        if chart_type == "Radar Chart":
                            fig = radar_chart(
                                STATS,
                                [row[STATS].values],
                                [row["Name"]]
                            )
                        else:
                            fig = bar_chart(
                                STATS,
                                row[STATS].values,
                                row["Name"]
                            )

                        # center the figure
                        c1, c2, c3 = st.columns([1, 2, 1])
                        with c2:
                            st.pyplot(fig, use_container_width=False)
# ==================================================
# RANKINGS PAGE
# ==================================================
elif page == "Rankings":
    st.title("Pokémon Rankings")

    metric = st.selectbox(
        "Rank by",
        ["total_stats", "Attack", "Defense", "Speed", "power_score"]
    )

    ascending = st.radio(
        "Order",
        ["Highest → Lowest", "Lowest → Highest"],
        horizontal=True
    ) == "Lowest → Highest"

    top_n = st.slider("Top N Pokémon", 5, 50, 10)

    ranked = base_df.sort_values(metric, ascending=ascending)

    st.dataframe(
        ranked[["#", "Name", "Type 1", metric]].head(top_n),
        use_container_width=True
    )

    st.subheader("Top Pokémon Cards")

    cols = st.columns(5)
    for i, (_, row) in enumerate(ranked.head(top_n).iterrows()):
        with cols[i % 5]:
            img = get_pokemon_image(row["#"], "base")
            st.image(img, width=120)
            st.markdown(f"**{row['Name']}**")
            st.caption(row["Type 1"])

# ==================================================
# POKÉMON COMPARISON PAGE
# ==================================================
elif page == "Pokémon Comparison":
    st.title("Pokémon Comparison")

    count = st.slider("Number of Pokémon", 2, 5, 2)

    selected = []
    for i in range(count):
        name = st.selectbox(
            f"Pokémon {i+1}",
            sorted(base_df["base_name"].unique()),
            key=f"cmp_{i}"
        )
        selected.append(name)

    compare_df = base_df[base_df["base_name"].isin(selected)]

    st.subheader("Stat Table")
    st.dataframe(
        compare_df.set_index("Name")[STATS],
        use_container_width=True
    )

    if st.checkbox("Show Visual Comparison"):
        col1, col2 = st.columns([1, 1])

        with col1:
            fig_radar = radar_chart(
                STATS,
                [row[STATS].values for _, row in compare_df.iterrows()],
                compare_df["Name"].tolist()
            )
            st.pyplot(fig_radar, use_container_width=False)

        with col2:
            fig_bar = comparison_bar_chart(STATS, compare_df)
            st.pyplot(fig_bar, use_container_width=False)
