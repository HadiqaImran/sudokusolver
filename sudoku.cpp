#include <iostream>
#include <vector>
#include <fstream>
#include "json.hpp"
using namespace std;
using json = nlohmann::json;
class SudokuSolver {
private:
    vector<vector<int>> board;

    // Check if placing num at board[row][col] is safe
    bool isSafe(int row, int col, int num) {
        // Check row
        for (int x = 0; x < 9; x++) {
            if (board[row][x] == num) return false;
        }

        // Check column
        for (int x = 0; x < 9; x++) {
            if (board[x][col] == num) return false;
        }

        // Check 3x3 box
        int startRow = row - row % 3;
        int startCol = col - col % 3;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (board[i + startRow][j + startCol] == num) return false;
            }
        }

        return true;
    }

    // Technique 1: Naked Singles - Fill cells with only one possibility
    bool fillNakedSingles() {
        bool progress = false;

        for (int row = 0; row < 9; row++) {
            for (int col = 0; col < 9; col++) {
                if (board[row][col] == 0) {
                    int possibleNum = 0;
                    int count = 0;

                    // Count how many numbers can go here
                    for (int num = 1; num <= 9; num++) {
                        if (isSafe(row, col, num)) {
                            possibleNum = num;
                            count++;
                        }
                    }

                    // If only one possibility, fill it
                    if (count == 1) {
                        board[row][col] = possibleNum;
                        progress = true;
                    }
                }
            }
        }

        return progress;
    }

    // Technique 2: Hidden Singles - Find numbers that can only go in one place
    bool fillHiddenSingles() {
        bool progress = false;

        // Check each row
        for (int row = 0; row < 9; row++) {
            for (int num = 1; num <= 9; num++) {
                int possibleCol = -1;
                int count = 0;

                for (int col = 0; col < 9; col++) {
                    if (board[row][col] == 0 && isSafe(row, col, num)) {
                        possibleCol = col;
                        count++;
                    }
                }

                if (count == 1) {
                    board[row][possibleCol] = num;
                    progress = true;
                }
            }
        }

        // Check each column
        for (int col = 0; col < 9; col++) {
            for (int num = 1; num <= 9; num++) {
                int possibleRow = -1;
                int count = 0;

                for (int row = 0; row < 9; row++) {
                    if (board[row][col] == 0 && isSafe(row, col, num)) {
                        possibleRow = row;
                        count++;
                    }
                }

                if (count == 1) {
                    board[possibleRow][col] = num;
                    progress = true;
                }
            }
        }

        return progress;
    }

    // Apply techniques before backtracking
    void applyTechniques() {
        bool progress = true;

        while (progress) {
            progress = false;
            progress |= fillNakedSingles();
            progress |= fillHiddenSingles();
        }
    }

    // Find empty cell
    bool findEmpty(int& row, int& col) {
        for (row = 0; row < 9; row++) {
            for (col = 0; col < 9; col++) {
                if (board[row][col] == 0) return true;
            }
        }
        return false;
    }

    // Backtracking recursion
    bool solveBacktrack() {
        int row, col;

        // If no empty cell, puzzle is solved
        if (!findEmpty(row, col)) return true;

        // Try numbers 1-9
        for (int num = 1; num <= 9; num++) {
            if (isSafe(row, col, num)) {
                board[row][col] = num;

                // Recursively solve
                if (solveBacktrack()) return true;

                // Backtrack
                board[row][col] = 0;
            }
        }

        return false;
    }

public:
    SudokuSolver(vector<vector<int>> puzzle) {
        board = puzzle;
    }

    bool solve() {
        // Step 1: Apply logical techniques first
        applyTechniques();

        // Step 2: Use backtracking for remaining cells
        return solveBacktrack();
    }

    void printBoard() {
        for (int i = 0; i < 9; i++) {
            if (i % 3 == 0 && i != 0) {
                cout << "------+-------+------" << endl;
            }
            for (int j = 0; j < 9; j++) {
                if (j % 3 == 0 && j != 0) {
                    cout << "| ";
                }
                cout << board[i][j] << " ";
            }
            cout << endl;
        }
    }
vector<vector<int>> getBoard() {
    return board;
}

};

int main() {
    // Read puzzle from JSON
    ifstream fin("input_board.json");
    if (!fin.is_open()) {
        cerr << "Error: Could not open input_board.json" << endl;
        return 1;
    }

    json j;
    fin >> j;
    vector<vector<int>> puzzle = j.get<vector<vector<int>>>();
    fin.close();

    SudokuSolver solver(puzzle);

    if (!solver.solve()) {
        cerr << "No solution exists!" << endl;
        return 1;
    }

    // Output solved board as JSON
    json out = solver.getBoard();
    cout << out.dump() << endl;

    return 0;
}