import os
import shutil
import sys
import time

def hide_cursor():
    sys.stdout.write("\033[?25l")
    sys.stdout.flush()

def show_cursor():
    sys.stdout.write("\033[?25h")
    sys.stdout.flush()

def sprint(text, delay=0.1, end="\n"):
    
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write(end)
    sys.stdout.flush()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def get_terminal_size():
    return shutil.get_terminal_size()


def print_centered(lines_list, prompt_text=None, footer=None):
    hide_cursor()
    columns, lines = shutil.get_terminal_size()
    clear_screen()
    content_height = len(lines_list)
    if prompt_text:
        content_height += 1

    vertical_padding = (lines - content_height) // 2
    print("\n" * vertical_padding, end="")

    align_lengths = []
    for l in lines_list:
        s_line = l.strip()
        if ":" in l:
            align_lengths.append(len(l.split(":", 1)[0] + ":  "))
        elif s_line and s_line[0].isdigit() and "." in s_line:
            align_lengths.append(len(l))
    
    if not prompt_text == None:
        align_lengths.append(len(prompt_text))
    
    fixed_padding = (columns - max(align_lengths)) // 2 if align_lengths else 0

    for line in lines_list:
        s_line = line.strip()
        if ":" in line:
            parts = line.split(":", 1)
            label = parts[0] + ": "
            value = parts[1].strip()
            print(" " * fixed_padding + label + value)
        elif s_line and s_line[0].isdigit() and "." in s_line:
            print(" " * fixed_padding + line)
        else:
            print(line.center(columns))

    if not prompt_text == None:
        #print(" " * max(0, fixed_padding), end="")
        input_center_padding = (columns // 2) - (len(prompt_text) // 2)
        print(" " * max(0, input_center_padding), end="")
        if footer:
            print(f"\033[{lines};1H{footer}", end="")
            print(f"\033[{vertical_padding + content_height};{fixed_padding + 1}H", end="")
        
        show_cursor()    
        s = input(prompt_text)
        hide_cursor()
        return s
    
    print("\n" * (vertical_padding - 1))
    return None

def centered_slow_print(static_lines, slow_line, delay=0.1):
    columns, lines = shutil.get_terminal_size()
    
    total_height = len(static_lines) + 1
    start_row = (lines - total_height) // 2
    
    for i, line in enumerate(static_lines):
        row = start_row + i
        print(f"\033[{row};1H" + line.center(columns))
    
    slow_row = start_row + len(static_lines)
    left_padding = (columns - len(slow_line)) // 2
    
    print(f"\033[{slow_row};1H" + (" " * max(0, left_padding)), end="")
    sys.stdout.flush()
    time.sleep(1)
    for char in slow_line:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    
    print() 

def draw_footer(text):
    print("\033[s", end="")
    rows, cols = shutil.get_terminal_size()
    print(f"\033[{rows};1H\033[K{text}", end="", flush=True)
    print("\033[u", end="", flush=True)
