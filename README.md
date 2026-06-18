# SofiCardHelper

Python utility for Sofi card management with queueing, duplicate protection, logging, and resume support.

## Features

- Resume after restarting
- Duplicate protection
- Automatic logging
- Random delays
- Pause with F8
- Emergency stop with F9

## Installation

```bash
git clone https://github.com/JhunJhun-chan/soficardhelper.git
cd soficardhelper

pip install -r requirements.txt
python main.py
```

## Controls

| Key | Action |
|------|--------|
| F8 | Pause / Resume |
| F9 | Stop |

## Dependencies

- pyautogui
- pyperclip
- keyboard

## License

MIT
