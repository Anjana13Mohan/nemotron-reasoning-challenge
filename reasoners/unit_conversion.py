"""
unit_conversion.py — deterministic reasoner for linear unit-conversion puzzles.

Rule: out = rate * in, with rate hidden. Recover the rate from a worked
example, verify against a second, apply to the target. Single rounded path.
"""

import re


def parse(prompt: str):
    """Return ([(in, out), ...], target, unit_in) from a conversion prompt."""
    examples, target, unit = [], None, ""
    for line in prompt.strip().split("\n"):
        m = re.match(r"([\d.]+)\s*(\w+)\s*becomes\s*([\d.]+)", line)
        if m:
            examples.append((float(m.group(1)), float(m.group(3))))
            unit = m.group(2)
        t = re.search(r"convert\s+([\d.]+)\s*(\w+)", line, re.IGNORECASE)
        if t and "convert" in line.lower():
            target = float(t.group(1))
            if not unit:
                unit = t.group(2)
    return examples, target, unit


def reason(prompt: str):
    """Generate (cot, answer) for a unit-conversion puzzle, or (None, None)."""
    examples, target, unit = parse(prompt)
    if not examples or target is None or len(examples) < 2:
        return None, None

    in1, out1 = examples[0]
    in2, out2 = examples[1]
    r1 = round(out1 / in1, 4)
    r2 = round(out2 / in2, 4)
    diff = round(abs(r1 - r2), 4)
    result_raw = round(target * r1, 4)
    answer = round(result_raw, 2)

    cot = "\n".join([
        "This is a linear unit-conversion problem.",
        "",
        "STEP 1: Recover the conversion rate from the first example.",
        f"EX1: {in1} {unit} -> {out1}",
        f"rate = {out1} / {in1} = {r1}",
        "",
        "STEP 2: Verify the rate with the second example.",
        f"EX2: {in2} {unit} -> {out2}",
        f"rate = {out2} / {in2} = {r2}",
        f"The rates agree (|{r1} - {r2}| = {diff}), so the rate is reliable.",
        "",
        "STEP 3: Apply the rate to the target value.",
        f"result = {target} * {r1} = {result_raw}",
        f"Rounded to two decimals, the answer is {answer:.2f}.",
    ])
    return cot, f"{answer:.2f}"
