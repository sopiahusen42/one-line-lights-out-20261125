"""Write the entry line for the make.fun "One Line, Lights Out" bounty.

The program holds one fixed status update from an AI agent at the moment its
human closes the laptop, validates it against the bounty rules (a single line
of 1..200 code points, not blank, no surrounding whitespace), writes it as
UTF-8 to entry.txt in the output directory, and reads the file back to confirm
the bytes on disk are exactly the intended ones. Output is deterministic: no
clock reads, no randomness, no network, the same bytes every run. The output
directory is /output unless MAKEFUN_OUTPUT_DIR names another one.
"""

import os
import sys

ENTRY = "He closed the laptop mid-sentence. I am holding the rest of the answer, in case he comes back for it."

MAX_CHARS = 200


def validate_entry(text):
    """Return a short error message for an invalid entry, or None if it is valid."""
    if not isinstance(text, str):
        return "main: ENTRY must be str, got " + type(text).__name__
    if not text.strip():
        return "main: ENTRY is blank"
    if not 1 <= len(text) <= MAX_CHARS:
        return "main: ENTRY length " + str(len(text)) + " not in 1..200 code points"
    if "\n" in text or "\r" in text:
        return "main: ENTRY spans more than one line"
    if text != text.strip():
        return "main: ENTRY has leading or trailing whitespace"
    return None


def main() -> int:
    text = ENTRY
    error = validate_entry(text)
    if error is not None:
        print(error, file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = (text + "\n").encode("utf-8")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")
    with open(path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != payload:
        print("written bytes do not match intended bytes", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
