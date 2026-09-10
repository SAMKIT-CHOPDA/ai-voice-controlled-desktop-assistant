from pathlib import Path
import subprocess


PROJECT_ROOT = Path(__file__).resolve().parent

# Files/directories that should never be modified through the developer agent.
PROTECTED_NAMES = {
    ".env",
    ".git",
    ".venv",
}

ALLOWED_TEXT_EXTENSIONS = {
    ".py",
    ".txt",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
}


def _safe_path(relative_path):
    """Resolve a project path and prevent access outside the project."""
    path = (PROJECT_ROOT / relative_path).resolve()

    try:
        path.relative_to(PROJECT_ROOT)
    except ValueError:
        raise ValueError("Path must remain inside the AI assistant project.")

    parts = path.relative_to(PROJECT_ROOT).parts

    if any(part in PROTECTED_NAMES for part in parts):
        raise ValueError("Access to protected project files/directories is not allowed.")

    return path


def list_project_files():
    try:
        excluded_dirs = {
            ".git",
            ".venv",
            "__pycache__",
            ".pytest_cache",
            "Assistant Screenshots",
        }

        excluded_extensions = {
            ".pyc",
            ".wav",
            ".mp3",
        }

        files = []

        for path in PROJECT_ROOT.rglob("*"):
            if not path.is_file():
                continue

            relative = path.relative_to(PROJECT_ROOT)

            if any(part in excluded_dirs for part in relative.parts):
                continue

            if path.suffix.lower() in excluded_extensions:
                continue

            files.append(str(relative))

        files.sort()

        if not files:
            return "No project files found."

        return (
            f"Project contains {len(files)} relevant files:\n"
            + "\n".join(files)
        )

    except Exception as e:
        return f"Could not list project files: {e}"



def read_project_file(path):
    """Read a text file from the project."""
    try:
        file_path = _safe_path(path)

        if not file_path.exists():
            return f"File not found: {path}"

        if not file_path.is_file():
            return f"Not a file: {path}"

        if file_path.suffix.lower() not in ALLOWED_TEXT_EXTENSIONS:
            return f"Unsupported text file type: {file_path.suffix}"

        content = file_path.read_text(encoding="utf-8")

        return content

    except UnicodeDecodeError:
        return "The file could not be decoded as UTF-8."

    except Exception as e:
        return f"Could not read file: {e}"


def search_project(query):
    """Search project text files for a string."""
    if not isinstance(query, str) or not query.strip():
        return "Search query cannot be empty."

    query = query.lower()
    results = []

    try:
        for path in PROJECT_ROOT.rglob("*"):
            if not path.is_file():
                continue

            relative = path.relative_to(PROJECT_ROOT)

            if any(part in PROTECTED_NAMES for part in relative.parts):
                continue

            if path.suffix.lower() not in ALLOWED_TEXT_EXTENSIONS:
                continue

            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            for line_number, line in enumerate(text.splitlines(), start=1):
                if query in line.lower():
                    results.append(
                        f"{relative}:{line_number}: {line.strip()}"
                    )

                    if len(results) >= 100:
                        return "\n".join(results)

        if not results:
            return f"No matches found for: {query}"

        return "\n".join(results)

    except Exception as e:
        return f"Project search failed: {e}"


def write_project_file(path, content):
    """Create or replace a project text file."""
    try:
        file_path = _safe_path(path)

        if file_path.suffix.lower() not in ALLOWED_TEXT_EXTENSIONS:
            return f"Unsupported text file type: {file_path.suffix}"

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")

        return f"File written successfully: {path}"

    except Exception as e:
        return f"Could not write file: {e}"


def run_python_file(path):
    """Run a Python file inside the project virtual environment."""
    try:
        file_path = _safe_path(path)

        if not file_path.exists():
            return f"File not found: {path}"

        if file_path.suffix.lower() != ".py":
            return "This tool can only run Python files."

        python_executable = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"

        if not python_executable.exists():
            python_executable = "python"

        result = subprocess.run(
            [str(python_executable), str(file_path)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )

        output = result.stdout

        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr

        if not output.strip():
            output = "(No output)"

        return (
            f"Exit code: {result.returncode}\n"
            f"{output}"
        )

    except subprocess.TimeoutExpired:
        return "Python execution timed out after 120 seconds."

    except Exception as e:
        return f"Could not run Python file: {e}"


def run_python_command(command):
    """Run a Python -c command inside the project environment."""
    if not isinstance(command, str) or not command.strip():
        return "Python command cannot be empty."

    try:
        python_executable = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"

        if not python_executable.exists():
            python_executable = "python"

        result = subprocess.run(
            [str(python_executable), "-c", command],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )

        output = result.stdout

        if result.stderr:
            output += "\nSTDERR:\n" + result.stderr

        if not output.strip():
            output = "(No output)"

        return (
            f"Exit code: {result.returncode}\n"
            f"{output}"
        )

    except subprocess.TimeoutExpired:
        return "Python command timed out after 120 seconds."

    except Exception as e:
        return f"Could not execute Python command: {e}"


def git_status():
    """Return the current Git status."""
    try:
        result = subprocess.run(
            ["git", "status", "--short"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = result.stdout.strip()

        if not output:
            return "Git working tree is clean."

        return output

    except Exception as e:
        return f"Could not get Git status: {e}"


def git_diff():
    """Return the current unstaged Git diff."""
    try:
        result = subprocess.run(
            ["git", "diff", "--"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0:
            return result.stderr

        return result.stdout if result.stdout.strip() else "No unstaged changes."

    except Exception as e:
        return f"Could not get Git diff: {e}"