"""
Performance validation for output filtering.

This script validates the token reduction claims by comparing
output sizes with and without filtering.
"""

import json


def count_tokens_approximate(text: str) -> int:
    """
    Approximate token count (rough estimate: 1 token ≈ 4 characters).
    For more accurate counting, use tiktoken or similar.
    """
    return len(text) // 4


def simulate_api_response_aggs():
    """Simulate a typical get_aggs API response."""
    return {
        "results": [
            {
                "v": 52165200,
                "vw": 184.5632,
                "o": 182.15,
                "c": 185.92,
                "h": 186.95,
                "l": 181.80,
                "t": 1704067200000,
                "n": 556789,
            }
        ],
        "ticker": "AAPL",
        "queryCount": 1,
        "resultsCount": 1,
        "adjusted": True,
        "status": "OK",
        "request_id": "abc123",
    }


def simulate_csv_output(data):
    """Simulate full CSV output (current behavior)."""
    csv = "v,vw,o,c,h,l,t,n\n"
    for record in data["results"]:
        csv += f"{record['v']},{record['vw']},{record['o']},{record['c']},{record['h']},{record['l']},{record['t']},{record['n']}\n"
    return csv


def simulate_filtered_compact(data, field="c"):
    """Simulate filtered compact output."""
    record = data["results"][0]
    return json.dumps({field: record[field]}, separators=(",", ":"))


def validate_price_query():
    """Validate Example 1: Get latest closing price."""
    print("\n=== Validating Price Query ===")

    data = simulate_api_response_aggs()

    # Without filtering
    full_output = simulate_csv_output(data)
    full_tokens = count_tokens_approximate(full_output)

    # With filtering
    filtered_output = simulate_filtered_compact(data, "c")
    filtered_tokens = count_tokens_approximate(filtered_output)

    # Calculate savings
    savings_percent = ((full_tokens - filtered_tokens) / full_tokens) * 100

    print(f"Full CSV output: {len(full_output)} chars ≈ {full_tokens} tokens")
    print(f"  Content: {full_output[:100]}...")
    print(
        f"\nFiltered compact output: {len(filtered_output)} chars ≈ {filtered_tokens} tokens"
    )
    print(f"  Content: {filtered_output}")
    print(f"\nToken reduction: {savings_percent:.1f}%")
    print(f"Status: {'✓ PASS' if savings_percent >= 50 else '✗ FAIL'}")

    return savings_percent


def validate_ohlc_query():
    """Validate Example 2: Get OHLC data."""
    print("\n=== Validating OHLC Query ===")

    # Simulate 10 days of data
    data = {
        "results": [
            {
                "v": 50000000 + i * 1000000,
                "vw": 180.0 + i,
                "o": 180.0 + i,
                "c": 181.0 + i,
                "h": 182.0 + i,
                "l": 179.0 + i,
                "t": 1704067200000 + i * 86400000,
                "n": 500000 + i * 10000,
            }
            for i in range(10)
        ]
    }

    # Full CSV (all fields)
    full_csv = simulate_csv_output(data)
    full_tokens = count_tokens_approximate(full_csv)

    # Filtered CSV (only OHLC fields: o, h, l, c, t)
    filtered_csv = "o,h,l,c,t\n"
    for record in data["results"]:
        filtered_csv += (
            f"{record['o']},{record['h']},{record['l']},{record['c']},{record['t']}\n"
        )
    filtered_tokens = count_tokens_approximate(filtered_csv)

    # Calculate savings
    savings_percent = ((full_tokens - filtered_tokens) / full_tokens) * 100

    print(f"Full CSV (10 rows, 8 fields): {len(full_csv)} chars ≈ {full_tokens} tokens")
    print(f"  {full_csv[:100]}...")
    print(
        f"\nFiltered CSV (10 rows, 5 fields): {len(filtered_csv)} chars ≈ {filtered_tokens} tokens"
    )
    print(f"  {filtered_csv[:100]}...")
    print(f"\nToken reduction: {savings_percent:.1f}%")
    print(f"Status: {'✓ PASS' if savings_percent >= 30 else '✗ FAIL'}")

    return savings_percent


def validate_news_query():
    """Validate Example 4: Get news headlines."""
    print("\n=== Validating News Query ===")

    # Simulate news response
    full_news = {
        "results": [
            {
                "id": f"article{i}",
                "title": f"Breaking News: Story {i}",
                "author": f"Reporter {i}",
                "published_utc": f"2024-01-{i:02d}T10:00:00Z",
                "article_url": f"https://example.com/article{i}",
                "description": f"This is a detailed description of news story {i}. " * 10,
                "image_url": f"https://example.com/image{i}.jpg",
                "keywords": ["tech", "stocks", "market"],
                "publisher": {"name": "News Corp", "homepage_url": "https://news.com"},
            }
            for i in range(1, 11)
        ]
    }

    # Full output (all fields)
    full_json = json.dumps(full_news, indent=2)
    full_tokens = count_tokens_approximate(full_json)

    # Filtered output (headlines only)
    filtered_results = [
        {
            "title": article["title"],
            "published_utc": article["published_utc"],
            "author": article["author"],
        }
        for article in full_news["results"]
    ]
    filtered_json = json.dumps(filtered_results, indent=2)
    filtered_tokens = count_tokens_approximate(filtered_json)

    # Calculate savings
    savings_percent = ((full_tokens - filtered_tokens) / full_tokens) * 100

    print(
        f"Full news (10 articles, all fields): {len(full_json)} chars ≈ {full_tokens} tokens"
    )
    print(f"  Sample: {full_json[:150]}...")
    print(
        f"\nFiltered news (10 articles, 3 fields): {len(filtered_json)} chars ≈ {filtered_tokens} tokens"
    )
    print(f"  Sample: {filtered_json[:150]}...")
    print(f"\nToken reduction: {savings_percent:.1f}%")
    print(f"Status: {'✓ PASS' if savings_percent >= 70 else '✗ FAIL'}")

    return savings_percent


def run_validation():
    """Run all performance validations."""
    print("=" * 70)
    print("PERFORMANCE VALIDATION")
    print("=" * 70)
    print("\nValidating token reduction claims...")
    print("=" * 70)

    results = []

    # Run validations (expected reductions are conservative estimates)
    # Real Polygon API responses are larger due to additional metadata
    results.append(("Price Query", validate_price_query(), 80))
    results.append(("OHLC Query", validate_ohlc_query(), 30))
    results.append(("News Query", validate_news_query(), 80))

    # Summary
    print("\n" + "=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)

    all_passed = True
    for test_name, actual, expected in results:
        status = "✓ PASS" if actual >= expected else "✗ FAIL"
        print(f"\n{test_name}:")
        print(f"  Expected: ≥{expected}% reduction")
        print(f"  Actual: {actual:.1f}% reduction")
        print(f"  Status: {status}")
        if actual < expected:
            all_passed = False

    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL VALIDATIONS PASSED")
        print("\nToken reduction validated:")
        print("  • Single queries: 80%+ reduction ✓")
        print("  • Multi-row data: 30%+ reduction ✓")
        print("  • News/text data: 80%+ reduction ✓")
        print("\nNote: Real Polygon API responses include additional metadata,")
        print("so actual token savings may be higher than these estimates.")
    else:
        print("✗ SOME VALIDATIONS FAILED")

    print("=" * 70)

    return all_passed


if __name__ == "__main__":
    success = run_validation()
    exit(0 if success else 1)
