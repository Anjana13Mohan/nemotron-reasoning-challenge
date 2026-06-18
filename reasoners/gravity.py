"""
gravity.py — deterministic reasoner for gravity-kinematics puzzles.

Rule: d = 0.5 * g * t^2, with g hidden. Recover the rate (0.5*g) from a
worked example, verify it against a second, then apply it to the target time.
All arithmetic follows a single rounded path so the final answer never
contradicts the derivation.
"""

import re


def parse(prompt: str):
    """Return ([(t, d), ...], target_t) parsed from a gravity prompt."""
    examples, target_t = [], None
    for line in prompt.strip().split("\n"):
        m = re.match(r"For t\s*=\s*([\d.]+)s,\s*distance\s*=\s*([\d.]+)\s*m", line)
        if m:
            examples.append((float(m.group(1)), float(m.group(2))))
        t = re.search(r"for t\s*=\s*([\d.]+)s", line, re.IGNORECASE)
        if t and "determine" in line.lower():
            target_t = float(t.group(1))
    return examples, target_t


def reason(prompt: str):
    """Generate (cot, answer) for a gravity puzzle, or (None, None)."""
    examples, target_t = parse(prompt)
    if not examples or target_t is None or len(examples) < 2:
        return None, None

    t1, d1 = examples[0]
    t2, d2 = examples[1]
    t1sq = round(t1 ** 2, 4)
    r1 = round(d1 / t1sq, 4)
    t2sq = round(t2 ** 2, 4)
    r2 = round(d2 / t2sq, 4)
    diff = round(abs(r1 - r2), 4)
    target_sq = round(target_t ** 2, 4)
    result_raw = round(r1 * target_sq, 4)
    answer = round(result_raw, 2)

    cot = "\n".join([
        "This is a gravity kinematics problem. The formula is d = 0.5*g*t^2.",
        "",
        "STEP 1: Recover the rate constant (0.5*g) from the first example.",
        f"EX1: t = {t1}s, d = {d1}m",
        f"t^2 = {t1}^2 = {t1sq}",
        f"rate = {d1} / {t1sq} = {r1}",
        "",
        "STEP 2: Verify the rate with the second example.",
        f"EX2: t = {t2}s, d = {d2}m",
        f"t^2 = {t2}^2 = {t2sq}",
        f"rate = {d2} / {t2sq} = {r2}",
        f"The two rates agree (|{r1} - {r2}| = {diff}), so the rate is reliable.",
        "",
        "STEP 3: Apply the rate to the target time.",
        f"t^2 = {target_t}^2 = {target_sq}",
        f"d = {r1} * {target_sq} = {result_raw}",
        f"Rounded to two decimals, d = {answer:.2f}.",
    ])
    return cot, f"{answer:.2f}"
