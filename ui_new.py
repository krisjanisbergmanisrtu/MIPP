import tkinter as tk
from tkinter import messagebox
import random

from alpha_beta import alpha_beta
from game import computer_turn_time, calculate_average_time
from tree import *
from minimax import *
import time


class BinaryGame:
    def __init__(self, root):
        self.game_states_vals = None
        self.game_states = None
        self.root = root
        self.root.title("Binary Game")
        self.root.geometry("800x600")
        # Player setup
        self.player1 = Player()
        self.player2 = Player()
        self.human = Player()
        self.human.type = 'Human'
        self.computer = Player()
        self.computer.type = 'Computer'
        self.level_counter = 0
        self.best_state_index = 0
        # GUI elements
        self.setup_gui()

        # Points and other misc. things
        self.buttons = []
        self.clicked_buttons = []
        self.prev_node = 0
        self.node_to_select = 0
        self.algorithm = ''
        self.tree = tree
        self.add_points = False
        self.turn_time = 0

    def setup_gui(self):

        # Setup player choice frame
        self.setup_player_frame()

        # Setup algorithm choice frame
        self.setup_algorithm_frame()

        # Setup input frame
        self.setup_input_frame()

        # Setup binary sequence frame
        self.setup_binary_frame()

        # Setup info frame
        self.setup_info_frame()

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
        tk.Button(self.algorithm_frame, text="Alpha-beta", command=lambda: self.algo_choice('alpha-beta')).pack(
            side=tk.LEFT)

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

    def setup_info_frame(self):
        self.info_frame = tk.Frame(self.root)
        self.info_frame.pack(pady=5)
        tk.Label(self.info_frame, text="Starting game as player:").grid(row=1, column=1)
        self.label_init_player = tk.Label(self.info_frame, text="")
        self.label_init_player.grid(row=1, column=2)
        tk.Label(self.info_frame, text="Computer is using algorithm:").grid(row=2, column=1)
        self.label_init_algo = tk.Label(self.info_frame, text="")
        self.label_init_algo.grid(row=2, column=2)
        tk.Label(self.info_frame, text="Current player:").grid(row=3, column=1)
        self.label_cur_player = tk.Label(self.info_frame, text="")
        self.label_cur_player.grid(row=3, column=2)
        self.label_player_selected = tk.Label(self.info_frame, text="", anchor="e")
        self.label_selected_combo_0 = tk.Label(self.info_frame, text="", anchor="center")
        self.label_selected_combo_1 = tk.Label(self.info_frame, text="", anchor="center")
        self.label_selected_combo_2 = tk.Label(self.info_frame, text="", anchor="w")
        self.point_change = tk.Label(self.info_frame, text="")
        self.computer_time = tk.Label(self.info_frame, text="")
        self.end_result_label = tk.Label(self.info_frame, text="")
        self.label_player_selected.grid(row=4, column=1, padx=5, sticky="e")
        self.label_selected_combo_0.grid(row=4, column=2, padx=5, sticky="ew")
        self.label_selected_combo_1.grid(row=4, column=3, padx=5, sticky="ew")
        self.label_selected_combo_2.grid(row=4, column=4, padx=5, sticky="w")
        self.computer_time.grid(row=5, column=1)
        self.point_change.grid(row=6, column=1)
        self.end_result_label.grid(row=7, column=1)

    def setup_result_frame(self):
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=20)

        # self.end_result_label = tk.Label(self.result_frame, text="Game ongoing")
        # self.end_result_label.pack(fill="none", expand=True)

    def setup_binary_frame(self):
        self.binary_frame = tk.Frame(self.root)
        self.binary_frame.pack(pady=10)

    def setup_result_frame(self):
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=20)

        # Add text boxes for showing points for each player
        tk.Label(self.result_frame, text="Player 1 Points:").pack(side=tk.LEFT)
        self.player1_points_text = tk.Label(self.result_frame, height=1, width=5)
        self.player1_points_text.pack(side=tk.LEFT)

        tk.Label(self.result_frame, text="Player 2 Points:").pack(side=tk.LEFT)
        self.player2_points_text = tk.Label(self.result_frame, height=1, width=5)
        self.player2_points_text.pack(side=tk.LEFT)

        # Update points display
        self.update_points_display()

    def update_active_player(self):
        if self.human.state == 0 and self.computer.state == 1:
            self.label_cur_player.config(text="computer", fg="red")
        else:
            self.label_cur_player.config(text="human", fg="red")
        return

    def display_player_points(self):
        # Display points for each player
        self.update_points_display()

    def update_points_display(self):
        # Update points display
        if hasattr(self, 'prev_node'):
            if self.prev_node != 0:
                self.player1_points_text.config(text=f"{getattr(self.prev_node, 'p1_points')}")
                self.player2_points_text.config(text=f"{getattr(self.prev_node, 'p2_points')}")
            else:
                self.player1_points_text.config(text="0")
                self.player2_points_text.config(text="0")

    def player_choice(self, player):
        if player == 'human':
            self.player1 = self.human
            self.player2 = self.computer
            self.human.state = 1
            self.computer.state = 0
        elif player == 'computer':
            self.player1 = self.computer
            self.player2 = self.human
            self.computer.state = 1
            self.human.state = 0
        self.label_init_player.config(text=f"{player}", fg="red")
        self.label_cur_player.config(text=f"{player}", fg="red")
        print(self.player1.type + ' is starting the game')

    def algo_choice(self, algo):
        self.algorithm = algo
        self.label_init_algo.config(text=f"{algo}", fg="red")
        print('Algorithm is ' + algo)

    def gen_rand_sequence(self, length):
        return ''.join(str(random.randint(0, 1)) for _ in range(length))

    def fill_tree(self):
        # init_tree(self.binary_str)
        if self.prev_node != 0:
            init_tree(getattr(self.prev_node, 'value'))
            self.tree = tree
        else:
            init_tree(self.binary_str)
            self.tree = tree
            self.prev_node = self.tree[0]
            #self.gen_nodes()

    def gen_nodes(self):
        gen_node(self.prev_node, MAX_VISIBILITY)
        self.tree = tree

    def clear_tree(self):
        # self.prev_node = tree[0]
        # self.refresh_prev_node()
        temp_level = 0
        if (self.prev_node != 0):
            # If level is odd number then point assignment will flip unless we make it odd now
            if (self.prev_node.level % 2 != 0):
                temp_level = 1
            self.prev_node = self.prev_node._replace(indx=0, parent_indx=-1, level=temp_level)
        tree.clear()
        self.tree = tree
        self.best_state_index = 0

    def is_players_turn(self):
        # Check if it's the player's turn
        return self.player1.state == 1

    def update_game_log(self):
        # previous_node = self.prev_node
        # selected_node = self.game_states[self.best_state_index + 1]
        cur_player = self.label_cur_player.cget("text")
        best_combo_indxs = getattr(self.node_to_select, 'best_combo_indxs')[0]
        print("update_game_log()")
        print(f"self.prev_node = {self.prev_node}")
        print(f"self.node_to_select = {self.node_to_select}")

        selected_combo_0 = getattr(self.prev_node, 'value')[:best_combo_indxs]
        selected_combo_1_0 = getattr(self.prev_node, 'value')[best_combo_indxs]
        selected_combo_1_1 = getattr(self.prev_node, 'value')[best_combo_indxs + 1]
        selected_combo_2 = getattr(self.prev_node, 'value')[best_combo_indxs + 2:]
        self.label_player_selected.config(fg="blue",
                                          text=f"Game value was: {getattr(self.prev_node, 'value')}\n{cur_player} selected combination: ")
        self.label_selected_combo_0.config(fg="blue", text=f"{selected_combo_0}")
        self.label_selected_combo_1.config(fg="red", text=f"{selected_combo_1_0}{selected_combo_1_1}")
        self.label_selected_combo_2.config(fg="blue", text=f"{selected_combo_2}")

        combo = f"{getattr(self.prev_node, 'value')[best_combo_indxs]}{getattr(self.prev_node, 'value')[best_combo_indxs + 1]}"
        if getattr(self.prev_node, 'level') % 2 != 0:
            p_active = self.player2
            p_waiting = self.player1
        else:
            p_active = self.player1
            p_waiting = self.player2

        point_change = ""
        if combo == "00":
            point_change = f"+1 point to {p_active.type}"
        elif combo == "01":
            point_change = f"+1 point to {p_waiting.type}"
        elif combo == "10":
            point_change = f"-1 point from {p_waiting.type}"
        elif combo == "11":
            point_change = f"+1 point to {p_active.type}"

        self.point_change.config(fg="blue", text=f"{point_change}")
        return

    def update_game_log_computer_time(self):
        computer_turn_time.append(self.turn_time)
        self.computer_time.config(text=f"Computer latest turn done in {self.turn_time}ms")

    def process_computers_turn(self):
        # Implement logic to process the computer's turn here
        # Placeholder; replace with actual logic
        start_time = time.time()
        print('Computers turn')
        if len(self.buttons) >= 2:
            if self.algorithm == 'minmax':
                best_path, best_value = minimax(tree[0], 0, True)
            elif self.algorithm == 'alpha-beta':
                best_path, best_value = alpha_beta(tree[0], float('-inf'), float('inf'), MAX_VISIBILITY)

            self.game_states = [self.tree[idx] for idx in best_path]
            self.game_states_vals = [self.tree[idx].value for idx in best_path]
            # print(f"game_states\n{self.game_states_vals}")
            index0 = getattr(self.game_states[self.best_state_index + 1], 'best_combo_indxs')[0]
            index1 = getattr(self.game_states[self.best_state_index + 1], 'best_combo_indxs')[1]
            print(index1)
            self.buttons[index0].config(bg="light gray")
            self.buttons[index0].invoke()
            self.buttons[index1].config(bg="light gray")
            self.buttons[index1].invoke()
            self.computer.state = 0
            self.human.state = 1

            # print(
            #     f"self.computer.state set to'{self.computer.state}'\nself.computer.state set to'{self.computer.state}'")
            print("Computers turn done")
            self.update_active_player()
            end_time = time.time()
            self.turn_time = end_time - start_time
            self.update_game_log_computer_time()
        return

    def convert_to_binary_and_display(self):
        try:
            length = int(self.entry.get())
            # if not 3 <= length <= 25:
            if not 15 <= length <= 25:
                raise ValueError("Number out of range")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer between 15 and 25.")
            return

        #self.binary_str = self.gen_rand_sequence(length)
        self.binary_str = "10100"  # This line is for testing
        self.display_binary_sequence()
        # self.tree[0] = self.prev_node
        print(self.binary_str)
        self.level_counter += 1
        # self.fill_tree()
        self.prev_node = self.node_to_select = tree[0]
        # gen_node(self.tree[0],3)
        self.play_game()

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
        # self.clear_tree()
        if self.level_counter == 0:
            self.clear_tree()
            self.fill_tree()
            self.gen_nodes()

    def on_button_click(self, index):
        self.buttons[index].config(bg="light gray")
        if self.computer.state == 1 and self.human.state == 0:
            print(f"button with index'{index}' was clicked by Computer")
        else:
            print(f"button with index'{index}' was clicked by Human")
        # if self.is_players_turn():
        if index in self.clicked_buttons:
            return  # ignore if this button was already clicked
        self.clicked_buttons.append(index)

        if len(self.clicked_buttons) == 2:  # if exactly two btns have been clicked
            if abs(self.clicked_buttons[0] - self.clicked_buttons[1]) == 1:  # check if clicked btns adjacent
                new_str = ''
                keep_bit = min(self.clicked_buttons)
                clicked_str = str(self.buttons[self.clicked_buttons[0]].cget('text')) + " " + str(
                    self.buttons[self.clicked_buttons[1]].cget('text'))
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
                # self.gen_nodes()

                # string = "mid0"
                if self.level_counter % MAX_VISIBILITY == 0 and self.level_counter != 0:
                    # print(self.node_to_select)
                    temp_p1_points = self.prev_node.p1_points
                    temp_p2_points = self.prev_node.p2_points
                    temp_heuristic = self.prev_node.heuristic_val
                    self.clear_tree()
                    self.set_node_vals(temp_p1_points, temp_p2_points, temp_heuristic)
                    self.fill_tree()
                    self.gen_nodes()
                else:
                    self.player1.points = self.node_to_select.p1_points
                    self.player2.points = self.node_to_select.p2_points

                found_node = False
                for node in tree:
                    if str(node.value) == new_str and self.prev_node == 0:
                        self.set_node_to_select(node)
                        print(f"onbuttonclick1.self.prev_node = {self.prev_node}")
                        # string = "mid1"
                        found_node = True
                    if str(node.value) == new_str and node.parent_indx == getattr(self.prev_node, 'indx'):
                        self.set_node_to_select(node)
                        print(f"onbuttonclick2.self.prev_node = {self.prev_node}")
                        found_node = True
                if not found_node:
                    print(tree)
                        # string = "mid2"
                # print(string)
                # print(f"self.prev_node = {self.prev_node}")
                # print(f"self.node_to_select = {self.node_to_select}")

                self.update_game_log()
                self.refresh_prev_node()
                self.update_points_display()
                print("Button clicked")

                # if self.level_counter % MAX_VISIBILITY == 0 and self.level_counter != 0:
                #     # print(self.node_to_select)
                #     temp_p1_points = self.prev_node.p1_points
                #     temp_p2_points = self.prev_node.p2_points
                #     temp_heuristic = self.prev_node.heuristic_val
                #     self.clear_tree()
                #     self.set_node_vals(temp_p1_points, temp_p2_points, temp_heuristic)
                #     self.fill_tree()
                #     self.gen_nodes()
                # else:
                #     self.player1.points = self.node_to_select.p1_points
                #     self.player2.points = self.node_to_select.p2_points

                print(self.player1.points)
                print(self.player2.points)

                if self.human.state == 1 and self.computer.state == 0:
                    self.human.state = 0
                    self.computer.state = 1
                    self.update_active_player()
                    print("Humans turn done")
                    print(len(tree))
                    # if (len(tree) < 1):
                    #     self.clear_tree()
                    #     self.fill_tree()
                    #     self.gen_nodes()
                    self.play_game()
                    print(f"self.best_state_index  = {self.best_state_index}")

                self.check_results()

    def refresh_prev_node(self):
        print('refreshed_prev_node')
        self.prev_node = self.node_to_select

    def set_node_to_select(self, node):
        self.node_to_select = node

    def play_game(self):
        if self.human.state == 0 and self.computer.state == 1:
            self.update_active_player()
            self.process_computers_turn()
        else:
            print("humans turn")

    def check_results(self):
        print("node to select")
        print(self.node_to_select)
        # if self.node_to_select != 0 and len(getattr(self.node_to_select, 'value')) < 2:
        if self.node_to_select != 0 and len(self.buttons) < 2:
            print("Calculating game result")
            end_label = f"Average computer turn time: {calculate_average_time()}ms"
            node = self.node_to_select
            p1_points = getattr(node, 'p1_points')
            p2_points = getattr(node, 'p2_points')
            if p1_points == p2_points:
                end_label = f"Draw! {end_label}"
            elif p1_points > p2_points:
                end_label = f"{self.player1.type} Won! {end_label}"
            elif p2_points > p1_points:
                end_label = f"{self.player2.type} Won! {end_label}"
            self.end_result_label.config(text=f"{end_label}", bg="light gray")
            print("GAME OVER!")

    # def setPoints(self, temp_p1_points, temp_p2_points):
    #     self.prev_node.p1_points = temp_p1_points
    #     self.prev_node.p2_points = temp_p2_points

    def set_node_vals(self, temp_p1_points, temp_p2_points, temp_heuristic):
        self.prev_node = self.prev_node._replace(p1_points=temp_p1_points,
                                                 p2_points=temp_p2_points, heuristic_val=temp_heuristic)


class Player:
    def __init__(self):
        self.type = ''
        self.points = 0
        self.state = 0


root = tk.Tk()
game = BinaryGame(root)
root.mainloop()
