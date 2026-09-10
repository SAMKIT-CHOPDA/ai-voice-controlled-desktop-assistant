import subprocess
import psutil


def list_processes(limit=20):
    """List the most resource-intensive running processes."""
    try:
        limit = int(limit)

        if limit < 1:
            return "Limit must be at least 1."

        processes = []

        for process in psutil.process_iter(
            ["pid", "name", "cpu_percent", "memory_percent"]
        ):
            try:
                info = process.info

                processes.append(
                    (
                        info["pid"],
                        info["name"] or "Unknown",
                        info["cpu_percent"] or 0,
                        info["memory_percent"] or 0,
                    )
                )

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        processes.sort(
            key=lambda item: item[2] + item[3],
            reverse=True,
        )

        lines = ["PID | Process | CPU % | Memory %"]

        for pid, name, cpu, memory in processes[:limit]:
            lines.append(
                f"{pid} | {name} | {cpu:.1f}% | {memory:.1f}%"
            )

        return "\n".join(lines)

    except (TypeError, ValueError):
        return "Limit must be a valid number."

    except Exception as e:
        return f"Could not list processes: {e}"


def find_process(name):
    """Find running processes by name."""
    if not isinstance(name, str) or not name.strip():
        return "Process name cannot be empty."

    name = name.strip().lower()
    matches = []

    try:
        for process in psutil.process_iter(
            ["pid", "name", "cpu_percent", "memory_percent"]
        ):
            try:
                info = process.info
                process_name = info["name"] or ""

                if name in process_name.lower():
                    matches.append(
                        f"PID: {info['pid']} | "
                        f"Name: {process_name} | "
                        f"CPU: {info['cpu_percent']:.1f}% | "
                        f"Memory: {info['memory_percent']:.1f}%"
                    )

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not matches:
            return f"No running process found matching '{name}'."

        return "\n".join(matches)

    except Exception as e:
        return f"Could not search processes: {e}"


def process_details(pid):
    """Get detailed information about a process."""
    try:
        pid = int(pid)
        process = psutil.Process(pid)

        with process.oneshot():
            name = process.name()
            status = process.status()
            cpu = process.cpu_percent(interval=0.1)
            memory = process.memory_percent()
            create_time = process.create_time()

        return (
            f"PID: {pid}\n"
            f"Name: {name}\n"
            f"Status: {status}\n"
            f"CPU: {cpu:.1f}%\n"
            f"Memory: {memory:.1f}%\n"
            f"Created: {create_time}"
        )

    except ValueError:
        return "PID must be a valid number."

    except psutil.NoSuchProcess:
        return f"No process found with PID {pid}."

    except psutil.AccessDenied:
        return f"Access denied for process {pid}."

    except Exception as e:
        return f"Could not get process details: {e}"


def close_process(name):
    """
    Close processes matching a name.

    This should only be called after the user explicitly
    asks the assistant to close the application/process.
    """
    if not isinstance(name, str) or not name.strip():
        return "Process name cannot be empty."

    name = name.strip().lower()
    closed = []
    failed = []

    try:
        for process in psutil.process_iter(["pid", "name"]):
            try:
                process_name = process.info["name"] or ""

                if name in process_name.lower():
                    pid = process.info["pid"]

                    try:
                        process.terminate()
                        closed.append(
                            f"{process_name} (PID {pid})"
                        )
                    except psutil.AccessDenied:
                        failed.append(
                            f"{process_name} (PID {pid}): access denied"
                        )

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not closed and not failed:
            return f"No running process found matching '{name}'."

        result = []

        if closed:
            result.append(
                "Termination requested for:\n"
                + "\n".join(closed)
            )

        if failed:
            result.append(
                "Could not close:\n"
                + "\n".join(failed)
            )

        return "\n\n".join(result)

    except Exception as e:
        return f"Could not close process: {e}"


def restart_process(name):
    """
    Restart a Windows application by terminating matching
    processes and launching the application by name.

    Only use when explicitly requested.
    """
    if not isinstance(name, str) or not name.strip():
        return "Application name cannot be empty."

    name = name.strip()

    try:
        lower_name = name.lower()
        executable = None
        terminated = []

        for process in psutil.process_iter(["pid", "name", "exe"]):
            try:
                process_name = process.info["name"] or ""

                if lower_name in process_name.lower():
                    if executable is None:
                        executable = process.info["exe"]

                    process.terminate()
                    terminated.append(process.info["pid"])

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if not executable:
            return f"Could not find running application '{name}'."

        subprocess.Popen([executable])

        return (
            f"Restarted {name}. "
            f"Previous process IDs: {terminated}"
        )

    except Exception as e:
        return f"Could not restart {name}: {e}"


def top_cpu_processes(limit=10):
    """Return processes using the most CPU."""
    try:
        limit = int(limit)

        if limit < 1:
            return "Limit must be at least 1."

        processes = []

        for process in psutil.process_iter(
            ["pid", "name", "cpu_percent"]
        ):
            try:
                info = process.info

                processes.append(
                    (
                        info["pid"],
                        info["name"] or "Unknown",
                        info["cpu_percent"] or 0,
                    )
                )

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        processes.sort(
            key=lambda item: item[2],
            reverse=True,
        )

        lines = ["PID | Process | CPU %"]

        for pid, name, cpu in processes[:limit]:
            lines.append(
                f"{pid} | {name} | {cpu:.1f}%"
            )

        return "\n".join(lines)

    except (TypeError, ValueError):
        return "Limit must be a valid number."

    except Exception as e:
        return f"Could not determine CPU usage: {e}"


def top_memory_processes(limit=10):
    """Return processes using the most memory."""
    try:
        limit = int(limit)

        if limit < 1:
            return "Limit must be at least 1."

        processes = []

        for process in psutil.process_iter(
            ["pid", "name", "memory_percent"]
        ):
            try:
                info = process.info

                processes.append(
                    (
                        info["pid"],
                        info["name"] or "Unknown",
                        info["memory_percent"] or 0,
                    )
                )

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        processes.sort(
            key=lambda item: item[2],
            reverse=True,
        )

        lines = ["PID | Process | Memory %"]

        for pid, name, memory in processes[:limit]:
            lines.append(
                f"{pid} | {name} | {memory:.1f}%"
            )

        return "\n".join(lines)

    except (TypeError, ValueError):
        return "Limit must be a valid number."

    except Exception as e:
        return f"Could not determine memory usage: {e}"