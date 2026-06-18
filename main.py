import pyautogui
import pyperclip
import keyboard
import time
import random
import re
import json

# ------------------------
# Load config
# ------------------------
with open("config.json", "r") as f:
    config = json.load(f)

# ------------------------
# File locations
# ------------------------
DATA_FOLDER = "data"

SENT_FILE = f"{DATA_FOLDER}/sent.txt"
REMAINING_FILE = f"{DATA_FOLDER}/remaining.txt"
LOG_FILE = f"{DATA_FOLDER}/log.txt"

# ------------------------
# Load sent cards
# ------------------------
try:
    with open(SENT_FILE, "r") as f:
        sent_codes = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    sent_codes = set()

# ------------------------
# Load remaining cards
# ------------------------
try:
    with open(REMAINING_FILE, "r") as f:
        remaining_codes = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    remaining_codes = []

# ------------------------
# Ask for page if empty
# ------------------------
if len(remaining_codes) == 0:

    print("\nPaste your entire Sofi page below.")
    print("Press Enter on an empty line when finished.\n")

    lines = []

    while True:
        line = input()

        if line == "":
            break

        lines.append(line)

    raw_text = "\n".join(lines)

    # Split by commas, spaces and newlines
    tokens = re.split(r"[,\s]+", raw_text)

    codes = []

    for token in tokens:

        token = token.strip()

        if not token:
            continue

        if re.fullmatch(r"[a-zA-Z0-9]{5,8}", token):
            codes.append(token)

    # Remove duplicates while preserving order
    codes = list(dict.fromkeys(codes))

    # Skip already sent cards
    codes = [c for c in codes if c not in sent_codes]

    with open(REMAINING_FILE, "w") as f:
        f.write("\n".join(codes))

    remaining_codes = codes

# ------------------------
# Variables
# ------------------------
TOTAL = len(remaining_codes)
completed = 0
paused = False
start_time = time.time()

print(f"\nLoaded {TOTAL} cards.")
print("Switch to Discord channel...")
print(f"Starting in {config['startup_delay']} seconds...\n")

time.sleep(config["startup_delay"])

# ------------------------
# Main loop
# ------------------------
while True:

    # Pause / Resume
    if keyboard.is_pressed("F8"):

        paused = not paused

        if paused:
            print("\n=== PAUSED ===")
        else:
            print("\n=== RESUMED ===")

        time.sleep(1)

    # Emergency stop
    if keyboard.is_pressed("F9"):
        print("\nStopped.")
        break

    if paused:
        time.sleep(0.5)
        continue

    # Load remaining cards
    with open(REMAINING_FILE, "r") as f:
        remaining = [line.strip() for line in f if line.strip()]

    if len(remaining) == 0:
        print("\n=================================")
        print("All cards completed!")

        runtime = time.time() - start_time

        minutes = int(runtime // 60)
        seconds = int(runtime % 60)

        print(f"Completed : {completed}")
        print(f"Runtime   : {minutes}m {seconds}s")

        if completed > 0:
            print(f"Average   : {runtime/completed:.1f}s/card")

        print("=================================")

        break

    code = remaining[0]

    command = f"sv {code}"

    # Copy command
    pyperclip.copy(command)

    # Delay before paste
    pre_paste_delay = random.uniform(
        config["pre_paste_min"],
        config["pre_paste_max"]
    )

    print(
        f"Waiting {pre_paste_delay:.2f}s before pasting..."
    )

    time.sleep(pre_paste_delay)

    # Paste
    pyautogui.hotkey("ctrl", "v")

    # Delay before enter
    post_paste_delay = random.uniform(
        config["post_paste_min"],
        config["post_paste_max"]
    )

    print(
        f"Waiting {post_paste_delay:.2f}s before pressing Enter..."
    )

    time.sleep(post_paste_delay)

    # Send
    pyautogui.press("enter")

    completed += 1

    elapsed = time.time() - start_time
    average_time = elapsed / completed
    remaining_cards = TOTAL - completed
    eta = average_time * remaining_cards

    print(
        f"\n[{completed}/{TOTAL}] Sent {command}"
    )

    print(
        f"Average: {average_time:.1f}s/card | "
        f"ETA: {eta/60:.1f} min"
    )

    # Save to sent.txt
    with open(SENT_FILE, "a") as f:
        f.write(code + "\n")

    # Save to log.txt
    with open(LOG_FILE, "a") as f:
        f.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} -> {command}\n"
        )

    # Remove current card
    with open(REMAINING_FILE, "w") as f:
        f.write("\n".join(remaining[1:]))

    # Cooldown
    wait_time = random.uniform(
        config["wait_min"],
        config["wait_max"]
    )

    print(
        f"Waiting {wait_time:.2f}s until next card...\n"
    )

    time.sleep(wait_time)
