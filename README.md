# 🧠 NLP-Based Code Summarization Tool

An NLP tool that takes Python source code as input and generates a natural language summary using the **CodeT5** transformer model.

---

## 📁 Project Structure

```
code_summarizer/
│
├── main.py                  ← Entry point (run this)
├── app.py                   ← Streamlit Web UI
├── requirements.txt         ← All dependencies
│
├── input_module/
│   ├── __init__.py
│   └── code_input.py        ← Accepts code from user
│
├── ast_parser/
│   ├── __init__.py
│   ├── parser.py            ← Parses code into AST
│   └── ast_serializer.py    ← Converts AST to readable dict
│
├── summarizer/
│   ├── __init__.py
│   └── model.py             ← CodeT5 NLP model (core)
│
├── data/
│   ├── __init__.py
│   └── save_samples.py      ← Saves input/output samples
│
└── tests/
    ├── test_parser.py
    └── test_summarizer.py
```

---

## ⚙️ Setup Instructions

### Step 1 — Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Run CLI Tool
```bash
python main.py
```

### Step 4 — Run Web UI (Optional)
```bash
streamlit run app.py
```

---

## 🧠 Model Used

| Property | Value |
|---|---|
| Model | `Salesforce/codet5-base-codexglue-sum-python` |
| Type | Seq2Seq Transformer |
| Task | Code → Natural Language Summary |
| Dataset | CodeSearchNet (Python) |

---

## 🔍 How It Works

1. User inputs Python code
2. AST parser validates the syntax
3. CodeT5 tokenizes the code
4. Model generates a natural language summary
5. Summary is printed and saved to `data/samples.json`

---

## 📌 Example

**Input:**
```python
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
```

**Output:**
```
Returns the factorial of a given number using recursion.
```
