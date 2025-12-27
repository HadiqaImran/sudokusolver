import streamlit as st
import numpy as np

def is_safe(board, row, col, num):
    """Check if placing num at board[row][col] is safe"""
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
    apply_techniques(board)
    return solve_backtrack(board)

def get_cell_style(i, j, is_input=True):
    """Get CSS style for a cell"""
    # Thicker borders for 3x3 boxes
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

# Page config
st.set_page_config(page_title="Sudoku Solver", page_icon="🧩", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 50px;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        background-color: #ffffff;
        font-weight: bold;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    h1 {
        color: white;
        text-align: center;
        font-size: 3em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    h2, h3 {
        color: white;
    }
    .stNumberInput>div>div>input {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        border: 2px solid #667eea;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🧩 Sudoku Solver Pro")

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = np.zeros((9, 9), dtype=int)
    st.session_state.solved_board = None

# Tabs
tab1, tab2, tab3 = st.tabs(["🎮 Solve Puzzle", "📚 How It Works", "ℹ️ About"])

with tab1:
    st.markdown("<h2 style='text-align: center;'>🎯 Enter Your Puzzle</h2>", unsafe_allow_html=True)
    
    # Control buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🌟 Easy Puzzle"):
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
        if st.button("🔥 Hard Puzzle"):
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
        if st.button("🗑️ Clear Board"):
            st.session_state.board = np.zeros((9, 9), dtype=int)
            st.session_state.solved_board = None
    
    with col4:
        if st.button("🎲 Random Empty"):
            board = st.session_state.board.copy()
            if np.any(board != 0):
                non_zero = np.argwhere(board != 0)
                idx = non_zero[np.random.randint(len(non_zero))]
                board[idx[0], idx[1]] = 0
                st.session_state.board = board
                st.session_state.solved_board = None
    
    with col5:
        if st.button("✨ Solve Puzzle"):
            board_copy = st.session_state.board.copy()
            if solve_sudoku(board_copy):
                st.session_state.solved_board = board_copy
                st.success("✅ Puzzle solved successfully!")
                st.balloons()
            else:
                st.error("❌ No solution exists for this puzzle!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display boards
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("<h3 style='text-align: center;'>📝 Input Puzzle</h3>", unsafe_allow_html=True)
        
        # White container for input grid
        st.markdown("<div style='background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>", unsafe_allow_html=True)
        
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
        
        # White container for solution grid
        st.markdown("<div style='background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);'>", unsafe_allow_html=True)
        
        if st.session_state.solved_board is not None:
            for i in range(9):
                cols = st.columns(9)
                for j in range(9):
                    with cols[j]:
                        val = st.session_state.solved_board[i][j]
                        is_input = st.session_state.board[i][j] != 0
                        
                        if is_input:
                            # Original number - gray background
                            st.markdown(f"<div style='{get_cell_style(i, j, True)}'>{val}</div>", unsafe_allow_html=True)
                        else:
                            # Solved number - green background
                            st.markdown(f"<div style='{get_cell_style(i, j, False)}'>{val}</div>", unsafe_allow_html=True)
        else:
            st.info("👆 Click 'Solve Puzzle' to see the solution!")
        
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<h2>📚 How the Algorithm Works</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background-color: white; padding: 20px; border-radius: 15px; margin: 10px 0;'>
        <h3 style='color: #667eea;'>🎯 Step 1: Constraint Propagation</h3>
        <p style='color: #2c3e50;'><strong>Naked Singles:</strong> Finds cells with only one possible number</p>
        <p style='color: #2c3e50;'><strong>Hidden Singles:</strong> Finds numbers that can only go in one place in a row, column, or box</p>
        <p style='color: #2c3e50;'>These techniques loop until no more progress can be made.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: white; padding: 20px; border-radius: 15px; margin: 10px 0;'>
        <h3 style='color: #764ba2;'>🔄 Step 2: Backtracking Recursion</h3>
        <p style='color: #2c3e50;'><strong>Recursive Search:</strong> Tries numbers 1-9 in empty cells</p>
        <p style='color: #2c3e50;'><strong>Validation:</strong> Checks if placement is valid</p>
        <p style='color: #2c3e50;'><strong>Backtrack:</strong> If stuck, goes back and tries a different number</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: white; padding: 20px; border-radius: 15px; margin: 20px 0;'>
    <h3 style='color: #667eea;'>⚡ Why This Approach is Efficient</h3>
    <ul style='color: #2c3e50; font-size: 16px;'>
        <li>Constraint propagation solves easy cells immediately</li>
        <li>Reduces the search space for backtracking</li>
        <li>Backtracking only used when logical techniques aren't enough</li>
        <li>Validates constraints at each step to fail fast</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("<h2>ℹ️ About This Solver</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: white; padding: 30px; border-radius: 15px;'>
    <p style='color: #2c3e50; font-size: 18px;'>
    This Sudoku solver combines logical reasoning with computational power to solve any valid Sudoku puzzle.
    </p>
    
    <h3 style='color: #667eea;'>✨ Features:</h3>
    <ul style='color: #2c3e50; font-size: 16px;'>
        <li>Interactive grid input</li>
        <li>Pre-loaded example puzzles (easy and hard)</li>
        <li>Visual highlighting of solved cells</li>
        <li>Two-step algorithm: constraint propagation + backtracking</li>
        <li>Fast and efficient solving</li>
    </ul>
    
    <h3 style='color: #667eea;'>🎮 How to Use:</h3>
    <ol style='color: #2c3e50; font-size: 16px;'>
        <li>Enter numbers in the input grid (0 for empty cells)</li>
        <li>Or click "Easy Puzzle" or "Hard Puzzle" to load examples</li>
        <li>Click "Solve Puzzle" to see the solution</li>
        <li>Green cells show the numbers that were filled in by the solver</li>
    </ol>
    
    <p style='color: #2c3e50; font-size: 16px; margin-top: 20px;'>
    <strong>💡 Tip:</strong> Use the "Random Empty" button to make puzzles easier by removing cells!
    </p>
    </div>
    """, unsafe_allow_html=True)