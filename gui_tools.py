import time

import pyautogui
import pyperclip


def _validate_coordinates(x, y):
    """Validate that coordinates are inside the screen."""
    x = int(x)
    y = int(y)

    screen_width, screen_height = pyautogui.size()

    if not (0 <= x < screen_width and 0 <= y < screen_height):
        raise ValueError(
            f"Coordinates ({x}, {y}) are outside the screen. "
            f"Screen size: {screen_width}x{screen_height}."
        )

    return x, y


def move_mouse(x, y):
    """Move the mouse to a screen coordinate."""
    try:
        x, y = _validate_coordinates(x, y)
        pyautogui.moveTo(x, y, duration=0.2)
        return f"Mouse moved to ({x}, {y})."
    except (TypeError, ValueError) as e:
        return str(e)


def click_at(x, y):
    """Click at a screen coordinate."""
    try:
        x, y = _validate_coordinates(x, y)
        pyautogui.click(x, y)
        return f"Clicked at ({x}, {y})."
    except (TypeError, ValueError) as e:
        return str(e)


def double_click_at(x, y):
    """Double-click at a screen coordinate."""
    try:
        x, y = _validate_coordinates(x, y)
        pyautogui.doubleClick(x, y, interval=0.1)
        return f"Double-clicked at ({x}, {y})."
    except (TypeError, ValueError) as e:
        return str(e)


def type_text(text):
    """Type text into the currently focused application."""
    if not isinstance(text, str):
        return "Text must be a string."

    if not text:
        return "Text cannot be empty."

    try:
        # Clipboard paste supports Unicode better than pyautogui.write().
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
        return "Text entered successfully."
    except Exception as e:
        return f"Could not enter text: {e}"


def press_key(key):
    """Press a keyboard key."""
    if not isinstance(key, str) or not key.strip():
        return "Key must be a non-empty string."

    try:
        pyautogui.press(key)
        return f"Pressed {key}."
    except Exception as e:
        return f"Could not press key: {e}"


def hotkey(*keys):
    """Press a keyboard combination."""
    if not keys:
        return "At least one key is required."

    try:
        pyautogui.hotkey(*keys)
        return f"Pressed {' + '.join(keys)}."
    except Exception as e:
        return f"Could not execute hotkey: {e}"


def scroll(amount):
    """
    Scroll the current application.

    Positive amount = scroll up.
    Negative amount = scroll down.
    """
    try:
        amount = int(amount)

        if amount == 0:
            return "Scroll amount cannot be zero."

        pyautogui.scroll(amount)

        direction = "up" if amount > 0 else "down"

        return f"Scrolled {direction} by {abs(amount)}."
    except (TypeError, ValueError) as e:
        return f"Invalid scroll amount: {e}"


def drag_to(x, y, duration=0.5):
    """
    Drag the mouse from its current position to a screen coordinate.
    """
    try:
        x, y = _validate_coordinates(x, y)
        duration = float(duration)

        if duration < 0:
            return "Duration cannot be negative."

        pyautogui.dragTo(x, y, duration=duration)

        return f"Dragged to ({x}, {y})."
    except (TypeError, ValueError) as e:
        return str(e)


def get_mouse_position():
    """Return the current mouse position."""
    try:
        x, y = pyautogui.position()
        return f"Mouse position: ({x}, {y})."
    except Exception as e:
        return f"Could not get mouse position: {e}"