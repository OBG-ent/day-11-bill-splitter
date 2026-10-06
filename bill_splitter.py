#!/usr/bin/env python3
"""
Day 11 (simple) of my daily coding journey - Bill Splitter.

End the "who owes what?" debate at the table. This tiny CLI tool splits a
restaurant bill between friends - evenly, or itemized per person - with
tax and tip handled fairly (each person's share of tax/tip is proportional
to what they ordered).

Usage:
    python bill_splitter.py --total 120 --tip 18 --tax 13 --people 4
    python bill_splitter.py --itemized

Run with --help to see every option.
"""

import argparse


def money(amount):
    """Round a float to the nearest cent, as a float."""
    return round(amount + 1e-9, 2)


def split_even(subtotal, tip_pct, tax_pct, people):
    """
    Split the whole bill evenly. Returns (per_person, total, tip, tax).

    Any leftover cent from rounding is added to the first person's share
    so the shares always add up to the real total.
    """
    tip = subtotal * tip_pct / 100
    tax = subtotal * tax_pct / 100
    total = subtotal + tip + tax
    each = money(total / people)
    # Fix rounding so shares add up exactly to the total.
    remainder = money(total - each * people)
    shares = [each] * people
    shares[0] = money(shares[0] + remainder)
    return shares, money(total), money(tip), money(tax)


def split_itemized(orders, tip_pct, tax_pct):
    """
    Split itemized: each person pays for what they ordered, plus their
    fair share of tax and tip (proportional to their subtotal).

    orders: dict like {"Ava": [12.50, 8.00], "Ben": [20.00]}
    Returns (shares_dict, total, tip, tax).
    """
    subtotal = sum(sum(items) for items in orders.values())
    if subtotal == 0:
        raise ValueError("The bill can't be $0.")
    tip = subtotal * tip_pct / 100
    tax = subtotal * tax_pct / 100
    total = subtotal + tip + tax

    shares = {}
    for person, items in orders.items():
        person_sub = sum(items)
        fraction = person_sub / subtotal
        shares[person] = money(person_sub + fraction * (tip + tax))

    # Fix rounding so shares add up exactly to the total.
    remainder = money(total - sum(shares.values()))
    first = next(iter(shares))
    shares[first] = money(shares[first] + remainder)
    return shares, money(total), money(tip), money(tax)


def print_receipt(shares, total, tip, tax):
    """Print a clean little receipt to the terminal."""
    print("\n" + "=" * 34)
    print("          BILL SPLIT RECEIPT")
    print("=" * 34)
    if isinstance(shares, dict):
        for person, amount in shares.items():
            print(f"  {person:<20} ${amount:>7.2f}")
    else:
        for i, amount in enumerate(shares, start=1):
            print(f"  Person {i:<15} ${amount:>7.2f}")
    print("-" * 34)
    print(f"  {'Tip':<20} ${tip:>7.2f}")
    print(f"  {'Tax':<20} ${tax:>7.2f}")
    print(f"  {'TOTAL':<20} ${total:>7.2f}")
    print("=" * 34 + "\n")


def ask_float(prompt, default=None):
    """Prompt for a number, with an optional default."""
    while True:
        suffix = f" [{default}]" if default is not None else ""
        raw = input(f"{prompt}{suffix}: ").strip()
        if raw == "" and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print("  Please enter a number.")


def interactive():
    """Walk the user through a split, question by question."""
    print("\n=== Bill Splitter ===\n")
    mode = input("Split (e)venly or (i)temized? ").strip().lower()
    tip = ask_float("Tip %", 18)
    tax = ask_float("Tax %", 13)

    if mode.startswith("i"):
        orders = {}
        n = int(ask_float("How many people"))
        for i in range(1, n + 1):
            name = input(f"Name of person {i}: ").strip() or f"Person {i}"
            raw = input(f"  {name}'s items, comma-separated prices (e.g. 12.50, 8): ")
            items = [float(x) for x in raw.split(",") if x.strip()]
            orders[name] = items
        shares, total, tip_amt, tax_amt = split_itemized(orders, tip, tax)
    else:
        subtotal = ask_float("Bill subtotal ($)")
        people = int(ask_float("How many people"))
        shares, total, tip_amt, tax_amt = split_even(subtotal, tip, tax, people)

    print_receipt(shares, total, tip_amt, tax_amt)


def main():
    parser = argparse.ArgumentParser(
        description="Split a restaurant bill between friends, evenly or itemized."
    )
    parser.add_argument("--total", type=float, help="Bill subtotal in dollars")
    parser.add_argument("--tip", type=float, default=18, help="Tip percent (default 18)")
    parser.add_argument("--tax", type=float, default=13, help="Tax percent (default 13)")
    parser.add_argument("--people", type=int, help="Number of people (even split)")
    parser.add_argument(
        "--itemized",
        action="store_true",
        help="Enter each person's items interactively",
    )
    args = parser.parse_args()

    if args.itemized:
        interactive()
    elif args.total is not None and args.people:
        shares, total, tip, tax = split_even(args.total, args.tip, args.tax, args.people)
        print_receipt(shares, total, tip, tax)
    else:
        # No flags given: fall back to the friendly guided mode.
        interactive()


if __name__ == "__main__":
    main()
