import tkinter as tk
from tkinter import messagebox
from collections import namedtuple
import random
from tree import *
from minimax import *

class BinaryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Game")
        self.root.geometry("600x400")
        # Player setup
        self.player1 = Player()
        self.player2 = Player()
        self.level_counter = 0
        # GUI elements
        self.setup_gui()

        # Points and other misc. things
        self.buttons = []
        self.clicked_buttons = []
        self.prev_node = 0
        self.algorithm = ''
        self.tree = tree
        self.add_points = False
    def setup_gui(self):
        # Setup player choice frame
        self.setup_player_frame()

        # Setup algorithm choice frame
        self.setup_algorithm_frame()

        # Setup input frame
        self.setup_input_frame()

        # Setup binary sequence frame
        self.setup_binary_frame()

        # Setup result frame
        self.setup_result_frame()

    def setup_player_frame(self):
        self.player_frame = tk.Frame(self.root)
        self.player_frame.pack(pady=5)

        tk.Label(self.player_frame, text="Who is starting?").pack(side=tk.LEFT)

        tk.Button(self.player_frame, text="Computer", command=lambda: self.player_choice('computer')).pack(side=tk.LEFT)
        tk.Button(self.player_frame, text="Human", command=lambda: self.player_choice('human')).pack(side=tk.LEFT)

    def setup_algorithm_frame(self):
        self.algorithm_frame = tk.Frame(self.root)
        self.algorithm_frame.pack(pady=5)

        tk.Label(self.algorithm_frame, text="Choose an algorithm").pack(side=tk.LEFT)

        tk.Button(self.algorithm_frame, text="Min-max", command=lambda: self.algo_choice('minmax')).pack(side=tk.LEFT)
        tk.Button(self.algorithm_frame, text="Alpha-beta", command=lambda: self.algo_choice('alpha-beta')).pack(side=tk.LEFT)

    def setup_input_frame(self):
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=20)

        tk.Label(self.input_frame, text="Enter length for sequence generation (15-25):").pack(side=tk.LEFT)

        self.entry = tk.Entry(self.input_frame, width=5)
        self.entry.pack(side=tk.LEFT, padx=10)

        tk.Button(self.input_frame, text="Convert", command=self.convert_to_binary_and_display).pack(side=tk.LEFT)

    def setup_binary_frame(self):
        self.binary_frame = tk.Frame(self.root)
        self.binary_frame.pack(pady=10)

    def setup_result_frame(self):
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=20)

        self.end_result_label = tk.Label(self.result_frame, text="Game ongoing")
        self.end_result_label.pack(fill="none", expand=True)

    def setup_input_frame(self):
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=20)

        tk.Label(self.input_frame, text="Enter length for sequence generation (15-25):").pack(side=tk.LEFT)

        self.entry = tk.Entry(self.input_frame, width=5)
        self.entry.pack(side=tk.LEFT, padx=10)

        tk.Button(self.input_frame, text="Convert", command=self.convert_to_binary_and_display).pack(side=tk.LEFT)

    def setup_binary_frame(self):
        self.binary_frame = tk.Frame(self.root)
        self.binary_frame.pack(pady=10)

    def setup_result_frame(self):
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=20)

        # Add text boxes for showing points for each player
        tk.Label(self.result_frame, text="Player 1 Points:").pack(side=tk.LEFT)
        self.player1_points_text = tk.Text(self.result_frame, height=1, width=5)
        self.player1_points_text.pack(side=tk.LEFT)

        tk.Label(self.result_frame, text="Player 2 Points:").pack(side=tk.LEFT)
        self.player2_points_text = tk.Text(self.result_frame, height=1, width=5)
        self.player2_points_text.pack(side=tk.LEFT)

        # Update points display
        self.update_points_display()

    def display_player_points(self):
        # Display points for each player
        self.player1_points_text.delete(1.0, tk.END)
        self.player1_points_text.insert(tk.END, str(self.player1_points))
        self.player2_points_text.delete(1.0, tk.END)
        self.player2_points_text.insert(tk.END, str(self.player2_points))

    def update_points_display(self):
        # Update points display
        self.player1_points_text.delete(1.0, tk.END)
        self.player1_points_text.insert(tk.END, str(self.player1.points))
        self.player2_points_text.delete(1.0, tk.END)
        self.player2_points_text.insert(tk.END, str(self.player2.points))

    def player_choice(self, player):
        if player == 'human':
            self.player1.type = 'human'
            self.player2.type = 'computer'
            self.player1.state = 1
            self.player2.state = 0
        elif player == 'computer':
            self.player1.type = 'computer'
            self.player2.type = 'human'
            self.player1.state = 0
            self.player2.state = 1

        print(self.player1.type + ' is starting the game')

    def algo_choice(self, algo):
        self.algorithm = algo
        print('Algorithm is ' + algo)

    def gen_rand_sequence(self, length):
        return ''.join(str(random.randint(0, 1)) for _ in range(length))
    def fill_tree(self):
        init_tree(self.binary_str)
        self.tree = tree
        self.prev_node = tree[0]
    def gen_nodes(self):
        gen_node(self.prev_node,3)
        self.tree = tree
    def clear_tree(self):
        self.prev_node = tree[0]
        self.prev_node = self.prev_node._replace(indx=0,parent_indx=-1)
        tree.clear()
        self.tree = tree


    def is_players_turn(self):
        # Check if it's the player's turn
        return self.player1.state == 1

    def process_computers_turn(self):
        # Implement logic to process the computer's turn here
        pass  # Placeholder; replace with actual logic

    def convert_to_binary_and_display(self):
        try:
            length = int(self.entry.get())
            if not 4 <= length <= 25:
                raise ValueError("Number out of range")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer between 15 and 25.")
            return

        self.binary_str = self.gen_rand_sequence(length)
        self.display_binary_sequence()
        #self.tree[0] = self.prev_node
        print(self.binary_str)
        self.level_counter += 1
        self.fill_tree()
        #gen_node(self.tree[0],3)


    def display_binary_sequence(self):
        if not self.player1.type or not self.algorithm:
            messagebox.showerror("Error", "Please choose both player and algorithm.")
            return

        self.clicked_buttons = []
        for widget in self.binary_frame.winfo_children():
            widget.destroy()

        self.buttons = []
        for index, bit in enumerate(self.binary_str):
            button = tk.Button(self.binary_frame, text=bit, command=lambda idx=index: self.on_button_click(idx))
            button.pack(side=tk.LEFT, padx=2)
            self.buttons.append(button)
        self.fill_tree()

    def on_button_click(self, index):
        if self.is_players_turn():
            if index in self.clicked_buttons:
                return  # ignore if this button was already clicked
            self.clicked_buttons.append(index)

            new_str = self.binary_str
            if len(self.clicked_buttons) == 2:  # if exactly two btns have been clicked
                if abs(self.clicked_buttons[0] - self.clicked_buttons[1]) == 1:  # check if clicked btns adjacent
                    new_str = ''
                    keep_bit = min(self.clicked_buttons)
                    clicked_str = str(self.buttons[self.clicked_buttons[0]].cget('text')) + " " + str(self.buttons[self.clicked_buttons[1]].cget('text'))
                    new_bit = {
                        "0 1": "0",
                        "0 0": "1",
                        "1 0": "1",
                        "1 1": "0",
                    }
                    # Make adjacent clicked buttons disappear
                    self.buttons[self.clicked_buttons[0]].pack_forget()
                    self.buttons[self.clicked_buttons[1]].pack_forget()
                    for i in range(len(self.buttons)):
                        if i not in self.clicked_buttons:
                            new_str = new_str + self.buttons[i].cget('text')
                    new_str = new_str[:keep_bit] + new_bit[clicked_str] + new_str[keep_bit:]
                    self.binary_str = new_str
                    self.display_binary_sequence()
                    self.level_counter += 1
                    self.gen_nodes()
                    for node in tree:
                        if str(node.value) == new_str and self.prev_node==0:
                            self.prev_node = node
                        if str(node.value) == new_str and node.parent_indx==self.prev_node.indx:
                            self.prev_node = node
                    if self.level_counter % 3 == 0 and self.level_counter!=0:
                        print(self.prev_node)
                        self.clear_tree()
                    print(self.prev_node)
                    self.player1.points = self.prev_node.p1_points
                    self.player2.points = self.prev_node.p2_points
                    print(self.player1.points)
                    print(self.player2.points)
                    self.update_points_display()




class Player:
    def __init__(self):
        self.type = ''
        self.points = 0
        self.state = 0

root = tk.Tk()
game = BinaryGame(root)
root.mainloop()
