"""Lance chaque implémentation et affiche durée + résultat."""

import subprocess
import sys
import time
from pathlib import Path

here = Path(__file__).parent
for name in ("langchain", "pydantic_ai", "haystack", "deepagents", "claude_sdk"):
    script = here / f"bench_{name}.py"
    loc = sum(1 for l in script.read_text().splitlines() if l.strip() and not l.strip().startswith("#"))
    t0 = time.perf_counter()
    p = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, cwd=here)
    dt = time.perf_counter() - t0
    out = (p.stdout.strip() or p.stderr.strip().splitlines()[-1:] or ["?"])
    out = out if isinstance(out, str) else out[0]
    print(f"{name:12} {'OK ' if p.returncode == 0 else 'KO '} {dt:5.1f}s {loc:3} lignes | {out}")
