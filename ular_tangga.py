import tkinter as tk
import random

class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Permainan Ular Tangga")
        self.create_widgets()
        self.reset_game()

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=500, height=500, bg='lightblue')
        self.canvas.pack()

        self.roll_button = tk.Button(self.root, text="Gulir Dadu", command=self.roll_dice, font=('Arial', 14))
        self.roll_button.pack(pady=10)

        self.position_label = tk.Label(self.root, text="Posisi Pemain: 1", font=('Arial', 14))
        self.position_label.pack(pady=10)

        self.dice_label = tk.Label(self.root, text="Hasil Dadu: 0", font=('Arial', 14))
        self.dice_label.pack(pady=10)

        self.dice_face = self.canvas.create_rectangle(400, 400, 450, 450, fill='white', outline='black')
        self.dice_dot1 = self.canvas.create_oval(420, 420, 430, 430, fill='black')
        self.dice_dot2 = self.canvas.create_oval(420, 440, 430, 450, fill='black')
        self.dice_dot3 = self.canvas.create_oval(440, 420, 450, 430, fill='black')
        self.dice_dot4 = self.canvas.create_oval(440, 440, 450, 450, fill='black')

    def reset_game(self):
        self.player_position = 1
        self.draw_board()
        self.update_position()

    def draw_board(self):
        self.canvas.delete("all")
        size = 40
        rows = 10
        cols = 10

        for row in range(rows):
            for col in range(cols):
                x1 = col * size
                y1 = row * size
                x2 = x1 + size
                y2 = y1 + size
                color = 'white' if (row + col) % 2 == 0 else 'lightgrey'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='black')
                self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(row * cols + col + 1), font=('Arial', 10, 'bold'))

        self.draw_snakes_and_ladders()
        self.draw_player()

    def draw_snakes_and_ladders(self):
        snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

        for start, end in snakes.items():
            self.draw_snake(start, end)
        for start, end in ladders.items():
            self.draw_ladder(start, end)

    def draw_snake(self, start, end):
        start_pos = self.get_position(start)
        end_pos = self.get_position(end)
        self.canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1], fill='red', width=3)

    def draw_ladder(self, start, end):
        start_pos = self.get_position(start)
        end_pos = self.get_position(end)
        self.canvas.create_line(start_pos[0], start_pos[1], end_pos[0], end_pos[1], fill='green', width=3)

    def get_position(self, num):
        size = 40
        rows = 10
        cols = 10
        row = (num - 1) // cols
        col = (num - 1) % cols
        return (col * size + size / 2, (rows - row - 1) * size + size / 2)

    def draw_player(self):
        pos = self.get_position(self.player_position)
        self.canvas.delete("player")
        self.canvas.create_oval(pos[0] - 10, pos[1] - 10, pos[0] + 10, pos[1] + 10, fill='blue', outline='black', tags="player")

    def roll_dice(self):
        roll = random.randint(1, 6)
        self.dice_label.config(text=f"Hasil Dadu: {roll}")
        self.animate_dice(roll)
        self.player_position += roll

        if self.player_position > 100:
            self.player_position = 100

        # Implement ular dan tangga
        snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
        
        if self.player_position in snakes:
            self.player_position = snakes[self.player_position]
        elif self.player_position in ladders:
            self.player_position = ladders[self.player_position]

        self.update_position()
        self.draw_player()
        
        if self.player_position == 100:
            tk.messagebox.showinfo("Menang!", "Selamat, Anda menang!")

    def animate_dice(self, roll):
        for i in range(6):
            self.canvas.after(i * 100, self.update_dice, (roll + i) % 6 + 1)

    def update_dice(self, number):
        faces = {
            1: [(420, 420, 430, 430)],
            2: [(420, 420, 430, 430), (440, 440, 450, 450)],
            3: [(420, 420, 430, 430), (440, 440, 450, 450), (420, 440, 430, 450)],
            4: [(420, 420, 430, 430), (420, 440, 430, 450), (440, 420, 450, 430), (440, 440, 450, 450)],
            5: [(420, 420, 430, 430), (420, 440, 430, 450), (440, 420, 450, 430), (440, 440, 450, 450), (420, 440, 430, 450)],
            6: [(420, 420, 430, 430), (420, 440, 430, 450), (420, 460, 430, 470), (440, 420, 450, 430), (440, 440, 450, 450), (440, 460, 450, 470)]
        }

        self.canvas.delete("dice_dot")
        for dot in faces[number]:
            self.canvas.create_oval(dot, fill='black', outline='black', tags="dice_dot")

    def update_position(self):
        self.position_label.config(text=f"Posisi Pemain: {self.player_position}")

def main():
    root = tk.Tk()
    game = SnakeLadderGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
