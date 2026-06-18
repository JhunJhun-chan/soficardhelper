import pyautogui
import pyperclip
import keyboard
import time
import random
import re

# ------------------------
# Load sent cards
# ------------------------
try:
    with open("sent.txt", "r") as f:
        sent_codes = set(line.strip() for line in f if line.strip())
except FileNotFoundError:
    sent_codes = set()

# ------------------------
# Load remaining cards
# ------------------------
try:
    with open("remaining.txt", "r") as f:
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

        # Accept alphanumeric codes
        if re.fullmatch(r"[a-zA-Z0-9]{5,8}", token):
            codes.append(token)

    # Remove duplicates while preserving order
    codes = list(dict.fromkeys(codes))

    # Skip already sent codes
    codes = [c for c in codes if c not in sent_codes]

    with open("remaining.txt", "w") as f:
        f.write("\n".join(codes))

    remaining_codes = codes

TOTAL = len(remaining_codes)
completed = 0
paused = False

print(f"\nLoaded {TOTAL} cards.")
print("Switch to Discord channel...")
print("Starting in 10 seconds...\n")

time.sleep(10)

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

    # Read remaining cards
    with open("remaining.txt", "r") as f:
        remaining = [line.strip() for line in f if line.strip()]

    if len(remaining) == 0:
        print("\nAll cards completed!")
        break

    code = remaining[0]

    command = f"sv {code}"

        # Copy command
    pyperclip.copy(command)

    # Small thinking delay
    pre_paste_delay = random.uniform(0.8, 1.5)
    print(f"Waiting {pre_paste_delay:.2f} seconds before pasting...")
    time.sleep(pre_paste_delay)

    # Paste into chat box
    pyautogui.hotkey("ctrl", "v")

    # Pause after paste so the message sits in the box
    post_paste_delay = random.uniform(2.5, 4.0)
    print(f"Waiting {post_paste_delay:.2f} seconds before pressing Enter...")
    time.sleep(post_paste_delay)

    # Send message
    pyautogui.press("enter")

    completed += 1

    print(f"[{completed}/{TOTAL}] Sent {command}")

    # Save to sent.txt
    with open("sent.txt", "a") as f:
        f.write(code + "\n")

    # Save to log.txt
    with open("log.txt", "a") as f:
        f.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} -> {command}\n"
        )

    # Remove sent code
    with open("remaining.txt", "w") as f:
        f.write("\n".join(remaining[1:]))

    # Cooldown between cards
    wait_time = random.uniform(12.0, 13.5)

    print(
        f"Waiting {wait_time:.2f} seconds until next card..."
    )

    time.sleep(wait_time)