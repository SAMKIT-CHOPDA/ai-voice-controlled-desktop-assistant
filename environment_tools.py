from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
VENV_PYTHON = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"


def _python_executable():
    """Return the project's virtual-environment Python executable."""
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)

    return sys.executable


def _run(command, timeout=120):
    """Run a command inside the project environment."""
    try:
        result = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        output = result.stdout.strip()

        if result.stderr.strip():
            output += "\nSTDERR:\n" + result.stderr.strip()

        if not output:
            output = "(No output)"

        return f"Exit code: {result.returncode}\n{output}"

    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds."

    except Exception as e:
        return f"Command failed: {e}"


def python_info():
    """Return information about the project's Python environment."""
    python = _python_executable()

    version = _run(
        [python, "--version"],
        timeout=30,
    )

    pip_version = _run(
        [python, "-m", "pip", "--version"],
        timeout=30,
    )

    environment = "Project .venv" if VENV_PYTHON.exists() else "Current Python environment"

    return (
        f"Environment: {environment}\n\n"
        f"Python:\n{version}\n\n"
        f"Pip:\n{pip_version}"
    )


def list_packages():
    """List installed Python packages."""
    python = _python_executable()

    return _run(
        [python, "-m", "pip", "list"],
        timeout=60,
    )


def package_info(package):
    """Show information about a specific installed package."""
    if not isinstance(package, str) or not package.strip():
        return "Package name cannot be empty."

    package = package.strip()

    python = _python_executable()

    return _run(
        [python, "-m", "pip", "show", package],
        timeout=60,
    )


def install_package(package):
    """Install a Python package into the project's environment."""
    if not isinstance(package, str) or not package.strip():
        return "Package name cannot be empty."

    package = package.strip()

    python = _python_executable()

    return _run(
        [python, "-m", "pip", "install", package],
        timeout=300,
    )


def uninstall_package(package):
    """Uninstall a Python package from the project's environment."""
    if not isinstance(package, str) or not package.strip():
        return "Package name cannot be empty."

    package = package.strip()

    python = _python_executable()

    return _run(
        [python, "-m", "pip", "uninstall", "-y", package],
        timeout=300,
    )


def upgrade_package(package):
    """Upgrade a Python package in the project's environment."""
    if not isinstance(package, str) or not package.strip():
        return "Package name cannot be empty."

    package = package.strip()

    python = _python_executable()

    return _run(
        [python, "-m", "pip", "install", "--upgrade", package],
        timeout=300,
    )


def check_package(package):
    """Check whether a Python package is installed."""
    if not isinstance(package, str) or not package.strip():
        return "Package name cannot be empty."

    package = package.strip()

    python = _python_executable()

    result = subprocess.run(
        [python, "-m", "pip", "show", package],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    if result.returncode == 0 and result.stdout.strip():
        return f"{package} is installed.\n\n{result.stdout.strip()}"

    return f"{package} is not installed."


def generate_requirements():
    """Generate requirements.txt from the project's environment."""
    python = _python_executable()
    requirements_file = PROJECT_ROOT / "requirements.txt"

    try:
        result = subprocess.run(
            [python, "-m", "pip", "freeze"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            return (
                f"Could not generate requirements.txt.\n"
                f"{result.stderr.strip()}"
            )

        requirements_file.write_text(
            result.stdout,
            encoding="utf-8",
        )

        return (
            f"requirements.txt updated successfully.\n"
            f"Packages recorded: {len(result.stdout.splitlines())}"
        )

    except Exception as e:
        return f"Could not generate requirements.txt: {e}"


def verify_requirements():
    """Check whether installed packages satisfy requirements.txt."""
    requirements_file = PROJECT_ROOT / "requirements.txt"

    if not requirements_file.exists():
        return "requirements.txt does not exist."

    python = _python_executable()

    return _run(
        [
            python,
            "-m",
            "pip",
            "check",
        ],
        timeout=120,
    )


def check_python_module(module):
    """Check whether a Python module can be imported."""
    if not isinstance(module, str) or not module.strip():
        return "Module name cannot be empty."

    module = module.strip()

    python = _python_executable()

    result = subprocess.run(
        [
            python,
            "-c",
            (
                "import importlib.util; "
                f"spec = importlib.util.find_spec({module!r}); "
                "print('Module is available.' if spec else 'Module is not available.')"
            ),
        ],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return f"Could not check module: {result.stderr.strip()}"

    return result.stdout.strip()