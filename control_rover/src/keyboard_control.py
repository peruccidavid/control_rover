import sys
import termios
import tty
import threading
import time
from control_motores import set_all_wheels_speed, stop_all_wheels, set_mosfet_state

def get_char():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def control_loop():
    while True:
        char = get_char()
        if char == '\x1b':  # Escape sequence
            next_char = get_char()
            if next_char == '[':
                direction = get_char()
                if direction == 'A':  # Up arrow
                    print("Moving forward at full speed.")
                    set_all_wheels_speed(100)
                elif direction == 'B':  # Down arrow
                    print("Reversing.")
                    set_all_wheels_speed(-100)
                elif direction == 'C':  # Right arrow
                    print("Turning right 45 degrees.")
                    # Implement turning logic here
                    set_all_wheels_speed(100)  # Adjust speeds for turning
                    time.sleep(1)  # Duration for turn
                    stop_all_wheels()
                elif direction == 'D':  # Left arrow
                    print("Turning left 45 degrees.")
                    # Implement turning logic here
                    set_all_wheels_speed(100)  # Adjust speeds for turning
                    time.sleep(1)  # Duration for turn
                    stop_all_wheels()
        elif char == 's':  # 's' key to stop
            print("Stopping all motors.")
            stop_all_wheels()
        elif char == 'q':  # 'q' key to quit
            print("Exiting control loop.")
            stop_all_wheels()
            break

if __name__ == "__main__":
    set_mosfet_state("ON")
    try:
        print("Starting keyboard control. Use arrow keys to control the rover.")
        control_thread = threading.Thread(target=control_loop)
        control_thread.start()
        control_thread.join()
    except KeyboardInterrupt:
        print("Control interrupted by user.")
    finally:
        stop_all_wheels()
        set_mosfet_state("OFF")