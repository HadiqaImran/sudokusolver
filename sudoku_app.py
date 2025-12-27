import streamlit as st
import numpy as np

def is_safe(board, row, col, num):
    """Check if placing num at board[row][col] is safe"""
    # Check row
    for x in range(9):
        if board[row][x] == num:
            return False
    
    # Check column
    for x in range(9):
        if board[x][col] == num:
            return False
    
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    
    return True

def fill_naked_singles(board):
    """Fill cells with only one possibility"""
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
    """Find numbers that can only go in one place"""
    progress = False
    
    # Check each row
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
    
    # Check each column
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
    """Apply logical techniques before backtracking"""
    progress = True
    
    while progress:
        progress = False
        progress |= fill_naked_singles(board)
        progress |= fill_hidden_singles(board)

def find_empty(board):
    """Find empty cell"""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def solve_backtrack(board):
    """Backtracking recursion"""
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
    """Main solve function"""
    # Step 1: Apply logical techniques
    apply_techniques(board)
    
    # Step 2: Use backtracking
    return solve_backtrack(board)

# Streamlit UI
st.set_page_config(page_title="Sudoku Solver", page_icon="🧩", layout="wide")

st.title("🧩 Sudoku Solver")
st.markdown("Enter your Sudoku puzzle below (use 0 for empty cells)")

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = np.zeros((9, 9), dtype=int)
    st.session_state.solved_board = None

# Example puzzles
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Load Easy Puzzle"):
        st.session_state.board = np.array([
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ])
        st.session_state.solved_board = None

with col2:
    if st.button("Load Hard Puzzle"):
        st.session_state.board = np.array([
            [8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 6, 0, 0, 0, 0, 0],
            [0, 7, 0, 0, 9, 0, 2, 0, 0],
            [0, 5, 0, 0, 0, 7, 0, 0, 0],
            [0, 0, 0, 0, 4, 5, 7, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 3, 0],
            [0, 0, 1, 0, 0, 0, 0, 6, 8],
            [0, 0, 8, 5, 0, 0, 0, 1, 0],
            [0, 9, 0, 0, 0, 0, 4, 0, 0]
        ])
        st.session_state.solved_board = None

with col3:
    if st.button("Clear Board"):
        st.session_state.board = np.zeros((9, 9), dtype=int)
        st.session_state.solved_board = None

with col4:
    if st.button("Solve Puzzle"):
        board_copy = st.session_state.board.copy()
        if solve_sudoku(board_copy):
            st.session_state.solved_board = board_copy
            st.success("✅ Puzzle solved!")
        else:
            st.error("❌ No solution exists!")

st.markdown("---")

# Display boards side by side
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Input Puzzle")
    
    # Create input grid
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

with col_right:
    st.subheader("Solution")
    
    if st.session_state.solved_board is not None:
        # Display solved board
        for i in range(9):
            cols = st.columns(9)
            for j in range(9):
                with cols[j]:
                    # Highlight newly filled cells
                    if st.session_state.board[i][j] == 0:
                        st.markdown(f"<div style='background-color: #90EE90; padding: 10px; text-align: center; border: 1px solid #ccc; font-weight: bold;'>{st.session_state.solved_board[i][j]}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div style='padding: 10px; text-align: center; border: 1px solid #ccc;'>{st.session_state.solved_board[i][j]}</div>", unsafe_allow_html=True)
    else:
        st.info("Click 'Solve Puzzle' to see the solution here")

st.markdown("---")
st.markdown("""
### How it works:
1. **Constraint Propagation**: First applies logical techniques (Naked Singles & Hidden Singles)
2. **Backtracking**: Uses recursive backtracking for remaining cells
3. Enter your puzzle or load an example, then click 'Solve Puzzle'!
""")