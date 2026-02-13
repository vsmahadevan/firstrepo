import tkinter as tk
import random
from PIL import Image, ImageTk

EMPTY = 0
IMAGE_PATH = "puppy.jpg"  # <-- your image

class SlidingPuzzleApp:
    def __init__(self, root, size=4, tile_px=90):
        self.root = root
        self.size = size
        self.tile_px = tile_px
        self.root.title(f"Sliding Puzzle ({self.size}x{self.size})")

        controls = tk.Frame(root)
        controls.pack(pady=8)

        self.status = tk.Label(controls, text="Click a tile next to the empty space.")
        self.status.pack(side=tk.LEFT, padx=8)

        tk.Button(controls, text="Shuffle", command=self.shuffle).pack(side=tk.LEFT, padx=4)
        tk.Button(controls, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=4)

        tk.Button(controls, text="3x3", command=lambda: self.set_size(3)).pack(side=tk.LEFT, padx=4)
        tk.Button(controls, text="4x4", command=lambda: self.set_size(4)).pack(side=tk.LEFT, padx=4)
        tk.Button(controls, text="5x5", command=lambda: self.set_size(5)).pack(side=tk.LEFT, padx=4)

        self.board_frame = tk.Frame(root)
        self.board_frame.pack(padx=10, pady=10)

        self.board = []
        self.buttons = []
        self.empty_pos = (self.size - 1, self.size - 1)

        self.tile_photos = {}
        self.blank_photo = None

        self.build_board_ui()
        self.load_and_slice_image()
        self.reset()
        self.shuffle()

    def build_board_ui(self):
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for r in range(self.size):
            row_buttons = []
            for c in range(self.size):
                btn = tk.Button(
                    self.board_frame,
                    width=self.tile_px,
                    height=self.tile_px,
                    command=lambda rr=r, cc=c: self.on_click(rr, cc)
                )
                btn.grid(row=r, column=c, padx=3, pady=3)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

    def load_and_slice_image(self):
        img = Image.open(IMAGE_PATH).convert("RGB")

        w, h = img.size
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        img = img.crop((left, top, left + side, top + side))

        grid_px = self.size * self.tile_px
        img = img.resize((grid_px, grid_px), Image.Resampling.LANCZOS)

        self.tile_photos = {}
        tile_num = 1
        for r in range(self.size):
            for c in range(self.size):
                if r == self.size - 1 and c == self.size - 1:
                    break

                x0 = c * self.tile_px
                y0 = r * self.tile_px
                tile_img = img.crop((x0, y0, x0 + self.tile_px, y0 + self.tile_px))
                self.tile_photos[tile_num] = ImageTk.PhotoImage(tile_img)
                tile_num += 1

        blank = Image.new("RGB", (self.tile_px, self.tile_px), color=(230, 230, 230))
        self.blank_photo = ImageTk.PhotoImage(blank)

    def reset(self):
        n = self.size * self.size
        values = list(range(1, n)) + [EMPTY]
        self.board = [values[i*self.size:(i+1)*self.size] for i in range(self.size)]
        self.empty_pos = (self.size - 1, self.size - 1)
        self.status.config(text="Reset to solved. Press Shuffle to play.")
        self.render()

    def render(self):
        for r in range(self.size):
            for c in range(self.size):
                val = self.board[r][c]
                btn = self.buttons[r][c]

                if val == EMPTY:
                    btn.config(image=self.blank_photo, state=tk.DISABLED)
                else:
                    btn.config(image=self.tile_photos[val], state=tk.NORMAL)

    def on_click(self, r, c):
        if self.is_adjacent((r, c), self.empty_pos):
            self.swap((r, c), self.empty_pos)
            self.empty_pos = (r, c)
            self.render()

            if self.is_solved():
                self.status.config(text="🎉 You win! Press Shuffle to play again.")
            else:
                self.status.config(text="Good move!")
        else:
            self.status.config(text="That tile can't move.")

    def is_adjacent(self, pos1, pos2):
        (r1, c1), (r2, c2) = pos1, pos2
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def swap(self, pos1, pos2):
        r1, c1 = pos1
        r2, c2 = pos2
        self.board[r1][c1], self.board[r2][c2] = self.board[r2][c2], self.board[r1][c1]

    def is_solved(self):
        n = self.size * self.size
        expected = list(range(1, n)) + [EMPTY]
        flat = [self.board[r][c] for r in range(self.size) for c in range(self.size)]
        return flat == expected

    def shuffle(self):
        moves = self.size * self.size * 50
        for _ in range(moves):
            r, c = self.empty_pos
            neighbors = []
            if r > 0: neighbors.append((r - 1, c))
            if r < self.size - 1: neighbors.append((r + 1, c))
            if c > 0: neighbors.append((r, c - 1))
            if c < self.size - 1: neighbors.append((r, c + 1))

            chosen = random.choice(neighbors)
            self.swap(chosen, self.empty_pos)
            self.empty_pos = chosen

        if self.is_solved():
            self.shuffle()
            return

        self.status.config(text="Shuffled! Click tiles to move.")
        self.render()

    def set_size(self, new_size):
        self.size = new_size
        self.root.title(f"Sliding Puzzle ({self.size}x{self.size})")
        self.empty_pos = (self.size - 1, self.size - 1)

        self.build_board_ui()
        self.load_and_slice_image()
        self.reset()
        self.shuffle()

if __name__ == "__main__":
    root = tk.Tk()
    app = SlidingPuzzleApp(root, size=4)
    root.mainloop()
