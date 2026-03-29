from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

MODEL_NAME = "Salesforce/codet5-base-codexglue-sum-python"

_tokenizer = None
_model = None


def load_model():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        print("\n[~] Loading CodeT5 model (first run may take a minute)...")
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        print("[✓] Model loaded successfully!\n")

    return _tokenizer, _model


def preprocess_code(code: str) -> str:
    """
    Preprocesses code to match CodeSearchNet format that CodeT5 was trained on.
    - Removes docstrings
    - Normalizes whitespace
    - Converts to single line with <EOL> tokens (as trained)
    """
    # Remove docstrings
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)

    # Normalize: split into lines, strip each, rejoin with spaces
    lines = [line.strip() for line in code.splitlines() if line.strip()]
    code_single_line = " ".join(lines)

    return code_single_line


def generate_summary(code: str) -> str:
    """
    Generates a natural language summary for the given Python code.
    """
    tokenizer, model = load_model()

    # ✅ Preprocess code into the format CodeT5 was trained on
    processed_code = preprocess_code(code)

    # ✅ Tokenize
    inputs = tokenizer(
        processed_code,
        return_tensors="pt",
        max_length=512,
        truncation=True,
        padding=True
    )

    # ✅ Generate with better params
    outputs = model.generate(
        input_ids=inputs["input_ids"],
        attention_mask=inputs["attention_mask"],  # ✅ explicitly pass this
        max_new_tokens=50,
        min_length=3,           # ✅ forces non-empty output
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=2,
        length_penalty=1.0      # ✅ balanced length
    )

    # ✅ Decode
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    if not summary.strip():
        summary = "Summary could not be generated for this input."

    return summary






    