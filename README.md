# HPC Dependency Expression Parser

A small, validated parser for **HPC job dependency expressions**.  
It accepts logical dependency expressions such as:

Parses logical dependency expressions like:

- `a & b`
- `a | b | c`
- `a & (b | c)`
- `(a & b) | (c & d)`

into nested Python list structures.

## Features
*Supports logical AND (&)
*Supports logical OR (|)
*Supports parentheses for grouping
*Correct operator precedence (& binds tighter than |)
*Rejects invalid expressions with descriptive errors
*Produces a nested list AST suitable for later evaluation
*Fully unit-tested with pytest

## Project Structure
hpc-deps-parser/
├── app/
│   ├── model.py        # Tokenizer + recursive-descent parser
│   ├── controller.py  # Orchestrates model and view
│   ├── view.py        # Output formatting
│   ├── main.py        # Demo entry point
│   └── __init__.py
│
├── tests/
│   ├── test_model_tokenizer.py
│   ├── test_model_parser_valid.py
│   ├── test_model_parser_invalid.py
│   ├── test_controller.py
│   ├── test_view.py
│   ├── test_main.py
│
├── pyproject.toml
└── README.md

## Installation & Setup
1. Clone the repository
```bash
    git clone <your-repo-url>
    cd hpc-deps-parser
```
2. Create a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```
3. Install project and development dependencies
    ```bash
   pip install -e .[dev]
   ```
4. Running the Demo
    ```bash
   python -m app.main
   ```
5. Running Tests
    ```bash
    pytest
    ```
6. Running Tests with Coverage
    ```bash
    pytest --cov=app --cov-report=term-missing
    ```

## Coverage Notes
The uncovered lines in the token.py contains a small number of defensive checks that are difficult to reach through realistic input. These are intentionally left uncovered to avoid artificial tests.  
Name                Stmts   Miss  Cover
---------------------------------------
app\controller.py      13      0   100%
app\model.py          104      1    99%
app\view.py             9      0   100%
---------------------------------------
TOTAL                 126      1    99%

The following files are excluded from coverage as they do not contain meaningful business logic:
- main.py (CLI entry point)
- `__init__.py` files
#### What is Covered
- Core parsing logic (tokenization and recursive parsing)
- Valid expressions (AND, OR, nested, mixed)
- Invalid expressions (syntax errors, unmatched parentheses, trailing operators, whitespaces)

## Assumptions & Design notes
- Only logical AND (`&`) and OR (`|`) operators are supported, as specified in the problem statement.
- A Recursive Descent parser was used. This approach maps naturally to nested parenthesis, produces clear and readable code, allows precise error reporting.
- Parsing is split into two units:
    * Tokenization (lexical analysis)
    * Recursive parsing of expressions and terms.
- Input is user provided text: The system assumes expressions are provided as strings and may be invalid, invalid expressions must be detected and rejected.
- I designed the solution follows an MVC design pattern for maintaiinability and clarity.

## Extensibility

Can be extended to support:
- NOT operator (!)
- Job status conditions (success/failure)
- JSON AST output
- Scheduler integration (e.g., Slurm)