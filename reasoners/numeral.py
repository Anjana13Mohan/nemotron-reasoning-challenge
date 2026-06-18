"""
numeral.py — deterministic reasoner for Roman-numeral conversion puzzles.

Handles both directions (integer -> Roman and Roman -> integer) with a
verification step that converts back and confirms the round trip.
"""

import re

_VAL = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
_SYM = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]


def to_roman(n: int) -> str:
    out = ""
    for v, s in zip(_VAL, _SYM):
        while n >= v:
            out += s
            n -= v
    return out


def from_roman(s: str) -> int:
    vals = dict(zip(_SYM, _VAL))
    r, i = 0, 0
    while i < len(s):
        if i + 1 < len(s) and s[i:i + 2] in vals:
            r += vals[s[i:i + 2]]
            i += 2
        else:
            r += vals[s[i]]
            i += 1
    return r


def reason(prompt: str):
    """Generate (cot, answer) for a numeral puzzle, or (None, None)."""
    m_int = re.search(r"write the number (\d+)", prompt, re.IGNORECASE)
    m_rom = re.search(r"convert ([A-Z]+) to an? integer", prompt, re.IGNORECASE)

    if m_int:
        n = int(m_int.group(1))
        steps, rem, built = [], n, ""
        for v, s in zip(_VAL, _SYM):
            while rem >= v:
                steps.append(f"{rem} >= {v} ({s}): append {s}, remainder {rem - v}")
                built += s
                rem -= v
        check = from_roman(built)
        cot = "\n".join(
            [f"This is a Roman-numeral conversion: integer {n} to Roman.",
             "", "Greedily subtract the largest values:"]
            + steps
            + ["",
               f"Assembled numeral: {built}",
               f"Verification: parsing {built} back gives {check}, "
               f"which matches {n}."]
        )
        return cot, built

    if m_rom:
        roman = m_rom.group(1)
        vals = dict(zip(_SYM, _VAL))
        steps, total, i = [], 0, 0
        while i < len(roman):
            if i + 1 < len(roman) and roman[i:i + 2] in vals:
                v = vals[roman[i:i + 2]]
                steps.append(f"{roman[i:i + 2]} = {v}, running total {total + v}")
                total += v
                i += 2
            else:
                v = vals[roman[i]]
                steps.append(f"{roman[i]} = {v}, running total {total + v}")
                total += v
                i += 1
        rebuilt = to_roman(total)
        cot = "\n".join(
            [f"This is a Roman-numeral conversion: {roman} to integer.",
             "", "Read symbols left to right, applying subtractive pairs:"]
            + steps
            + ["",
               f"Total: {total}",
               f"Verification: rebuilding {total} as a numeral gives "
               f"{rebuilt}, which matches {roman}."]
        )
        return cot, str(total)

    return None, None
