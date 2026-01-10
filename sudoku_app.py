import streamlit as st
import numpy as np

def is_safe(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    for x in range(9):
        if board[x][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True


def fill_naked_singles(board):
    progress = False
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                possible_num = 0
                count = 0
                for num in range(1, 10):
                    if is_safe(board, row, col, num):
                        possible_num = num
                        count += 1
                if count == 1:
                    board[row][col] = possible_num
                    progress = True
    return progress


def fill_hidden_singles(board):
    progress = False

    for row in range(9):
        for num in range(1, 10):
            possible_col = -1
            count = 0
            for col in range(9):
                if board[row][col] == 0 and is_safe(board, row, col, num):
                    possible_col = col
                    count += 1
            if count == 1:
                board[row][possible_col] = num
                progress = True

    for col in range(9):
        for num in range(1, 10):
            possible_row = -1
            count = 0
            for row in range(9):
                if board[row][col] == 0 and is_safe(board, row, col, num):
                    possible_row = row
                    count += 1
            if count == 1:
                board[possible_row][col] = num
                progress = True

    return progress


def apply_techniques(board):
    progress = True
    while progress:
        progress = False
        progress |= fill_naked_singles(board)
        progress |= fill_hidden_singles(board)


def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None


def solve_backtrack(board):
    find = find_empty(board)
    if not find:
        return True

    row, col = find
    for num in range(1, 10):
        if is_safe(board, row, col, num):
            board[row][col] = num
            if solve_backtrack(board):
                return True
            board[row][col] = 0
    return False


def solve_sudoku(board):
    apply_techniques(board)
    return solve_backtrack(board)


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


# ------------------ UI ------------------

st.set_page_config(page_title="Sudoku Solver", page_icon="🧩", layout="wide")
st.title("🧩 Sudoku Solver Pro")

if "board" not in st.session_state:
    st.session_state.board = np.zeros((9, 9), dtype=int)
    st.session_state.solved_board = None


tab1, tab2, tab3 = st.tabs(["🎮 Solve Puzzle", "📚 How It Works", "ℹ️ About"])


with tab1:
    st.markdown("<h2 style='text-align: center;'>🎯 Enter Your Puzzle</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🗑️ Clear Board"):
            # 🔑 FIX: clear widget state as well
            for i in range(9):
                for j in range(9):
                    st.session_state[f"input_{i}_{j}"] = 0
            st.session_state.board = np.zeros((9, 9), dtype=int)
            st.session_state.solved_board = None

    with col2:
        if st.button("✨ Solve Puzzle"):
            board_copy = st.session_state.board.copy()
            if solve_sudoku(board_copy):
                st.session_state.solved_board = board_copy
                st.success("✅ Puzzle solved successfully!")
            else:
                st.error("❌ No solution exists!")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

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
                        st.markdown(
                            f"<div style='{get_cell_style(i, j, is_input)}'>{val}</div>",
                            unsafe_allow_html=True
                        )
        else:
            st.info("👆 Click **Solve Puzzle** to see the solution.")

        st.markdown("</div>", unsafe_allow_html=True)


with tab2:
    st.markdown("""
    <div style='background-color: white; padding: 20px; border-radius: 15px;'>
    <h3>📚 How the Algorithm Works</h3>
    <ul>
        <li><b>Naked Singles:</b> Cells with only one valid number</li>
        <li><b>Hidden Singles:</b> Numbers that fit in only one position</li>
        <li><b>Backtracking:</b> Recursive search for remaining cells</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)


with tab3:
    st.markdown("""
    <div style='background-color: white; padding: 30px; border-radius: 15px;'>
    <p>
    This Sudoku solver allows users to manually input any valid Sudoku puzzle
    and solves it using logical techniques followed by backtracking.
    </p>

    <h4>✨ Features</h4>
    <ul>
        <li>Manual puzzle input</li>
        <li>Automatic Sudoku solving</li>
        <li>Visual distinction between input and solved cells</li>
        <li>Efficient algorithm</li>
    </ul>

    <h4>🎮 How to Use</h4>
    <ol>
        <li>Enter numbers (0 for empty cells)</li>
        <li>Click <b>Solve Puzzle</b></li>
        <li>View the solution on the right</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
