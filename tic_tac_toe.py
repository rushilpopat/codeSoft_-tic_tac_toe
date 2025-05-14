from tkinter import *
from tkinter import messagebox

root = Tk()
root.geometry("360x600")
root.title("Tic Tac Toe")
root.resizable(0, 0)
root.configure(bg="#121212")

board = {i: " " for i in range(1, 10)}
turn = "x"
game_end = False
mode = "singlePlayer"

def change_mode(new_mode):
    global mode
    mode = new_mode
    single_btn.config(bg="#03DAC5" if mode == "singlePlayer" else "#2A2A2A", fg="black" if mode == "singlePlayer" else "white")
    multi_btn.config(bg="#03DAC5" if mode == "multiPlayer" else "#2A2A2A", fg="black" if mode == "multiPlayer" else "white")

def update_board():
    for i in board:
        buttons[i - 1]["text"] = board[i]

def check_win(player):
    win_positions = [
        [1, 2, 3], [4, 5, 6], [7, 8, 9],
        [1, 4, 7], [2, 5, 8], [3, 6, 9],
        [1, 5, 9], [3, 5, 7]
    ]
    return any(all(board[pos] == player for pos in combo) for combo in win_positions)

def check_draw():
    return all(space != " " for space in board.values())

def restart_game():
    global game_end, turn
    if messagebox.askyesno("Restart Game", "Restart the game?"):
        for i in board:
            board[i] = " "
        for btn in buttons:
            btn["text"] = " "
        turn = "x"
        game_end = False
        title_lbl.config(text="Tic Tac Toe")
        status_lbl.config(text="Turn: X")

def minimax(state, is_max):
    if check_win("o"): return 1
    if check_win("x"): return -1
    if check_draw(): return 0

    best = -100 if is_max else 100
    for i in state:
        if state[i] == " ":
            state[i] = "o" if is_max else "x"
            score = minimax(state, not is_max)
            state[i] = " "
            best = max(best, score) if is_max else min(best, score)
    return best

def computer_move():
    best_score = -100
    best_move = 0
    for i in board:
        if board[i] == " ":
            board[i] = "o"
            score = minimax(board, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                best_move = i
    board[best_move] = "o"
    update_board()

def play(event):
    global turn, game_end
    if game_end:
        return

    btn = event.widget
    idx = buttons.index(btn) + 1

    if board[idx] == " ":
        board[idx] = turn
        update_board()

        if check_win(turn):
            title_lbl.config(text=f"{turn.upper()} Wins!")
            game_end = True
        elif check_draw():
            title_lbl.config(text="Game Draw")
            game_end = True

        turn = "o" if turn == "x" else "x"
        status_lbl.config(text=f"Turn: {turn.upper()}")

        if mode == "singlePlayer" and turn == "o" and not game_end:
            computer_move()
            if check_win("o"):
                title_lbl.config(text="O Wins!")
                game_end = True
            elif check_draw():
                title_lbl.config(text="Game Draw")
                game_end = True
            turn = "x"
            status_lbl.config(text="Turn: X")

# ----- UI -----
title_lbl = Label(root, text="Tic Tac Toe", font=("Helvetica", 28, "bold"), fg="#FFFFFF", bg="#121212")
title_lbl.pack(pady=20)

# Top-right restart button
restart_top_btn = Button(
    root,
    text="↻",
    font=("Arial", 16, "bold"),
    bg="#FF6B6B",
    fg="white",
    width=3,
    height=1,
    relief=FLAT,
    bd=0,
    command=restart_game
)
restart_top_btn.place(x=310, y=10)

mode_frame = Frame(root, bg="#121212")
mode_frame.pack(pady=10)

single_btn = Button(mode_frame, text="Single Player", font=("Arial", 14, "bold"), width=14, bg="#03DAC5", fg="black", bd=0, relief=FLAT, command=lambda: change_mode("singlePlayer"))
single_btn.grid(row=0, column=0, padx=10)

multi_btn = Button(mode_frame, text="Multiplayer", font=("Arial", 14, "bold"), width=14, bg="#2A2A2A", fg="white", bd=0, relief=FLAT, command=lambda: change_mode("multiPlayer"))
multi_btn.grid(row=0, column=1, padx=10)

board_frame = Frame(root, bg="#121212")
board_frame.pack(pady=30)

buttons = []
for i in range(3):
    for j in range(3):
        btn = Button(board_frame, text=" ", font=("Arial", 28, "bold"), width=4, height=2, bg="#1F1F1F", fg="#FFFFFF", relief=FLAT, activebackground="#333", activeforeground="#03DAC5")
        btn.grid(row=i, column=j, padx=6, pady=6)
        btn.bind("<Button-1>", play)
        buttons.append(btn)

# Bottom restart button
restart_btn = Button(
    root,
    text="🔄 Restart Game",
    font=("Arial", 16, "bold"),
    bg="#FF6B6B",
    fg="white",
    relief=FLAT,
    bd=0,
    padx=20,
    pady=5,
    command=restart_game
)
restart_btn.pack(pady=15)

status_lbl = Label(root, text="Turn: X", font=("Arial", 18, "bold"), bg="#121212", fg="#FFFFFF")
status_lbl.pack(pady=10)

# Keyboard shortcut to restart with "r" or "R"
root.bind("r", lambda e: restart_game())
root.bind("R", lambda e: restart_game())

root.mainloop()
