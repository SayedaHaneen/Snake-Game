import tkinter as tk
import random

# Game configuration
GAME_WIDTH = 600
GAME_HEIGHT = 400
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#39FF14"  # Neon green
FOOD_COLOR = "#FF3131"   # Neon red
BACKGROUND_COLOR = "#000000"  # Black for neon theme

# Global variables
score = 0
direction = 'right'
canvas = None
label = None

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for _ in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )

def next_turn(snake, food):
    global score, direction, label

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    opposites = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
    if direction != opposites.get(new_direction):
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body in snake.coordinates[1:]:
        if x == body[0] and y == body[1]:
            return True

    return False

def game_over():
    global canvas

    canvas.delete(tk.ALL)
    canvas.create_text(
        GAME_WIDTH // 2, GAME_HEIGHT // 3,
        font=('Consolas', 36),
        text="GAME OVER", fill="#FF3131", tag="gameover"
    )
    canvas.create_text(
        GAME_WIDTH // 2, GAME_HEIGHT // 2,
        font=('Consolas', 20),
        text=f"Final Score: {score}", fill="white"
    )

    # Buttons after 2 seconds
    def show_buttons():
        play_again_btn = tk.Button(
            window, text="▶ PLAY AGAIN", font=('Consolas', 16),
            bg="#1F1FFF", fg="white", width=20,
            command=start_game
        )
        play_again_btn.pack(pady=10)

        exit_btn = tk.Button(
            window, text="❌ EXIT", font=('Consolas', 16),
            bg="#B22222", fg="white", width=20,
            command=window.destroy
        )
        exit_btn.pack(pady=5)

    window.after(2000, show_buttons)

def start_game():
    global canvas, score, direction, label

    clear_window()
    score = 0
    direction = 'right'

    label = tk.Label(
        window, text=f"Score: {score}",
        font=('Consolas', 20),
        bg=BACKGROUND_COLOR, fg="white"
    )
    label.pack()

    canvas = tk.Canvas(
        window, bg=BACKGROUND_COLOR,
        height=GAME_HEIGHT, width=GAME_WIDTH
    )
    canvas.pack()

    window.bind('<Left>', lambda e: change_direction('left'))
    window.bind('<Right>', lambda e: change_direction('right'))
    window.bind('<Up>', lambda e: change_direction('up'))
    window.bind('<Down>', lambda e: change_direction('down'))

    snake = Snake()
    food = Food()
    next_turn(snake, food)

def show_instructions():
    clear_window()

    title = tk.Label(
        window, text="📘 How to Play",
        font=('Arial Black', 28),
        fg="#00FFFF", bg=BACKGROUND_COLOR
    )
    title.pack(pady=20)

    info = (
        "🎮 Use arrow keys to control the snake.\n\n"
        "🍎 Eat the red food to grow and earn points.\n\n"
        "💥 Avoid hitting walls or your own tail.\n\n"
        "⌛ Game ends if you collide.\n\n"
        "🚀 Try to score as high as you can!\n"
    )

    text = tk.Label(
        window, text=info, font=('Consolas', 16),
        fg="white", bg=BACKGROUND_COLOR, justify="left"
    )
    text.pack(pady=10)

    back_btn = tk.Button(
        window, text="⬅ BACK", font=('Consolas', 16),
        bg="#5555FF", fg="white", width=20,
        command=show_main_menu
    )
    back_btn.pack(pady=20)

def show_main_menu():
    clear_window()

    title = tk.Label(
        window, text="🐍 Snake Rush",
        font=('Arial Black', 32),
        fg="#39FF14", bg=BACKGROUND_COLOR
    )
    title.pack(pady=30)

    play_btn = tk.Button(
        window, text="▶ PLAY", font=('Consolas', 20),
        bg="#1F1FFF", fg="white", width=20,
        command=start_game
    )
    play_btn.pack(pady=15)

    instructions_btn = tk.Button(
        window, text="📘 INSTRUCTIONS", font=('Consolas', 20),
        bg="#FF8C00", fg="black", width=20,
        command=show_instructions
    )
    instructions_btn.pack(pady=15)

    quit_btn = tk.Button(
        window, text="❌ EXIT", font=('Consolas', 20),
        bg="#B22222", fg="white", width=20,
        command=window.destroy
    )
    quit_btn.pack(pady=15)

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

# Setup window
window = tk.Tk()
window.title("Snake Rush")
window.config(bg=BACKGROUND_COLOR)
window.resizable(False, False)

show_main_menu()
window.mainloop()
