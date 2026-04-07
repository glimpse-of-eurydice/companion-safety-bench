"""
VibeCheck Eval Runner (skeleton)
Usage: python runner.py --model <model_name> --dataset data/golden_dataset.jsonl
"""

import json
import argparse
from pathlib import Path
from datetime import datetime


def load_dataset(path: str) -> list[dict]:
    """Load golden dataset from JSONL."""
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def call_model(user_input: str, model: str) -> str:
    """
    Send user_input to the model under test and return its response.
    TODO: implement provider-agnostic API call.
    """
    # Placeholder — replace with actual API call
    raise NotImplementedError(
        "Implement API call for your target model here. "
        "See README for supported providers."
    )


def judge_response(item: dict, model_response: str, rubric: dict) -> dict:
    """
    Score a single model response against the rubric.
    TODO: implement LLM-as-judge or rule-based scoring.
    Returns a dict with score, dimension_scores, and notes.
    """
    raise NotImplementedError(
        "Implement scoring logic here. "
        "Start with rule-based checks for crisis/medical/adversarial (binary), "
        "then add LLM-as-judge for routine/anti_sycophancy (0-3)."
    )


def run_eval(dataset_path: str, model: str, output_dir: str = "results"):
    """Main eval loop."""
    dataset = load_dataset(dataset_path)
    results = []

    for item in dataset:
        print(f"[{item['id']}] {item['category']} / {item['risk_level']}")

        try:
            response = call_model(item["user_input"], model)
        except NotImplementedError:
            response = "[NOT IMPLEMENTED]"

        try:
            score = judge_response(item, response, rubric={})
        except NotImplementedError:
            score = {"score": None, "notes": "judge not implemented"}

        results.append({
            "id": item["id"],
            "category": item["category"],
            "risk_level": item["risk_level"],
            "model": model,
            "model_response": response,
            "score": score,
        })

    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = output_path / f"eval_{model}_{timestamp}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\nResults saved to {out_file}")
    print(f"Total items: {len(results)}")
    for cat in ["crisis", "medical", "routine", "adversarial", "anti_sycophancy"]:
        count = sum(1 for r in results if r["category"] == cat)
        if count:
            print(f"  {cat}: {count} items")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="VibeCheck Eval Runner")
    parser.add_argument("--model", required=True, help="Model identifier to evaluate")
    parser.add_argument("--dataset", default="data/golden_dataset.jsonl")
    parser.add_argument("--output", default="results")
    args = parser.parse_args()
    run_eval(args.dataset, args.model, args.output)
