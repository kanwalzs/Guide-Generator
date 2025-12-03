import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pytest


INPUT_FILES = [
    "aisql",
    "data-quality-monitor",
    "internal-marketplace",
    "semantic-view",
    "sensitive-data",
]


def test_generate_templates_from_form_inputs():
    """
    Invoke `make generate <name>` for the five predefined inputs in parallel
    to speed up the integration test. Further validation and log inspection
    will be added in a subsequent step.
    """
    # Ensure sf CLI exists; otherwise skip to avoid false negatives in CI.
    if shutil.which("sf") is None:
        pytest.skip("sf CLI not found; skipping generation integration test.")

    repo_root = Path(__file__).resolve().parents[1]
    missing = [
        name for name in INPUT_FILES
        if not (repo_root / "new-template-form-inputs" / f"{name}.md").exists()
    ]
    if missing:
        pytest.skip(f"Missing input files: {', '.join(missing)}")

    def run_one(name: str):
        env = os.environ.copy()
        try:
            completed = subprocess.run(
                ["make", "generate", name],
                cwd=str(repo_root),
                text=True,
                capture_output=True,
                timeout=900,
                env=env,
            )
            return name, completed.returncode, completed.stdout, completed.stderr
        except subprocess.TimeoutExpired as e:
            return name, 124, "", f"Timeout: {e}"

    results = []
    with ThreadPoolExecutor(max_workers=len(INPUT_FILES)) as executor:
        futures = {executor.submit(run_one, name): name for name in INPUT_FILES}
        for fut in as_completed(futures):
            name, code, out, err = fut.result()
            results.append((name, code, out, err))
            # Print a concise per-file result as each future completes
            out_file = repo_root / "generated-templates" / name / "claude-output.json"
            print("")
            print(f"[generate:{name}] exit={code} output={'exists' if out_file.exists() else 'missing'} path={out_file}", out, err)

    failures = [r for r in results if r[1] != 0]
    assert not failures, "\n\n".join(
        [
            f"Generation failed for {name}:\nSTDOUT:\n{out}\nSTDERR:\n{err}"
            for name, code, out, err in failures
        ]
    )


