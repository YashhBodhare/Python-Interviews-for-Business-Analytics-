# 🧪 Python practice companion

[← Study hub](../README.md) · [Cheat sheet](../CHEAT_SHEET.md)

## Run the interview examples

Use Python **3.11 or later** for this pack; TaskGroup, timeout and ExceptionGroup examples require 3.11+. The examples were checked on Python **3.12.14**.

From the repository root:

```bash
python3 practice/verify_examples.py
```

This runs all 50 examples as separate scripts. Each uses assertions to show the expected result. The process-pool example starts two short-lived worker processes; the examples make no network calls and do not modify your source files. Run from a local terminal rather than pasting the process-pool example into a notebook.

You can run one example directly:

```bash
python3 practice/examples/q03.py
```

A successful individual example usually prints nothing; an assertion failure indicates an unexpected result. Typing examples demonstrate runtime behaviour, not a completed static type-checker run. Free-threaded examples inspect configuration only; they do not benchmark a free-threaded interpreter.

## Business-analysis lab

With pandas installed:

```bash
python3 practice/business_lab.py
```

The code embeds a small fictional dataset, so no external files or downloads are needed. It was checked with pandas **2.2.3**. Install a pandas version supported by your Python environment if needed; exact production dependencies should be chosen for your own project.

| Business check | Expected result |
|---|---|
| Paid revenue and AOV | 3,700 INR; 5 orders; AOV 740 INR; zero-value paid order included |
| Customer enrichment | Same five paid-order rows and same revenue |
| City summary | Mumbai 1,500; Thane 2,200 |
| Complete customer population | All four customers retained, including a non-buyer |
| Monthly revenue | January 1,500; February 2,200 |
| Duplicated reference key | Merge rejected rather than totals inflated |
| Explicit update | One high-value order flagged; retained source version preserved |
| Missing vs zero | Nullable series identifies the missing value separately |

**Try changing the rules:** exclude zero-value paid orders, add refunds, introduce a missing customer key or duplicate a source order. Explain how the expected result should change before changing the calculation.

All 50 interview scripts, eight business-result checks and 12 cheat-sheet code blocks passed in the stated environment. These checks are illustrative, not production security, concurrency stress or performance validation.
