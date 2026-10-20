"""Code execution for Playground and Challenges.

Backends:
- ``subprocess``: run in the current Python interpreter. Local development
  only -- NOT safe for untrusted users.
- ``docker``: run in a throwaway, hardened container. Recommended for servers.

Environment:
- ``BELAJAR_LAGI_RUNNER=0`` disables execution entirely.
- ``BELAJAR_LAGI_RUNNER_BACKEND=subprocess|docker`` selects the backend.
- ``BELAJAR_LAGI_RUNNER_IMAGE`` overrides the container image.
- ``BELAJAR_LAGI_RUNNER_TIMEOUT_S`` overrides the container timeout.
"""
import os
import shutil
import subprocess
import sys
import tempfile
import time

TIMEOUT_S = 5
DOCKER_TIMEOUT_S = 20
MAX_OUTPUT = 10000
DEFAULT_DOCKER_IMAGE = "python:3.11-slim"


def _disabled() -> bool:
    value = os.environ.get("BELAJAR_LAGI_RUNNER", "1").strip().lower()
    return value in {"0", "false", "off", "no"}


def _backend() -> str:
    value = os.environ.get("BELAJAR_LAGI_RUNNER_BACKEND", "subprocess").strip().lower()
    return value or "subprocess"


def _docker_image() -> str:
    return os.environ.get("BELAJAR_LAGI_RUNNER_IMAGE", "").strip() or DEFAULT_DOCKER_IMAGE


def _docker_timeout() -> int:
    try:
        return int(os.environ.get("BELAJAR_LAGI_RUNNER_TIMEOUT_S", DOCKER_TIMEOUT_S))
    except (TypeError, ValueError):
        return DOCKER_TIMEOUT_S


def _truncate(text: str) -> str:
    if len(text) > MAX_OUTPUT:
        return text[:MAX_OUTPUT] + "\n...[output truncated]..."
    return text


def _write_script(code: str) -> tuple[str, str]:
    tmpdir = tempfile.mkdtemp(prefix="bl_")
    script_path = os.path.join(tmpdir, "__bl_runner__.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code or "")
    return tmpdir, script_path


def run_python_subprocess(code: str) -> dict:
    code = code or ""
    tmpdir, script_path = _write_script(code)
    try:
        start = time.time()
        try:
            proc = subprocess.run(
                [sys.executable, "-B", "-I", script_path],
                capture_output=True,
                text=True,
                cwd=tmpdir,
                timeout=TIMEOUT_S,
                env={"PATH": os.environ.get("PATH", ""), "HOME": tmpdir},
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {"status": "error", "error": f"Timeout (>{TIMEOUT_S}s)", "output": ""}
        except Exception as e:  # pragma: no cover
            return {"status": "error", "error": str(e), "output": ""}

        elapsed = round(time.time() - start, 3)
        outp = _truncate((proc.stdout or "") + (proc.stderr or ""))
        if proc.returncode == 0:
            return {"status": "ok", "output": outp, "time": elapsed}
        return {"status": "error", "error": outp, "time": elapsed, "returncode": proc.returncode}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _docker_available() -> bool:
    try:
        proc = subprocess.run(
            ["docker", "version", "--format", "{{.Server.Version}}"],
            capture_output=True, text=True, timeout=5, check=False,
        )
        return proc.returncode == 0
    except Exception:
        return False


def docker_command(tmpdir: str, image: str | None = None) -> list[str]:
    """Build the hardened ``docker run`` command for a temporary script dir."""
    return [
        "docker", "run", "--rm",
        "--pull=never",
        "--network", "none",
        "--memory", "128m",
        "--memory-swap", "128m",
        "--cpus", "0.5",
        "--cap-drop", "ALL",
        "--read-only",
        "--tmpfs", "/tmp:size=16m",
        "--pids-limit", "64",
        "--security-opt", "no-new-privileges",
        "--user", "1000:1000",
        "-v", f"{tmpdir}:/sandbox:ro",
        "-w", "/sandbox",
        image or _docker_image(),
        "python", "-B", "/sandbox/__bl_runner__.py",
    ]


def run_python_docker(code: str) -> dict:
    if not _docker_available():
        return {
            "status": "error",
            "error": (
                "Backend Docker diminta tapi Docker tidak tersedia. "
                "Install Docker atau set BELAJAR_LAGI_RUNNER_BACKEND=subprocess."
            ),
            "output": "",
        }

    code = code or ""
    tmpdir, script_path = _write_script(code)
    try:
        # Container runs as UID 1000, so the script must be readable by it.
        os.chmod(tmpdir, 0o755)
        os.chmod(script_path, 0o644)

        cmd = docker_command(tmpdir)
        start = time.time()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=_docker_timeout(),
                check=False,
            )
        except subprocess.TimeoutExpired:
            return {"status": "error", "error": f"Timeout (>{_docker_timeout()}s)", "output": ""}
        except Exception as e:
            return {"status": "error", "error": str(e), "output": ""}

        elapsed = round(time.time() - start, 3)
        outp = _truncate((proc.stdout or "") + (proc.stderr or ""))
        if proc.returncode == 0:
            return {"status": "ok", "output": outp, "time": elapsed}
        return {"status": "error", "error": outp, "time": elapsed, "returncode": proc.returncode}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def run_python(code: str) -> dict:
    if _disabled():
        return {
            "status": "error",
            "error": "Code runner dinonaktifkan oleh server (BELAJAR_LAGI_RUNNER=0).",
            "output": "",
        }

    backend = _backend()
    if backend == "docker":
        return run_python_docker(code)
    if backend in {"subprocess", "local"}:
        return run_python_subprocess(code)
    return {
        "status": "error",
        "error": f"Backend runner tidak dikenal: {backend}",
        "output": "",
    }
