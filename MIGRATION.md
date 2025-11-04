# Migration Guide: v0.5.1 → v0.6.0

## Quick Summary

✅ **No breaking changes** - Your existing code works unchanged!
✅ **Backward compatible** - All new parameters are optional
✅ **Zero migration required** - Upgrade safely without code changes

## What's New

Version 0.6.0 adds optional server-side output filtering to all 51 MCP tools, enabling 60-90% token reduction.

## Do I Need to Migrate?

**No!** Version 0.6.0 is fully backward compatible. You can upgrade immediately without changing any code.

## Upgrade Steps

### Step 1: Update Version

Update your installation to v0.6.0:

```bash
# Claude CLI
claude mcp add polygon -e POLYGON_API_KEY=your_api_key_here -- uvx --from git+https://github.com/polygon-io/mcp_polygon@v0.6.0 mcp_polygon
```

Or in your Claude Desktop config:

```json
{
    "mcpServers": {
        "polygon": {
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/polygon-io/mcp_polygon@v0.6.0",
                "mcp_polygon"
            ],
            "env": {
                "POLYGON_API_KEY": "your_api_key_here"
            }
        }
    }
}
```

### Step 2: Test (Optional)

Run your existing queries - they should work exactly as before:

```python
# This still works unchanged
result = await get_aggs("AAPL", 1, "day", "2024-01-01", "2024-01-10")
```

### Step 3: Adopt Filtering (Optional)

When ready, gradually adopt filtering for token savings:

```python
# New: Add filtering for 94% token reduction
result = await get_aggs(
    "AAPL", 1, "day", "2024-01-01", "2024-01-10",
    fields="close",
    output_format="compact",
    aggregate="last"
)
# Returns: {"close": 185.92}
```

## New Features Overview

### 1. Field Selection

Choose specific fields to return:

```python
# Specific fields
fields="ticker,close,volume"

# Or use presets
fields="preset:ohlc"      # ticker, open, high, low, close, timestamp
fields="preset:price"     # ticker, close, timestamp
fields="preset:summary"   # ticker, close, volume, change_percent
```

**13 presets available** - See FILTERING_GUIDE.md

### 2. Output Formats

Choose how data is formatted:

```python
output_format="csv"      # Default (backward compatible)
output_format="json"     # Structured JSON
output_format="compact"  # Minimal JSON for single records
```

### 3. Row Aggregation

Get just one record instead of all:

```python
aggregate="last"   # Get only the last record
aggregate="first"  # Get only the first record
```

## Migration Strategies

### Strategy 1: Gradual Adoption (Recommended)

Upgrade to v0.6.0 and adopt filtering incrementally:

1. **Week 1**: Upgrade, test existing code works
2. **Week 2**: Add filtering to high-frequency queries
3. **Week 3**: Add filtering to large-response queries
4. **Week 4**: Review token savings, optimize further

### Strategy 2: Immediate Optimization

Identify your top 10 most-used queries and add filtering immediately:

```python
# Before
price = await get_last_trade("AAPL")

# After (93% token reduction)
price = await get_last_trade("AAPL", fields="price", output_format="compact")
```

### Strategy 3: Use Defaults

Upgrade and continue as-is. Filtering is completely optional.

## Common Migration Patterns

### Pattern 1: Price Queries

**Before:**
```python
result = await get_aggs("AAPL", 1, "day", "2024-01-01", "2024-01-02")
# ~500 tokens
```

**After:**
```python
result = await get_aggs(
    "AAPL", 1, "day", "2024-01-01", "2024-01-02",
    fields="close",
    output_format="compact",
    aggregate="last"
)
# ~30 tokens (94% reduction)
```

### Pattern 2: OHLC Data

**Before:**
```python
result = await get_aggs("MSFT", 1, "day", "2024-01-01", "2024-01-10")
# ~2000 tokens
```

**After:**
```python
result = await get_aggs(
    "MSFT", 1, "day", "2024-01-01", "2024-01-10",
    fields="preset:ohlc"
)
# ~800 tokens (60% reduction)
```

### Pattern 3: News Headlines

**Before:**
```python
result = await list_ticker_news(ticker="AAPL", limit=10)
# ~5000 tokens
```

**After:**
```python
result = await list_ticker_news(
    ticker="AAPL",
    limit=10,
    fields="preset:news_headlines"
)
# ~600 tokens (88% reduction)
```

## Validation

Run the validation script to verify token savings:

```bash
python examples/performance_validation.py
```

Expected output:
```
✓ ALL VALIDATIONS PASSED

Token reduction validated:
  • Single queries: 80%+ reduction ✓
  • Multi-row data: 30%+ reduction ✓
  • News/text data: 80%+ reduction ✓
```

## Troubleshooting

### Issue: "Unknown preset" error

**Problem:**
```python
fields="preset:invalid_name"
# Error: Unknown preset: invalid_name
```

**Solution:**
Use one of the 13 available presets. See FILTERING_GUIDE.md for the full list:
- preset:price, preset:ohlc, preset:summary, etc.

### Issue: Empty response

**Problem:**
Field names don't match, resulting in empty output.

**Solution:**
Field names are case-sensitive and use underscores for nested data:
```python
# Nested data is flattened with underscores
# Original: {"day": {"close": 185.92}}
# Field name: "day_close" (not "day.close" or "close")

fields="day_close"  # Correct
```

### Issue: Invalid output format

**Problem:**
```python
output_format="xml"
# Error: Invalid output_format
```

**Solution:**
Only three formats are supported:
- `"csv"` (default)
- `"json"`
- `"compact"`

## Rollback Plan

If you encounter any issues, rollback to v0.5.1:

```bash
# Claude CLI
claude mcp add polygon -e POLYGON_API_KEY=your_api_key_here -- uvx --from git+https://github.com/polygon-io/mcp_polygon@v0.5.1 mcp_polygon
```

Or update your config to use `@v0.5.1`.

**Note:** Rollback should not be necessary as v0.6.0 is fully backward compatible.

## Support & Resources

- **Complete Guide**: [FILTERING_GUIDE.md](FILTERING_GUIDE.md)
- **Examples**: [examples/filtering_examples.py](examples/filtering_examples.py)
- **Validation**: [examples/performance_validation.py](examples/performance_validation.py)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Implementation**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

## FAQ

**Q: Will this break my existing code?**
A: No! All filtering parameters are optional. Your code works unchanged.

**Q: Do I have to use filtering?**
A: No, it's completely optional. Use it when you want to save tokens.

**Q: Can I use filtering on some queries but not others?**
A: Yes! Mix and match as needed.

**Q: What if I specify a field that doesn't exist?**
A: Non-existent fields are silently ignored. Only matching fields are returned.

**Q: Can I combine presets with custom fields?**
A: No, choose either a preset OR custom fields (not both).

**Q: Is there any performance overhead?**
A: Minimal (<5ms). Filtering reduces data processing, so it may actually improve performance.

**Q: Are there any new dependencies?**
A: No, filtering uses only stdlib (json, csv, io).

## Summary

✅ **Upgrade safely** - Zero breaking changes
✅ **Test thoroughly** - Run validation scripts
✅ **Adopt gradually** - No rush, filtering is optional
✅ **Save tokens** - 60-90% reduction when you need it
✅ **Get support** - See guides and examples

**Recommended action**: Upgrade to v0.6.0 today, adopt filtering when ready!
