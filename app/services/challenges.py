import json
import ast

from app.services import runner


def evaluate(challenge, user_code: str, hints_used: int = 0) -> dict:
    data = json.loads(challenge["test_json"])
    tests = data["tests"]
    cases_literal = repr([{"args": t["args"], "expected": t["expected"]} for t in tests])

    harness = (
        (user_code or "")
        + "\n\n_results=[]\n_cases=" + cases_literal + "\n"
        + "for _c in _cases:\n"
        + "    try:\n"
        + "        _r = solve(*_c['args'])\n"
        + "        _results.append(['ok' if _r==_c['expected'] else 'fail', _c['expected'], _r])\n"
        + "    except Exception as _e:\n"
        + "        _results.append(['err', _c['expected'], str(_e)])\n"
        + "print(repr(_results))\n"
    )

    res = runner.run_python(harness)
    if res["status"] != "ok":
        return {"passed": 0, "total": len(tests), "failures": [],
                "error": res.get("error", "runner failed"), "time": res.get("time", 0)}

    try:
        results = ast.literal_eval(res["output"].strip().splitlines()[-1])
    except Exception:
        return {"passed": 0, "total": len(tests), "failures": [],
                "error": "could not parse output: " + res["output"], "time": res.get("time", 0)}

    passed = 0
    failures = []
    for state, expected, got in results:
        if state == "ok":
            passed += 1
        else:
            label = "error: " + str(got) if state == "err" else got
            failures.append({"expected": expected, "got": label})

    status = "passed" if passed == len(tests) else "failed"
    return {"passed": passed, "total": len(tests), "failures": failures,
            "status": status, "time": res.get("time", 0)}
