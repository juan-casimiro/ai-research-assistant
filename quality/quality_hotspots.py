"""Join coverage.py JSON and Radon CC; report CRAP and decision nesting.

Usage: python quality/quality_hotspots.py coverage.json > hotspots.json
Line coverage is used in CRAP = CC**2 * (1 - coverage)**3 + CC.
Decision nesting is a deterministic structural proxy, NOT cognitive complexity.
No thresholds are implied by this report. Nested functions are reported separately;
parent coverage/nesting includes their source spans and must not be summed.
"""
import ast
import json
from pathlib import Path
import sys

from radon.complexity import cc_visit

FILES = ("main.py", "eval_golden.py", "eval_context_sufficient.py", "ingest_corpus.py",
         "compare_evals.py", "reset_collection.py", "debug_bm25.py", "show_failures.py")
DECISIONS = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.Try, ast.IfExp, ast.Match)


def nesting(node, depth=0):
    depth += isinstance(node, DECISIONS)
    return max([depth] + [nesting(child, depth) for child in ast.iter_child_nodes(node)])


def functions(blocks, prefix=""):
    for block in blocks:
        if hasattr(block, "closures"):
            name = prefix + block.name
            yield name, block
            yield from functions(block.closures, name + ".")


def main():
    coverage = json.loads(Path(sys.argv[1]).read_text())
    rows = []
    for filename in FILES:
        source = Path(filename).read_text()
        data = coverage["files"][filename]
        executed = set(data["executed_lines"])
        statements = executed | set(data["missing_lines"])
        tree = ast.parse(source)
        nodes = {n.lineno: n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for name, block in functions(cc_visit(source)):
            lines = statements & set(range(block.lineno + 1, block.endline + 1))
            fraction = len(lines & executed) / len(lines) if lines else 1.0
            cc = block.complexity
            rows.append({"file": filename, "function": name, "line": block.lineno,
                         "cyclomatic": cc, "decision_nesting": nesting(nodes[block.lineno]),
                         "covered_lines": len(lines & executed), "statements": len(lines),
                         "line_coverage": round(100 * fraction, 2),
                         "crap": round(cc ** 2 * (1 - fraction) ** 3 + cc, 2)})
    print(json.dumps(sorted(rows, key=lambda r: r["crap"], reverse=True), indent=2))


if __name__ == "__main__":
    main()
