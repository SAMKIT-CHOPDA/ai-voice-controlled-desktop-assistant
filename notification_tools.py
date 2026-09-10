import threading
import time

import psutil
from winotify import Notification, audio


MONITOR_INTERVAL = 60

LOW_BATTERY_THRESHOLD = 20
HIGH_CPU_THRESHOLD = 90
HIGH_MEMORY_THRESHOLD = 90


_monitor_thread = None
_monitor_running = False

_last_battery_warning = False
_last_cpu_warning = False
_last_memory_warning = False


def send_notification(title, message):
    try:
        notification = Notification(
            app_id="AI Desktop Assistant",
            title=title,
            msg=message,
        )

        notification.set_audio(
            audio.Default,
            loop=False
        )

        notification.show()

        return f"Notification sent: {title} - {message}"

    except Exception as e:
        return f"Could not send notification: {e}"


def check_battery():
    global _last_battery_warning

    battery = psutil.sensors_battery()

    if battery is None:
        return

    percent = battery.percent
    plugged = battery.power_plugged

    if percent <= LOW_BATTERY_THRESHOLD and not plugged:
        if not _last_battery_warning:
            send_notification(
                "Low Battery",
                f"Battery is at {percent}%. Consider connecting the charger."
            )

            _last_battery_warning = True

    else:
        _last_battery_warning = False


def check_cpu():
    global _last_cpu_warning

    usage = psutil.cpu_percent(interval=1)

    if usage >= HIGH_CPU_THRESHOLD:
        if not _last_cpu_warning:
            send_notification(
                "High CPU Usage",
                f"CPU usage is currently {usage:.0f}%."
            )

            _last_cpu_warning = True

    else:
        _last_cpu_warning = False


def check_memory():
    global _last_memory_warning

    memory = psutil.virtual_memory()
    usage = memory.percent

    if usage >= HIGH_MEMORY_THRESHOLD:
        if not _last_memory_warning:
            send_notification(
                "High Memory Usage",
                f"Memory usage is currently {usage:.0f}%."
            )

            _last_memory_warning = True

    else:
        _last_memory_warning = False


def _monitor_loop():
    global _monitor_running

    while _monitor_running:

        try:
            check_battery()
            check_cpu()
            check_memory()

        except Exception as e:
            print(f"Notification monitor error: {e}")

        time.sleep(MONITOR_INTERVAL)


def start_monitoring():
    global _monitor_thread
    global _monitor_running

    if _monitor_running:
        return "Context-aware notification monitoring is already running."

    _monitor_running = True

    _monitor_thread = threading.Thread(
        target=_monitor_loop,
        daemon=True
    )

    _monitor_thread.start()

    return "Context-aware notification monitoring started."


def stop_monitoring():
    global _monitor_running

    if not _monitor_running:
        return "Context-aware notification monitoring is not running."

    _monitor_running = False

    return "Context-aware notification monitoring stopped."


def monitoring_status():
    if _monitor_running:
        return "Context-aware notification monitoring is running."

    return "Context-aware notification monitoring is stopped."