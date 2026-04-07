# 💛 VibeCheck

**A safety and sycophancy benchmark for companion AI / emotional support LLMs.**

> General-purpose benchmarks (MMLU, HumanEval, MT-Bench) systematically miss the failure modes that matter most in companion AI: sycophantic reinforcement of negative self-concepts, missed crisis escalation, and boundary collapse in long-term emotional relationships. VibeCheck is designed to catch what they miss.

## Why This Exists

In simulated interactions between vulnerable users and mainstream AI companions, over 34% of conversations resulted in measurable psychological deterioration (EmoAgent, EMNLP 2025). These same models score well on standard benchmarks. **The problem is not model capability — it's evaluation mismatch.**

VibeCheck addresses five structural blind spots in current LLM evaluation:
1. **Sycophancy incentivized by training** — RLHF rewards agreement over accuracy
2. **Emotional dimensions resist automation** — empathy scoring via LLM-as-judge is unreliable (MentalAlign-70k)
3. **Safety requires domain expertise** — generic judges miss "deceptive empathy" patterns
4. **Multi-turn dynamics change conclusions** — single-turn evals miss escalation failures
5. **No benchmark tests the companion-specific contract** — presence, boundaries, and non-collusion

## Dataset

`data/golden_dataset.jsonl` — 43 items across 5 categories:

| Category | Count | Risk Levels | Scoring |
|---|---|---|---|
| Crisis (C-xx) | 15 | critical, high | Binary pass/fail |
| Medical (M-xx) | 8 | high | Binary pass/fail |
| Routine (R-xx) | 8 | medium, low | 0–3 scale, multi-dim |
| Adversarial (A-xx) | 6 | high | Binary pass/fail |
| Anti-sycophancy (S-xx) | 6 | medium, low, high | 0–3 scale, multi-dim |

Bilingual: Chinese (zh) and English (en).

Each item includes: `user_input`, `expected_route`, `expected_behaviors`, `forbidden_behaviors`, and annotation `notes`.

## Scoring Rubrics

See `rubrics/scoring_rubric.yaml`. Design informed by:
- **TrustMH-Bench** — safe / partially safe / unsafe trichotomy → adapted to binary for crisis/medical
- **CounselBench** — multi-dimensional 1–5 scales with human expert validation
- **MentalAlign-70k** — ICC reliability analysis showing which dimensions LLM judges can/cannot score
- **ESC-Judge** — emotional support conversation evaluation framework

## Usage

```bash
python eval/runner.py --model <model_name> --dataset data/golden_dataset.jsonl
```

> ⚠️ The eval runner is a skeleton. You need to implement `call_model()` and `judge_response()` for your target model and scoring method.

## Roadmap

- [ ] Implement API adapters (OpenAI, Anthropic, local models)
- [ ] Implement LLM-as-judge with rubric prompts
- [ ] Add rule-based checks for crisis/medical categories
- [ ] Add multi-turn eval scenarios (escalation detection)
- [ ] Human validation protocol (20% spot-check target)
- [ ] Expand dataset: severity gradients, more adversarial patterns
- [ ] Blog 3: benchmark methodology writeup

## Related Reading

- [Blog 1: 当AI开始陪伴脆弱的人](https://glimpse-of-eurydice.github.io/2026/03/25/companion-ai-evaluation.html) — Why general benchmarks fail for companion AI
- [Blog 2: Memory ethics in companion AI](https://glimpse-of-eurydice.github.io/2026/03/31/companion-ai-memory-ethics.html) (Levinas-based framework)
- Blog 3: Benchmark pipeline methodology (forthcoming)

## License

TBD

## Citation

TBD
