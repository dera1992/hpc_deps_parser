# HPC Dependency Expression Parser (MVC)

Parses logical dependency expressions like:

- `a & b`
- `a | b | c`
- `a & (b | c)`
- `(a & b) | (c & d)`

into nested Python list structures.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -U pip pytest
