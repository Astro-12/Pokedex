import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pokedex = pd.read_csv("pokemon.csv")

pokedex["Type 2"] = pokedex["Type 2"].fillna("None")
pokedex = pokedex.drop(columns=["Total"])

stats = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
pokedex[stats] = pokedex[stats].apply(pd.to_numeric)

stat_array = pokedex[stats].to_numpy()
pokedex["total_stats"] = np.sum(stat_array, axis=1)

weights = np.array([1.0, 1.3, 1.2, 1.4, 1.3, 1.1])
pokedex["power_score"] = stat_array @ weights


def show_top_10():
    top_10 = pokedex.sort_values("total_stats", ascending=False).head(10)
    print(top_10[["Name", "Type 1", "total_stats"]])


def show_type_means():
    type_stats = pokedex.groupby("Type 1")[stats].mean().round(1)
    print(type_stats)


def show_power_scores():
    top_power = pokedex.sort_values("power_score", ascending=False).head(10)
    print(top_power[["Name", "Type 1", "power_score"]])


def search_pokemon():
    query = input("Enter pokemon name: ").strip().lower()

    if not query:
        print("Please enter a name.")
        return
    matches = pokedex[pokedex["Name"].str.lower().str.contains(query)]
    if matches.empty:
        print("❌ Pokemon not found")
    else:
        print(matches[
            ["Name", "Type 1", "Type 2",
             "HP", "Attack", "Defense",
             "Sp. Atk", "Sp. Def", "Speed",
             "total_stats", "power_score"]
        ])
        return
    
    
    print("\n Multiple pokemon found: ")
    for i in enumerate(matches["Name"].values, start = 1):
        print(f"{i}. {__name__}")

    choice = input("\nEnter the number to view details (or press Enter to cancel): ").strip()

    if not choice:
        return
    
    
    choice = int(choice)

    if choice < 1 or choice > len(matches):
        print("⚠️ Number out of range.")
        return

    selected = matches.iloc[choice - 1]

    print("\n📊 Pokémon Details:\n")
    print(selected[
        ["Name", "Type 1", "Type 2",
         "HP", "Attack", "Defense",
         "Sp. Atk", "Sp. Def", "Speed",
         "total_stats", "power_score"]
    ])

def plot_avg_stats_by_type():
    print("\nAvailable Types:['Grass' 'Fire' 'Water' 'Bug' 'Normal' 'Poison' 'Electric' " \
    "'Ground' 'Fairy' 'Fighting' 'Psychic' 'Rock' 'Ghost' 'Ice' 'Dragon' 'Dark' 'Steel''Flying']")
    print(sorted(pokedex["Type 1"].unique()))

    types_input = input(
        "\nEnter types to compare (comma separated, e.g. Fire,Water): "
    ).strip()

    selected_types = [t.strip() for t in types_input.split(",")]

    valid_types = pokedex["Type 1"].unique()
    selected_types = [t for t in selected_types if t in valid_types]

    if len(selected_types) < 2:
        print("⚠️ Please select at least 2 valid types.")
        return

    print("\nAvailable Stats:", stats)
    stats_input = input(
        "Enter stats to compare (comma separated, e.g. Attack,Speed): "
    ).strip()

    selected_stats = [s.strip() for s in stats_input.split(",")]

    selected_stats = [s for s in selected_stats if s in stats]

    if not selected_stats:
        print("⚠️ No valid stats selected.")
        return

    type_stats = (
        pokedex[pokedex["Type 1"].isin(selected_types)]
        .groupby("Type 1")[selected_stats]
        .mean()
    )

    type_stats.plot(kind="bar", figsize=(10, 6))
    plt.title("Average Stats Comparison by Type")
    plt.ylabel("Average Value")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()


def plot_stat_distribution():
    print("\nAvailable Stats:", stats)
    stat = input("Enter stat to analyze: ").strip()

    if stat not in stats:
        print("⚠️ Invalid stat.")
        return

    names_input = input(
        "Enter Pokémon names to compare (comma separated, e.g. Pikachu,Charizard): "
    ).strip()

    names = [n.strip() for n in names_input.split(",")]

    selected = pokedex[pokedex["Name"].isin(names)]

    if selected.empty:
        print("⚠️ No valid Pokémon found.")
        return

    plt.figure(figsize=(8, 5))

    for name in selected["Name"]:
        values = pokedex[pokedex["Name"] == name][stat]
        plt.hist(
            values,
            bins=10,
            alpha=0.6,
            edgecolor="black",
            label=name
        )

    plt.title(f"{stat} Distribution Comparison")
    plt.xlabel(stat)
    plt.ylabel("Frequency")
    plt.legend()
    plt.tight_layout()
    plt.show()
#The graphs can be modified(outline,different colors)basically make the graph more user friendly to understand and again more in-depht selection of what pokemons you wanna compare the stats for

def plot_attack_vs_speed():
    plt.figure(figsize=(8, 6))

    plt.scatter(
        pokedex["Attack"],
        pokedex["Speed"],
        alpha=0.7,
        edgecolors="black"
    )

    plt.title("Attack vs Speed of Pokémon")
    plt.xlabel("Attack")
    plt.ylabel("Speed")

    # Highlight fast Pokémon
    fast = pokedex["Speed"] > 100
    plt.scatter(
        pokedex.loc[fast, "Attack"],
        pokedex.loc[fast, "Speed"],
        label="Fast Pokémon (Speed > 100)"
    )

    plt.legend()
    plt.tight_layout()
    plt.show()

#The dot color of speed and attack has to be changed.

def menu():
    while True:
        print("\n--- POKEDEX MENU ---")
        print("1. Show Top 10 Pokémon (by Total Stats)")
        print("2. Show Average Stats by Type")
        print("3. Show Top 10 Pokémon (by Power Score)")
        print("4. Search Pokémon by Name")  
        print("5. Plot Attack vs Speed")
        print("6. Plot Average Stats by Type")
        print("7. Plot Stat Distribution")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if not choice.isdigit():
            print("⚠️ Enter a number.")
            continue

        choice = int(choice)

        if choice == 1:
            show_top_10()
        elif choice == 2:
            show_type_means()
        elif choice == 3:
            show_power_scores()
        elif choice == 4:
            search_pokemon()
        elif choice == 5:
            plot_attack_vs_speed()
        elif choice == 6:
            plot_avg_stats_by_type()
        elif choice == 7:
            plot_stat_distribution()
        elif choice == 8:
            print("Goodbye, Trainer! 👋")
            break
        else:
            print("⚠️ Invalid choice.")


print()

menu()
