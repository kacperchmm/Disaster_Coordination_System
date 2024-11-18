import time
import sys

def spinner(seconds):
    spinner_chars = ['|', '/', '-', '\\']
    end_time = time.time() + seconds

    while time.time() < end_time:
        for char in spinner_chars:
            sys.stdout.write(f'\r{char}')
            sys.stdout.flush()
            time.sleep(0.2)

    sys.stdout.write('\rDone!\n')