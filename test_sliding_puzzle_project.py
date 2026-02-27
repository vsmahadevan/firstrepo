import pytest
import tkinter as tk
from unittest.mock import patch, MagicMock
import sliding_puzzle_project


@pytest.fixture
def app():
    root = tk.Tk()
    root.withdraw()

    with patch.object(sliding_puzzle_project.SlidingPuzzleApp, "render"), \
         patch("sliding_puzzle_project.Image.open") as mock_open, \
         patch("sliding_puzzle_project.ImageTk.PhotoImage"):

        mock_img = MagicMock()
        mock_img.size = (500, 500)
        mock_img.convert.return_value = mock_img
        mock_img.crop.return_value = mock_img
        mock_img.resize.return_value = mock_img
        mock_open.return_value = mock_img

        puzzle = sliding_puzzle_project.SlidingPuzzleApp(root, size=3)

    yield puzzle
    root.destroy()

def test_reset_creates_solved_board(app):
    app.reset()
    n = app.size * app.size
    expected = list(range(1, n)) + [sliding_puzzle_project.EMPTY]
    flat = [app.board[r][c] for r in range(app.size) for c in range(app.size)]
    assert flat == expected
    assert app.is_solved()


def test_is_adjacent_true(app):
    assert app.is_adjacent((0, 0), (0, 1))
    assert app.is_adjacent((1, 1), (2, 1))


def test_is_adjacent_false(app):
    assert not app.is_adjacent((0, 0), (2, 2))
    assert not app.is_adjacent((0, 0), (1, 1))


def test_swap_changes_positions(app):
    app.board = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, sliding_puzzle_project.EMPTY]
    ]
    app.swap((2, 1), (2, 2))
    assert app.board[2][2] == 8
    assert app.board[2][1] == sliding_puzzle_project.EMPTY


def test_is_solved_false_when_moved(app):
    app.reset()
    app.swap((2, 1), (2, 2))
    assert not app.is_solved()


def test_shuffle_changes_board(app):
    app.reset()
    before = [row[:] for row in app.board]
    app.shuffle()
    after = app.board
    assert before != after
    assert not app.is_solved()


def test_set_size_changes_board_dimensions(app):
    app.set_size(4)
    assert app.size == 4
    assert len(app.board) == 4
    assert len(app.board[0]) == 4