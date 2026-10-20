import subprocess
import sys
import tempfile
import os
import shutil
import time

TIMEOUT_S = 5
MAX_OUTPUT = 10000


def _disabled() -> bool:
    value = os.environ.get("BELAJAR_LAGI_RUNNER", "1").strip().lower()
    return value in {"0", "false", "off", "no"}


def run_python(code: str) -> dict:
    if _disabled():
        return {
            "status": "error",
            "error": "Code runner dinonaktifkan oleh server (BELAJAR_LAGI_RUNNER=0).",
            "output": "",
        }
    code = code or ""

    # ponytail: best-effort sandbox on localhost via -I (isolated) + -B (no
    # bytecode writes) + temp cwd + timeout + no shell. Not bulletproof against
    # a malicious local user; upgrade to Docker later (Level 17).
    tmpdir = tempfile.mkdtemp(prefix="bl_")
    script_path = os.path.join(tmpdir, "__bl_runner__.py")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)

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
        outp = (proc.stdout or "") + (proc.stderr or "")
        if len(outp) > MAX_OUTPUT:
            outp = outp[:MAX_OUTPUT] + "\n...[output truncated]..."

        if proc.returncode == 0:
            return {"status": "ok", "output": outp, "time": elapsed}
        return {"status": "error", "error": outp, "time": elapsed, "returncode": proc.returncode}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
