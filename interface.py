import streamlit as st
import subprocess

# Define function to run Game 1
def run_game_1():
    subprocess.Popen(["python", "launcher_game1.py"])

# Define function to run Game 2
def run_game_2():
    subprocess.Popen(["python", "launcher_game2.py"])

# Define function to run Game 3
def run_game_3():
    subprocess.Popen(["python", "game3.py"])

# Streamlit app
def main():
    # Set page config for dark theme
    st.set_page_config(
        page_title="Game Launcher",
        page_icon="🎮",
        layout="centered",
        initial_sidebar_state="auto"    )

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        body {
            color: #FFFFFF;
            background-color: #121212;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            color: #FFFFFF;
            background-color: #1976D2;
            border-color: #1976D2;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #2196F3;
            border-color: #2196F3;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Game Launcher")

    st.write("Welcome to the Game Launcher! Choose a game to play.")

    # Button to run Game 1
    if st.button("Run Game 1"):
        run_game_1()
    
    # Button to run Game 2
    if st.button("Run Game 2"):
        run_game_2()

    # Button to run Game 3
    if st.button("Run Game 3"):
        run_game_3()

if __name__ == "__main__":
    main()
