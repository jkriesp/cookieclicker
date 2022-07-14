from concurrent.futures import thread
from rich import print, pretty
import time
from threading import Thread
import os
from getkey import getkey
import time
import timeit
from pyfiglet import Figlet
import threading

pretty.install()


def ac():
    global cookies

    while True:
        cookies += 10
        if exit_event.is_set():
            break
        time.sleep(5)
        



def clear():
    os.system('clear')

auto_clicker = Thread(target=ac)
#auto_clicker.start()

# stats
cookies = 0
cps = 1

# Print ASCII header
header = Figlet(font='smslant')
print_header = header.renderText("Cookie Clicker")

# Define thread exit event
exit_event = threading.Event()

clear()
while True:
    print(f"""{print_header}\n 
        {cookies} 🍪""")
    
    start = timeit.default_timer()

    click = getkey()
    end = timeit.default_timer()

    if click == "\n" and end - start > 0.04:  # prevent spam
        cookies += 1

    elif click == "q":
        exit_event.set()
        clear()
        break

    elif click == "a" and not auto_clicker.is_alive():
        auto_clicker.start()

    elif click == "u":
        clear()
    
    time.sleep(0.04)
    clear()
