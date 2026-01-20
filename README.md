🧩 Pokédex Web App
A fully interactive Pokédex web application built using Python, Pandas, NumPy, Matplotlib, and Streamlit.
This app allows users to explore Pokémon data, visualize stats, compare Pokémon, and handle complex alternate forms accurately.
----------------------------------------------------------------
🚀 Live Features
🔍 Pokémon Search
Search Pokémon by name with instant filtering
Toggle Mega / Alternate Forms on or off
----------------------------------------------------------------
Displays:
Pokémon image
Full stat table
Total stats
Custom power score
Stat visualization options:
Radar chart
Bar chart
Each form (Mega, Primal, Therian, etc.) is displayed independently
----------------------------------------------------------------
🏆 Pokémon Rankings
Rank Pokémon based on:
Total Stats
Attack
Defense
Speed
Power Score
Supports ascending and descending order
Rankings are calculated using base Pokémon only
Displays ranked Pokémon cards with images
----------------------------------------------------------------
⚔️ Pokémon Comparison
Compare 2–5 Pokémon simultaneously
Includes:
Side-by-side stat table
Radar chart comparison
Bar chart comparison (rendered next to radar chart)
Designed for quick visual comparison of strengths and weaknesses
----------------------------------------------------------------
📊 Visualizations
Radar Charts for relative stat distribution
Bar Charts for absolute stat values
Charts are compact, responsive, and optimized for Streamlit layouts
----------------------------------------------------------------
🖼️ Image Handling System
Pokémon images are loaded locally from the images/ directory
----------------------------------------------------------------
Supports:
Base Pokémon images ({id}.jpg)
Mega forms ({id}-mega-x.jpg, {id}-mega-y.jpg)
Alternate forms (Deoxys, Shaymin, Kyurem Black/White, etc.)
----------------------------------------------------------------
Includes:
Automatic form name normalization
Special-case handling for edge Pokémon (e.g. Kyurem)
Graceful fallback to a placeholder image
----------------------------------------------------------------
🧠 Data Handling
Uses a cleaned dataset (pokemon_cleaned.csv)
----------------------------------------------------------------
Important columns:
# – Pokédex ID
Name
base_name – canonical Pokémon name
form – base, Mega, alternate form
Stat columns (HP, Attack, Defense, Sp. Atk, Sp. Def, Speed)
Strict separation between:
Base Pokémon
Mega / alternate forms
Prevents incorrect form leakage when toggles are disabled
----------------------------------------------------------------
🗂 Project Structure
Pokedex/
│
├── app.py
├── pokemon_cleaned.csv
├── images/
│   ├── 1.jpg
│   ├── 6-mega-x.jpg
│   ├── 646-black.jpg
│   ├── 646-white.jpg
│   ├── placeholder.jpg
│   └── ...
----------------------------------------------------------------
⚙️ Installation & Usage
1️⃣ Install dependencies
pip install streamlit pandas numpy matplotlib

2️⃣ Run the application
streamlit run app.py
The app will open automatically in your browser.
----------------------------------------------------------------
🎯 Project Goals
This project was built to:
Practice data cleaning and normalization
Handle real-world dataset inconsistencies
Implement data-driven UI logic
Build a complete interactive analytics app using Streamlit
Solve edge cases involving Pokémon alternate forms
----------------------------------------------------------------
🛠 Tech Stack
Python
Pandas
NumPy
Matplotlib
Streamlit
----------------------------------------------------------------
📌 Notes
Runs entirely locally
No external APIs requires
Easily extendable with new Pokémon generations or forms
----------------------------------------------------------------
📄 License:
This project is for educational and portfolio use.
