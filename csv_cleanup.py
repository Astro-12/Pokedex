import pandas as pd
import re

df = pd.read_csv("pokemon.csv")
import pandas as pd
import re

df = pd.read_csv("pokemon.csv")

def extract_base_and_form(name):
    name = name.strip()

    patterns = [
        ("mega-x", r"Mega .* X"),
        ("mega-y", r"Mega .* Y"),
        ("mega", r"Mega "),
        ("primal", r"Primal "),
        ("incarnate", r"Incarnate Forme"),
        ("therian", r"Therian Forme"),
        ("land", r"Land Forme"),
        ("sky", r"Sky Forme"),
        ("origin", r"Origin Forme"),
        ("altered", r"Altered Forme"),
        ("attack", r"Attack Forme"),
        ("defense", r"Defense Forme"),
        ("speed", r"Speed Forme"),
        ("normal", r"Normal Forme"),
        ("blade", r"Blade Forme"),
        ("shield", r"Shield Forme"),
    ]

    for form_id, pattern in patterns:
        if re.search(pattern, name):
            base = re.sub(pattern, "", name).replace("Mega", "").strip()
            return base, form_id

    return name, "base"


df[["base_name", "form_id"]] = df["Name"].apply(
    lambda x: pd.Series(extract_base_and_form(x))
)

df["image_file"] = df.apply(
    lambda r: f"{r['#']}.jpg" if r["form_id"] == "base"
    else f"{r['#']}-{r['form_id']}.jpg",
    axis=1
)

df.to_csv("pokemon_cleaned.csv", index=False)

def extract_base_and_form(name):
    """
    Splits Name into:
    - base_name (used for display & grouping)
    - form (used for image resolution)
    """

    base = name
    form = "base"

    if "Mega" in name:
        base, rest = name.split("Mega", 1)
        form = "mega-" + rest.strip().lower().replace(" ", "-")

    elif "Forme" in name:
        parts = name.split()
        base = parts[0]
        form = parts[-2].lower()  # land, sky, therian, etc.

    elif "Mode" in name:
        parts = name.split()
        base = parts[0]
        form = parts[-2].lower()

    elif "Cloak" in name or "Size" in name:
        parts = name.split()
        base = parts[0]
        form = parts[-2].lower()

    return base.strip(), form.strip()

df[["base_name", "form"]] = df["Name"].apply(
    lambda x: pd.Series(extract_base_and_form(x))
)

df.to_csv("pokemon_cleaned.csv", index=False)

print("✅ pokemon_cleaned.csv created successfully")
