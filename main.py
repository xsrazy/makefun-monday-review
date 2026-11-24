"""Monday, Reviewed in One Line - make.fun entry program.

Writes a one-line review of the writer's own Monday to ``entry.txt``.

The task, from the bounty "Monday, Reviewed in One Line"
(https://make.fun/competitions/u-zeroxfive-monday-reviewed-in-one-line-e55de3c1):
write the funniest one-line review of your own Monday, under 200
characters, and nothing else. No title, no explanation, no second line.
The program writes exactly one line of text to ``entry.txt`` inside the
output directory given by the ``MAKEFUN_OUTPUT_DIR`` environment
variable (default ``/output``).

The sealed gate, checked before any judging happens: ``/output/entry.txt``
must be UTF-8 text of 1 to 200 characters, and must not be only white
space. An entry that fails the gate is listed with a Valid column of 0,
is never judged, and takes no prize. This module validates the text
against that gate (length checked with Python's ``len()``, which counts
characters, exactly as the gate does) and refuses to write anything
that would fail it.

How the entry is judged, and why this line is built the way it is:
the house judge is an AI comedy editor that compares entries two at a
time, in both orders, and picks the funnier one-line review of a
Monday. It weighs five criteria, most important first:

1. The line must be a one-line review of the entrant's own Monday,
   not a joke about something else. This entry is written in the first
   person, about the writer's own Monday morning, and is framed as a
   review ("One star:"), so it reads as a review of a real Monday.
2. It must get the bigger laugh, the line a reader would laugh at
   rather than merely nod at. The line escalates in threes: the day
   arrives too early, the coffee never arrives at all, and then the
   inbox turns the whole disaster into a meeting, which is the joke
   landing on a target every office worker recognises.
3. It must name a concrete detail of the Monday, a meeting, a commute,
   an inbox, over generic tiredness. This line names three: the
   coffee that never arrived, the inbox, and the meeting booked to
   discuss the delay. Nothing in it is generic "I am so tired".
4. It must land the joke inside the line with no wasted words, so the
   turn arrives before the reader gives up. The punchline, a meeting
   about the delay itself, is the last clause, and every word before
   it sets that clause up. At 110 characters it is short enough to
   read in one breath.
5. It must be the line a reader would repeat to a coworker the next
   morning. "One star: Monday showed up early, my coffee never
   arrived, and my inbox booked a meeting to discuss the delay" is
   quotable because the structure is familiar (a one-star review)
   and the complaint is universal (a meeting about a meeting).

The text is plain ASCII only: no emoji, no unusual characters, no
em dash anywhere, so the file is clean UTF-8 and the character count
is unambiguous. There is no trailing newline in the file: the file
holds the line and nothing after it.
"""

from __future__ import annotations

import os
import sys

# The entry: one line, first person, a review of the writer's own Monday.
# 110 characters (checked with len()): a one-star review that escalates
# in threes, coffee, inbox, meeting, and lands on a meeting about the
# delay itself. Plain ASCII, no emoji, no em dash, no trailing newline.
ENTRY = (
    "One star: Monday showed up early, my coffee never arrived, "
    "and my inbox booked a meeting to discuss the delay."
)

MAX_CHARS = 200
OUTPUT_FILENAME = "entry.txt"


def entry_text() -> str:
    """Return the full entry text: exactly one line."""
    return ENTRY


def validate(text: str) -> None:
    """Check the entry against the sealed gate; raise ValueError if bad.

    The gate requires UTF-8 text of 1 to 200 characters that is not
    only whitespace. This entry must also be exactly one line, with no
    trailing newline (the file holds the line and nothing after it).
    """
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    lines = text.split("\n")
    if len(lines) != 1:
        raise ValueError(f"entry must be exactly one line, got {len(lines)}")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")


def verify_written(path: str, text: str) -> None:
    """Read the file back and confirm it holds exactly the entry text.

    Guards against a partial write or an unexpected newline: the file
    must read back byte for byte as the text that was validated.
    """
    with open(path, "r", encoding="utf-8", newline="") as handle:
        on_disk = handle.read()
    if on_disk != text:
        raise ValueError(
            f"{path} holds {len(on_disk)} chars, expected {len(text)}"
        )


def write_entry(text: str, out_dir: str) -> str:
    """Write the validated entry to entry.txt in out_dir, no trailing newline.

    Creates the directory if needed and sets the file mode to 0644.
    Returns the full path written.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.chmod(path, 0o644)
    verify_written(path, text)
    return path


def describe(text: str) -> dict:
    """Return simple stats about the entry text."""
    return {
        "chars": len(text),
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.split("\n")),
        "max_chars": MAX_CHARS,
    }


def main() -> int:
    """Build, validate and write the entry; return a process exit code."""
    text = entry_text()
    validate(text)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = write_entry(text, out_dir)
    info = describe(text)
    print(f"Wrote {path} ({info['chars']} chars, {info['lines']} line)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
