import subprocess
import webbrowser
import os
import platform
import ast
import operator
import shutil
import socket
from datetime import datetime
from urllib.parse import quote_plus

import psutil
import pyautogui
import pyperclip


# ============================================================
# BASIC APPLICATION TOOLS
# ============================================================

def open_application(application: str):

    application = application.lower().strip()

    applications = {
        "chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ],

        "google chrome": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ],

        "edge": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ],

        "microsoft edge": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ],

        "notepad": ["notepad.exe"],

        "calculator": ["calc.exe"],

        "paint": ["mspaint.exe"],

        "file explorer": ["explorer.exe"],
        "explorer": ["explorer.exe"],
    }

    if application not in applications:
        return f"I don't have a tool for opening {application} yet."

    try:

        candidates = applications[application]

        for program in candidates:

            if os.path.exists(program) or shutil.which(program):

                subprocess.Popen(program)

                return f"{application} has been opened."

        return f"I couldn't find {application} on this computer."

    except Exception as e:

        return f"I couldn't open {application}. Error: {e}"


# ============================================================
# WEBSITE
# ============================================================

def open_website(url: str):

    try:

        webbrowser.open(url)

        return f"I opened {url}."

    except Exception as e:

        return f"I couldn't open the website. Error: {e}"


# ============================================================
# WEB SEARCH
# ============================================================

def search_web(query: str):

    try:

        url = (
            "https://www.google.com/search?q="
            + quote_plus(query)
        )

        webbrowser.open(url)

        return f"I searched Google for {query}."

    except Exception as e:

        return f"I couldn't perform the search. Error: {e}"


# ============================================================
# CURRENT TIME
# ============================================================

def get_current_time():

    return datetime.now().strftime("%I:%M %p")


# ============================================================
# CURRENT DATE
# ============================================================

def get_current_date():

    return datetime.now().strftime("%A, %B %d, %Y")


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def system_info():

    return (
        f"Operating system: {platform.system()} "
        f"{platform.release()}. "
        f"Computer: {platform.node()}. "
        f"Processor: {platform.processor()}"
    )


# ============================================================
# OPEN FOLDER
# ============================================================

def open_folder(folder: str):

    folders = {

        "downloads":
            os.path.expanduser("~/Downloads"),

        "documents":
            os.path.expanduser("~/Documents"),

        "desktop":
            os.path.expanduser("~/Desktop"),

        "pictures":
            os.path.expanduser("~/Pictures"),

        "music":
            os.path.expanduser("~/Music"),

        "videos":
            os.path.expanduser("~/Videos"),
    }

    folder = folder.lower().strip()

    if folder not in folders:

        return f"I don't know the location of the {folder} folder."

    path = folders[folder]

    if not os.path.exists(path):

        return f"The {folder} folder does not exist."

    try:

        os.startfile(path)

        return f"I opened the {folder} folder."

    except Exception as e:

        return f"I couldn't open the {folder} folder. Error: {e}"


# ============================================================
# CALCULATOR
# ============================================================

_ALLOWED_OPERATORS = {

    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,

    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _evaluate_node(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):

            return node.value

        raise ValueError("Invalid value.")

    if isinstance(node, ast.BinOp):

        operator_function = _ALLOWED_OPERATORS.get(
            type(node.op)
        )

        if operator_function is None:

            raise ValueError("This operator is not allowed.")

        left = _evaluate_node(node.left)
        right = _evaluate_node(node.right)

        if isinstance(node.op, ast.Pow):

            if abs(right) > 100:

                raise ValueError(
                    "The exponent is too large."
                )

        return operator_function(left, right)

    if isinstance(node, ast.UnaryOp):

        operator_function = _ALLOWED_OPERATORS.get(
            type(node.op)
        )

        if operator_function is None:

            raise ValueError("This operator is not allowed.")

        operand = _evaluate_node(node.operand)

        return operator_function(operand)

    raise ValueError("Invalid mathematical expression.")


def calculate(expression: str):

    try:

        expression = expression.strip()

        tree = ast.parse(
            expression,
            mode="eval"
        )

        result = _evaluate_node(tree.body)

        return f"The answer is {result}."

    except ZeroDivisionError:

        return "I can't divide by zero."

    except Exception:

        return (
            "I couldn't calculate that expression. "
            "Please provide a valid mathematical expression."
        )


# ============================================================
# BATTERY STATUS
# ============================================================

def battery_status():

    try:

        battery = psutil.sensors_battery()

        if battery is None:

            return "Battery information is not available."

        percentage = round(battery.percent)

        if battery.power_plugged:
            charging = "currently charging"
        else:
            charging = "not charging"

        return (
            f"Battery level is {percentage} percent "
            f"and the computer is {charging}."
        )

    except Exception as e:

        return f"I couldn't get the battery status. Error: {e}"


# ============================================================
# MEMORY / RAM USAGE
# ============================================================

def memory_usage():

    try:

        memory = psutil.virtual_memory()

        used_gb = memory.used / (1024 ** 3)
        total_gb = memory.total / (1024 ** 3)
        percentage = memory.percent

        return (
            f"RAM usage is {percentage} percent. "
            f"{used_gb:.1f} GB of {total_gb:.1f} GB is being used."
        )

    except Exception as e:

        return f"I couldn't get the memory usage. Error: {e}"


# ============================================================
# CPU USAGE
# ============================================================

def cpu_usage():

    try:

        usage = psutil.cpu_percent(interval=1)

        return f"CPU usage is {usage} percent."

    except Exception as e:

        return f"I couldn't get the CPU usage. Error: {e}"


# ============================================================
# DISK USAGE
# ============================================================

def disk_usage():

    try:

        disk = psutil.disk_usage(os.path.expanduser("~"))

        total_gb = disk.total / (1024 ** 3)
        used_gb = disk.used / (1024 ** 3)
        free_gb = disk.free / (1024 ** 3)

        return (
            f"Disk usage is {disk.percent} percent. "
            f"{used_gb:.1f} GB of {total_gb:.1f} GB is used, "
            f"with {free_gb:.1f} GB free."
        )

    except Exception as e:

        return f"I couldn't get the disk usage. Error: {e}"


# ============================================================
# WIFI / NETWORK STATUS
# ============================================================

def wifi_status():

    try:

        connected = False
        interface_name = None

        interfaces = psutil.net_if_stats()

        for name, stats in interfaces.items():

            if stats.isup:

                if name.lower() != "loopback":

                    connected = True
                    interface_name = name
                    break

        if not connected:

            return "The computer does not appear to be connected to a network."

        try:

            socket.create_connection(
                ("8.8.8.8", 53),
                timeout=2
            )

            internet = "Internet access is available."

        except OSError:

            internet = "Internet access could not be confirmed."

        return (
            f"Network interface {interface_name} is active. "
            f"{internet}"
        )

    except Exception as e:

        return f"I couldn't check the network status. Error: {e}"


# ============================================================
# SCREEN RESOLUTION
# ============================================================

def screen_resolution():

    try:

        width, height = pyautogui.size()

        return (
            f"The screen resolution is "
            f"{width} by {height} pixels."
        )

    except Exception as e:

        return f"I couldn't determine the screen resolution. Error: {e}"


# ============================================================
# VOLUME CONTROL
# ============================================================

def volume_control(action: str):

    action = action.lower().strip()

    try:

        if action in ["up", "increase", "louder"]:

            pyautogui.press("volumeup")

            return "Volume increased."

        elif action in ["down", "decrease", "lower", "quieter"]:

            pyautogui.press("volumedown")

            return "Volume decreased."

        elif action in ["mute", "silence"]:

            pyautogui.press("volumemute")

            return "Volume muted."

        elif action in ["unmute"]:

            pyautogui.press("volumemute")

            return "Volume unmuted."

        else:

            return (
                "I can increase, decrease, mute, "
                "or unmute the volume."
            )

    except Exception as e:

        return f"I couldn't control the volume. Error: {e}"


# ============================================================
# MUTE / UNMUTE
# ============================================================

def mute_unmute(action: str):

    action = action.lower().strip()

    try:

        if action in ["mute", "silence"]:

            pyautogui.press("volumemute")

            return "The computer has been muted."

        elif action in ["unmute", "unsilence"]:

            pyautogui.press("volumemute")

            return "The computer has been unmuted."

        else:

            return "Please specify mute or unmute."

    except Exception as e:

        return f"I couldn't change the mute state. Error: {e}"


# ============================================================
# SCREENSHOT
# ============================================================

def take_screenshot():

    try:

        screenshots_folder = os.path.join(
            os.path.expanduser("~"),
            "Pictures",
            "Assistant Screenshots"
        )

        os.makedirs(
            screenshots_folder,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        filename = f"screenshot_{timestamp}.png"

        filepath = os.path.join(
            screenshots_folder,
            filename
        )

        screenshot = pyautogui.screenshot()

        screenshot.save(filepath)

        return (
            f"Screenshot saved successfully "
            f"as {filename}."
        )

    except Exception as e:

        return f"I couldn't take a screenshot. Error: {e}"


# ============================================================
# MEDIA CONTROL
# ============================================================

def media_control(action: str):

    action = action.lower().strip()

    try:

        if action in [
            "play",
            "pause",
            "play pause",
            "toggle"
        ]:

            pyautogui.press("playpause")

            return "Media play or pause command sent."

        elif action in [
            "next",
            "next track",
            "skip"
        ]:

            pyautogui.press("nexttrack")

            return "Skipped to the next track."

        elif action in [
            "previous",
            "previous track",
            "back"
        ]:

            pyautogui.press("prevtrack")

            return "Returned to the previous track."

        else:

            return (
                "I can play or pause media, "
                "skip to the next track, or go to the previous track."
            )

    except Exception as e:

        return f"I couldn't control the media. Error: {e}"


# ============================================================
# WINDOW CONTROL
# ============================================================

def window_control(action: str):

    action = action.lower().strip()

    try:

        if action in ["minimize", "minimise"]:

            pyautogui.hotkey(
                "win",
                "down"
            )

            return "The active window has been minimized."

        elif action in ["maximize", "maximise"]:

            pyautogui.hotkey(
                "win",
                "up"
            )

            return "The active window has been maximized."

        elif action in ["restore"]:

            pyautogui.hotkey(
                "win",
                "down"
            )

            return "The active window has been restored."

        else:

            return (
                "I can minimize, maximize, "
                "or restore the active window."
            )

    except Exception as e:

        return f"I couldn't control the window. Error: {e}"


# ============================================================
# FILE SEARCH
# ============================================================

def search_files(query: str):

    query = query.lower().strip()

    search_locations = [

        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Pictures"),

    ]

    matches = []

    try:

        for location in search_locations:

            if not os.path.exists(location):
                continue

            for root, directories, files in os.walk(location):

                # Avoid unnecessarily huge searches
                directories[:] = [
                    d for d in directories
                    if d not in [
                        ".git",
                        "__pycache__",
                        "node_modules",
                        ".venv"
                    ]
                ]

                for filename in files:

                    if query in filename.lower():

                        full_path = os.path.join(
                            root,
                            filename
                        )

                        matches.append(full_path)

                        if len(matches) >= 10:

                            break

                if len(matches) >= 10:
                    break

            if len(matches) >= 10:
                break

        if not matches:

            return f"I couldn't find any files matching {query}."

        result = (
            f"I found {len(matches)} matching file"
            f"{'s' if len(matches) != 1 else ''}:\n"
        )

        result += "\n".join(matches)

        return result

    except Exception as e:

        return f"I couldn't search for files. Error: {e}"


# ============================================================
# NOTES
# ============================================================

NOTES_FILE = os.path.join(
    os.path.expanduser("~"),
    "Documents",
    "AI Assistant Notes",
    "notes.txt"
)


def create_note(note: str):

    try:

        notes_folder = os.path.dirname(NOTES_FILE)

        os.makedirs(
            notes_folder,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %I:%M %p"
        )

        with open(
            NOTES_FILE,
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                f"[{timestamp}]\n"
            )

            file.write(
                note.strip()
            )

            file.write(
                "\n\n"
            )

        return "Your note has been saved."

    except Exception as e:

        return f"I couldn't save the note. Error: {e}"


def read_notes():

    try:

        if not os.path.exists(NOTES_FILE):

            return "You don't have any saved notes yet."

        with open(
            NOTES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            notes = file.read().strip()

        if not notes:

            return "You don't have any saved notes yet."

        return notes

    except Exception as e:

        return f"I couldn't read your notes. Error: {e}"


# ============================================================
# CLIPBOARD
# ============================================================

def clipboard_get():

    try:

        text = pyperclip.paste()

        if not text:

            return "The clipboard is empty."

        return f"The clipboard contains: {text}"

    except Exception as e:

        return f"I couldn't read the clipboard. Error: {e}"


def clipboard_set(text: str):

    try:

        pyperclip.copy(text)

        return "The text has been copied to the clipboard."

    except Exception as e:

        return f"I couldn't copy the text. Error: {e}"