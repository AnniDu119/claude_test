"""Parse the 1800-word vocabulary text file into a JS-loadable words.js file."""
import json
import re
from pathlib import Path

SRC = Path(r"C:\Users\annir\Downloads\1800words11+.txt")
OUT = Path(__file__).parent / "words.js"

word_line = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")
page_line = re.compile(r"^Page\s+\d+\s*[·•]\s*", re.IGNORECASE)
example_line = re.compile(r"^\s*Example:\s*(.+?)\s*$", re.IGNORECASE)

raw = SRC.read_text(encoding="utf-8", errors="replace").splitlines()
# Strip page-banner lines that interrupt entries.
lines = [ln for ln in raw if not page_line.match(ln.strip())]

entries = []
i = 0
while i < len(lines):
    m = word_line.match(lines[i])
    if not m:
        i += 1
        continue
    word = m.group(2).strip()
    definition = ""
    example = ""
    # Collect lines until next numbered word, capturing definition + example
    j = i + 1
    def_parts = []
    while j < len(lines) and not word_line.match(lines[j]):
        ln = lines[j].strip()
        if not ln:
            j += 1
            continue
        ex_m = example_line.match(ln)
        if ex_m:
            example = ex_m.group(1).strip()
        else:
            def_parts.append(ln)
        j += 1
    definition = " ".join(def_parts).strip()
    if word and definition:
        entries.append({"word": word, "def": definition, "ex": example})
    i = j

print(f"Parsed {len(entries)} entries")
# Sanity: show a few
for e in entries[:3] + entries[-3:]:
    print(e)

OUT.write_text(
    "const VOCAB = " + json.dumps(entries, ensure_ascii=False) + ";\n",
    encoding="utf-8",
)
print(f"Wrote {OUT}")
