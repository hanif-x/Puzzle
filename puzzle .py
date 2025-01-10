import tkinter as tk
from random import shuffle


class InfinityPuzzle:
    def __init__(self, root):
        self.root = root
        self.root.title("Infinity Puzzle")
        self.level = 1  # ডিফল্ট লেভেল ১
        self.grid_size = 3  # লেভেল অনুযায়ী গ্রিড সাইজ
        self.time_limit = 60  # লেভেল অনুযায়ী টাইমার
        self.create_menu()
        self.start_game()

    def create_menu(self):
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        game_menu = tk.Menu(menu, tearoff=0)
        game_menu.add_command(label="Restart", command=self.start_game)
        game_menu.add_command(label="Exit", command=self.root.quit)
        menu.add_cascade(label="Game", menu=game_menu)

        level_menu = tk.Menu(menu, tearoff=0)
        for i in range(1, 101):  # ১ থেকে ১০০ পর্যন্ত লেভেল
            level_menu.add_command(label=f"Level {i}", command=lambda l=i: self.set_level(l))
        menu.add_cascade(label="Levels", menu=level_menu)

    def set_level(self, level):
        self.level = level
        self.grid_size = min(3 + (level - 1) // 10, 10)  # গ্রিড সাইজ ধীরে ধীরে বড় হবে
        self.time_limit = max(60 - (level - 1) * 2, 10)  # টাইমার ধীরে ধীরে কমবে
        self.start_game()

    def start_game(self):
        self.numbers = list(range(1, self.grid_size ** 2)) + [""]
        shuffle(self.numbers)
        self.grid_frame = tk.Frame(self.root)
        self.grid_frame.pack(pady=20)
        self.create_grid()
        self.start_timer()

    def create_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        for i, num in enumerate(self.numbers):
            row, col = divmod(i, self.grid_size)
            button = tk.Button(
                self.grid_frame,
                text=num,
                font=("Arial", 18),
                width=4,
                height=2,
                command=lambda n=num: self.move_tile(n),
            )
            button.grid(row=row, column=col, padx=5, pady=5)
            if num == "":
                button.config(state="disabled")

    def move_tile(self, num):
        idx = self.numbers.index(num)
        empty_idx = self.numbers.index("")
        row, col = divmod(idx, self.grid_size)
        empty_row, empty_col = divmod(empty_idx, self.grid_size)

        if abs(row - empty_row) + abs(col - empty_col) == 1:
            self.numbers[idx], self.numbers[empty_idx] = self.numbers[empty_idx], self.numbers[idx]
            self.create_grid()
            if self.check_win():
                self.show_message("Congratulations! You solved it!")

    def check_win(self):
        return self.numbers == list(range(1, self.grid_size ** 2)) + [""]

    def start_timer(self):
        self.time_label = tk.Label(self.root, text=f"Time: {self.time_limit} seconds", font=("Arial", 16))
        self.time_label.pack()
        self.update_timer()

    def update_timer(self):
        if self.time_limit > 0:
            self.time_limit -= 1
            self.time_label.config(text=f"Time: {self.time_limit} seconds")
            self.root.after(1000, self.update_timer)
        else:
            self.show_message("Time's up! Try again!")

    def show_message(self, message):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        msg_label = tk.Label(self.grid_frame, text=message, font=("Arial", 24), fg="red")
        msg_label.pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = InfinityPuzzle(root)
    root.mainloop()