import pytest
import tkinter as tk
from unittest.mock import patch, MagicMock
import sliding_puzzle_project


# -------------------- Fixture --------------------
@pytest.fixture
def app():
    root = tk.Tk()
    root.withdraw()  # hide the main window

    # Patch image loading and Tkinter PhotoImage to avoid GUI errors
    with patch("sliding_puzzle_project.Image.open") as mock_open, \
         patch("sliding_puzzle_project.ImageTk.PhotoImage") as mock_photo, \
         patch.object(sliding_puzzle_project.SlidingPuzzleApp, "render"):

        # Mock PIL image
        mock_img = MagicMock()
        mock_img.size = (500, 500)
        mock_img.convert.return_value = mock_img
        mock_img.crop.return_value = mock_img
        mock_img.resize.return_value = mock_img
        mock_open.return_value = mock_img

        # Mock Tkinter PhotoImage
        mock_photo.return_value = MagicMock()

        # Create the app (render is mocked, so no GUI operations happen)
        puzzle = sliding_puzzle_project.SlidingPuzzleApp(root, size=3)

    yield puzzle
    root.destroy()


# -------------------- Tests --------------------
def test_reset_creates_solved_board(app):
    app.reset()
    expected = [[1,2,3],[4,5,6],[7,8,0]]
    assert app.board == expected


def test_is_adjacent_true(app):
    assert app.is_adjacent((2,2), (2,1)) is True
    assert app.is_adjacent((1,1), (0,1)) is True


def test_is_adjacent_false(app):
    assert app.is_adjacent((0,0), (2,2)) is False
    assert app.is_adjacent((1,0), (0,2)) is False


def test_swap_changes_positions(app):
    app.board = [[1,2,3],[4,5,6],[7,8,0]]
    app.swap((2,2), (2,1))
    assert app.board[2][2] == 8
    assert app.board[2][1] == 0


def test_is_solved_false_when_moved(app):
    app.board = [[1,2,3],[4,5,6],[7,0,8]]
    assert app.is_solved() is False


def test_on_click_valid_move(app):
    app.board = [[1,2,3],[4,5,6],[7,0,8]]
    app.on_click((2,2))  # swap with blank
    assert app.board[2][2] == 0
    assert app.board[2][1] == 8


def test_on_click_invalid_move(app):
    app.board = [[1,2,3],[4,5,6],[7,0,8]]
    old_board = [row[:] for row in app.board]
    app.on_click((0,0))  # invalid move
    assert app.board == old_board  # board unchanged


def test_shuffle_changes_board(app):
    original = [row[:] for row in app.board]
    app.shuffle()
    assert app.board != original  # after shuffle, board should change


def test_set_size_changes_board_dimensions(app):
    app.set_size(4)
    assert len(app.board) == 4
    assert len(app.board[0]) == 4