from transformers import RobertaTokenizer, T5ForConditionalGeneration
import re

MODEL_NAME = "Salesforce/codet5-base-multi-sum"

_tokenizer = None
_model = None


def load_model():
    global _tokenizer, _model

    if _tokenizer is None or _model is None:
        print("\n[~] Loading CodeT5 model (first run may take a minute)...")
        _tokenizer = RobertaTokenizer.from_pretrained(MODEL_NAME)
        _model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
        print("[✓] Model loaded successfully!\n")

    return _tokenizer, _model


def preprocess_code(code: str) -> str:
    """Flatten code to single line as CodeT5 expects."""
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)
    lines = [line.strip() for line in code.splitlines() if line.strip()]
    return " ".join(lines)


def generate_summary(code: str) -> str:
    tokenizer, model = load_model()

    processed_code = preprocess_code(code)

    input_ids = tokenizer(
        processed_code,
        return_tensors="pt",
        max_length=512,
        truncation=True
    ).input_ids

    # ✅ Generate summary
    generated_ids = model.generate(
        input_ids,
        max_length=30,
        min_length=5,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=2
    )

    summary = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    if not summary.strip():
        summary = "Summary could not be generated for this input."

    return summary
