# 🧾 Bill Splitter

**Never argue over the restaurant bill again.** A tiny Python CLI that splits a check between friends — evenly, or item-by-item — with tax and tip shared fairly.

*Day 11 (simple build) of my daily coding journey — one small project, shipped every day.*

## Features

- **Even split** — one subtotal, divide it up in seconds
- **Itemized split** — each person pays for what they ordered, plus their fair share of tax and tip (proportional, not lazy-even)
- **Rounding-proof** — leftover cents are assigned so the shares always add up to the real total
- **Guided mode** — run it with no flags and it walks you through step by step

## Run it in 30 seconds

No dependencies — just Python 3.

```bash
# Even split: $120 bill, 18% tip, 13% tax, 4 people
python bill_splitter.py --total 120 --tip 18 --tax 13 --people 4

# Guided mode (asks you everything)
python bill_splitter.py

# Itemized mode (each person enters their dishes)
python bill_splitter.py --itemized
```

### Example output

```
==================================
          BILL SPLIT RECEIPT
==================================
  Person 1             $  39.31
  Person 2             $  39.30
  Person 3             $  39.30
  Person 4             $  39.30
----------------------------------
  Tip                  $  21.60
  Tax                  $  15.60
  TOTAL                $ 157.20
==================================
```

## Options

| Flag | What it does |
|---|---|
| `--total` | Bill subtotal in dollars |
| `--people` | Number of people (even split) |
| `--tip` | Tip percent (default 18) |
| `--tax` | Tax percent (default 13) |
| `--itemized` | Enter each person's items one by one |

## What I practiced

- `argparse` for a clean command-line interface
- Splitting a total proportionally and fixing float rounding so shares sum exactly
- Writing a friendly interactive fallback with input validation
