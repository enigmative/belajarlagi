from app.services import runner


def test_backend_default_is_subprocess(monkeypatch):
    monkeypatch.delenv("BELAJAR_LAGI_RUNNER_BACKEND", raising=False)
    assert runner._backend() == "subprocess"


def test_subprocess_backend_runs(monkeypatch):
    monkeypatch.setenv("BELAJAR_LAGI_RUNNER", "1")
    monkeypatch.setenv("BELAJAR_LAGI_RUNNER_BACKEND", "subprocess")
    res = runner.run_python("print('hello')")
    assert res["status"] == "ok"
    assert "hello" in res["output"]


def test_subprocess_backend_reports_error(monkeypatch):
    monkeypatch.setenv("BELAJAR_LAGI_RUNNER", "1")
    monkeypatch.setenv("BELAJAR_LAGI_RUNNER_BACKEND", "subprocess")
    res = runner.run_python("print(undefined_name)")
    assert res["status"] == "error"


def test_docker_backend_requires_docker(monkeypatch):
    monkeypatch.setenv("BELAJAR_LAGI_RUNNER", "1")
    monkeypatch.setenv("BELAJAR_LAGI_RUNNER_BACKEND", "docker")
    monkeypatch.setattr(runner, "_docker_available", lambda: False)
    res = runner.run_python("print(1)")
    assert res["status"] == "error"
    assert "Docker" in res["error"]


def test_docker_command_is_hardened():
    cmd = runner.docker_command("/tmp/bl_xyz")
    assert cmd[0] == "docker" and "run" in cmd

    def value_after(flag: str) -> str:
        return cmd[cmd.index(flag) + 1]

    assert value_after("--network") == "none"
    assert value_after("--cap-drop") == "ALL"
    assert "--read-only" in cmd
    assert value_after("--security-opt") == "no-new-privileges"
    assert "--memory" in cmd and "--cpus" in cmd
    assert "--pids-limit" in cmd
    assert "--pull=never" in cmd
    assert value_after("--user") == "1000:1000"
    assert value_after("-v") == "/tmp/bl_xyz:/sandbox:ro"


def test_unknown_backend_errors(monkeypatch):
    monkeypatch.setenv("BELAJAR_LAGI_RUNNER_BACKEND", "nonsense")
    res = runner.run_python("print(1)")
    assert res["status"] == "error"
    assert "tidak dikenal" in res["error"]
