import tkinter as tk
from tkinter import messagebox
from tree import *
import random

computer_result = 0
human_result = 0
binary_str = ''
level_counter = 0
p1_points = 0
p2_points = 0
prev_node = 0
sum_flag = True
def player_choice():
    # placeholder
    pass


def algo_choice():
    # placeholder
    pass


def gen_rand_sequence(length):
    # generate a rand sequence with 0s and 1s
    seq = ""
    for i in range(length):
        seq = seq + str(random.randint(0, 1))
    return seq


def convert_to_binary_and_display(binary_str):
    # clear previous buttons and reset the list of buttons and clicked status
    for widget in binary_frame.winfo_children():
        widget.destroy()
    buttons.clear()
    clicked_buttons.clear()
    # check if function called to generate a new game or called to continue the game
    if (len(binary_str) < 1):
        try:
            length = int(entry.get())
            if not 15 <= length <= 25:
                raise ValueError("Number out of range")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer between 15 and 25.")
            return

        binary_str = gen_rand_sequence(length)  # generate random binary str for new game
        init_tree(binary_str)
        gen_node(tree[0],3)
        global computer_result
        global human_result
        computer_result = 0
        human_result = 0
        #computer_result_label.config(text=str("Computer" + " " + str(computer_result)))

    else:
        binary_str = binary_str
        global level_counter
        global prev_node
        global sum_flag
        if level_counter % 3 == 0:
            tree.clear()
            init_tree(binary_str)
            gen_node(tree[0],3)
            level_counter = 0
            prev_node = 0
            sum_flag = True
        else:
            sum_flag = False
        level_counter += 1

    # generate btns for sequence
    for index, bit in enumerate(binary_str):
        button = tk.Button(binary_frame, text=bit, command=lambda idx=index: on_button_click(idx))
        button.pack(side=tk.LEFT, padx=2)
        buttons.append(button)  # Add the button to the list
        # button_idx_map[button]=index
    #print(tree)

def on_button_click(index):
    # add btn to clicked btns
    if index in clicked_buttons:
        return  # ignore if this button was already clicked
    clicked_buttons.append(index)

    new_str = binary_str
    if len(clicked_buttons) == 2:  # if exactly two btns have been clicked
        if abs(clicked_buttons[0] - clicked_buttons[1]) == 1:  # check if clicked btns adjacent
            new_str = ''
            keep_bit = min(clicked_buttons)
            clicked_str = str(buttons[clicked_buttons[0]].cget('text')) + " " + str(buttons[clicked_buttons[1]].cget('text'))
            new_bit = {
                "0 1": "0",
                "0 0": "1",
                "1 0": "1",
                "1 1": "0",
            }
            # Make adjacent clicked buttons disappear
            buttons[clicked_buttons[0]].pack_forget()
            buttons[clicked_buttons[1]].pack_forget()
            ## todo: add new bits to the binary string
            for i in range(len(buttons)):
                if i not in clicked_buttons:
                    new_str = new_str + buttons[i].cget('text')
            new_str = new_str[:keep_bit] + new_bit[clicked_str] + new_str[keep_bit:]
            # Reset the clicked buttons list
            global p1_points
            global p2_points
            #computer_result += 1
            clicked_buttons.clear()
            global prev_node
            print(len(tree))
            for node in tree:
                if str(node.value) == new_str and prev_node == 0:
                    prev_node = node
                    print(node)
                    p1_points = p1_points+node.p1_points
                    p2_points = p2_points+node.p2_points
                    #print(p1_points)
                    #print(p2_points)
                    computer_result_label.config(text=str("Computer" + " " + str(p1_points)))
                    human_result_label.config(text=str("Human" + " " + str(p2_points)))
                elif str(node.value) == new_str and node.parent_indx==prev_node.indx:
                    prev_node = node
                    print(node)
                    #print('newnode')
                    p1_points = node.p1_points
                    p2_points = node.p2_points
                    #print(p1_points)
                    #print(p2_points)
                    computer_result_label.config(text=str("Computer" + " " + str(p1_points)))
                    human_result_label.config(text=str("Human" + " " + str(p2_points)))
            # generate new btns
            #print(len(new_str))
            convert_to_binary_and_display(new_str)
            # if less then 2 btns left game over
            if (len(new_str) == 0):
                end_result_label.config(text='game over')
                for widget in binary_frame.winfo_children():
                    widget.destroy()
                    buttons.clear()
                    clicked_buttons.clear()

        clicked_buttons.clear()


root = tk.Tk()
root.title("1.praktiskais darbs")
setting_frame = tk.Frame(root)
setting_frame.pack(pady=0)

# Player choice UI
player_choice_label = tk.Label(setting_frame, text="Who is starting?")
player_choice_label.pack(side=tk.LEFT)

computer_btn = tk.Button(setting_frame, text="Computer", command=player_choice)
computer_btn.pack(side=tk.LEFT)

player_btn = tk.Button(setting_frame, text="Human", command=player_choice)
player_btn.pack(side=tk.LEFT)

# Algo choice UI
algo_frame = tk.Frame(root)
algo_frame.pack(pady=5)
algo_choice_label = tk.Label(algo_frame, text="Choose an algorithm")
algo_choice_label.pack(side=tk.LEFT)

minmax_btn = tk.Button(algo_frame, text="Min-max", command=player_choice)
minmax_btn.pack(side=tk.LEFT)

alpha_beta_btn = tk.Button(algo_frame, text="Alpha-beta", command=player_choice)
alpha_beta_btn.pack(side=tk.LEFT)

# Frame for the input field and submit button
input_frame = tk.Frame(root)
input_frame.pack(pady=20)

# Entry widget for user input
entry_label = tk.Label(input_frame, text="Enter length for sequence generation (15-25):")
entry_label.pack(side=tk.LEFT)

entry = tk.Entry(input_frame, width=5)
entry.pack(side=tk.LEFT, padx=10)

# Submit button(start game)
submit_btn = tk.Button(input_frame, text="Convert", command=lambda: convert_to_binary_and_display(''))
submit_btn.pack(side=tk.LEFT)

# Frame for displaying 0/1 btn
binary_frame = tk.Frame(root)
binary_frame.pack(pady=10)
# Frame for result update
state_frame = tk.Frame(root)
state_frame.pack(pady=15)

human_result_label = tk.Label(state_frame, text=str("Human" + " " + " "))
human_result_label.pack(side=tk.LEFT)

computer_result_label = tk.Label(state_frame, text=str("Computer" + " " +" "))
computer_result_label.pack(side=tk.RIGHT)

result_frame = tk.Frame(root)
result_frame.pack(pady=20)
end_result_label = tk.Label(result_frame, text="game ongoing")
end_result_label.pack(fill="none", expand=True)

# Initialize a list to keep track of btns and clicked btns
buttons = []
clicked_buttons = []
button_idx_map = {}

root.mainloop()
