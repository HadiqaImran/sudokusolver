import streamlit as st
import numpy as np
import subprocess
import json



def get_cell_style(i, j, is_input=True):
    border_right = "3px solid #2c3e50" if (j + 1) % 3 == 0 and j != 8 else "1px solid #bdc3c7"
    border_bottom = "3px solid #2c3e50" if (i + 1) % 3 == 0 and i != 8 else "1px solid #bdc3c7"
    bg_color = "#f8f9fa" if is_input else "#e8f5e9"
    return f"""
        background-color: {bg_color};
        padding: 15px;
        text-align: center;
        border: 1px solid #bdc3c7;
        border-right: {border_right};
        border-bottom: {border_bottom};
        font-size: 20px;
        font-weight: bold;
        color: #2c3e50;
        border-radius: 4px;
        min-height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    """

st.set_page_config(page_title="Sudoku Solver", page_icon="🧩", layout="wide")
st.title("🧩 Sudoku Solver Pro")

# Initialize session state
if "board" not in st.session_state:
    st.session_state.board = np.zeros((9, 9), dtype=int)
    st.session_state.solved_board = None

tab1, tab2, tab3 = st.tabs(["🎮 Solve Puzzle", "📚 How It Works", "ℹ️ About"])

with tab1:
    st.markdown("<h2 style='text-align: center;'>🎯 Enter Your Puzzle</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    # Clear board button
    with col1:
        if st.button("🗑️ Clear Board"):
            st.session_state.board = np.zeros((9, 9), dtype=int)
            st.session_state.solved_board = None

    # Solve puzzle button
    with col2:
        if st.button("✨ Solve Puzzle"):
            # Send board to C++ solver (assumes ./sudoku_solver reads JSON input/output)
            with open("input_board.json", "w") as f:
                json.dump(st.session_state.board.tolist(), f)
            try:
                result = subprocess.run(["./sudoku_solver"], capture_output=True, text=True, check=True)
                solved_board = np.array(json.loads(result.stdout))
                st.session_state.solved_board = solved_board
                st.success("✅ Puzzle solved successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Solver failed! Make sure the C++ executable exists.\n{e}")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    # Input grid
    with col_left:
        st.markdown("<h3 style='text-align: center;'>📝 Input Puzzle</h3>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: white; padding: 20px; border-radius: 15px;'>", unsafe_allow_html=True)
        for i in range(9):
            cols = st.columns(9)
            for j in range(9):
                with cols[j]:
                    val = st.number_input(
                        f"cell_{i}_{j}",
                        min_value=0,
                        max_value=9,
                        value=int(st.session_state.board[i][j]),
                        key=f"input_{i}_{j}",
                        label_visibility="collapsed"
                    )
                    st.session_state.board[i][j] = val
        st.markdown("</div>", unsafe_allow_html=True)

    # Solution grid
    with col_right:
        st.markdown("<h3 style='text-align: center;'>✅ Solution</h3>", unsafe_allow_html=True)
        st.markdown("<div style='background-color: white; padding: 20px; border-radius: 15px;'>", unsafe_allow_html=True)
        if st.session_state.solved_board is not None:
            for i in range(9):
                cols = st.columns(9)
                for j in range(9):
                    with cols[j]:
                        val = st.session_state.solved_board[i][j]
                        is_input = st.session_state.board[i][j] != 0
                        st.markdown(f"<div style='{get_cell_style(i, j, is_input)}'>{val}</div>", unsafe_allow_html=True)
        else:
            st.info("👆 Click **Solve Puzzle** to see the solution.")
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div style='background-color: white; padding: 20px; border-radius: 15px;'>
    <h3>📚 How the Algorithm Works</h3>
    <ul>
        <li><b>C++ Solver:</b> Uses naked/hidden singles + backtracking</li>
        <li>Front-end only handles input/output visualization</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
    <div style='background-color: white; padding: 30px; border-radius: 15px;'>
    <p>
    This Sudoku solver lets users manually input a puzzle and sends it to a C++ solver.
    </p>

    <h4>✨ Features</h4>
    <ul>
        <li>Manual puzzle input</li>
        <li>Automatic Sudoku solving via C++ backend</li>
        <li>Visual distinction between input and solved cells</li>
        <li>Clean front-end with Streamlit</li>
    </ul>

    <h4>🎮 How to Use</h4>
    <ol>
        <li>Enter numbers (0 for empty cells)</li>
        <li>Click <b>Solve Puzzle</b></li>
        <li>View the solution on the right</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
