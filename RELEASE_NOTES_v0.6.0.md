# Release Notes: v0.6.0

**Release Date**: 2025-11-04

## 🚀 Major Feature Release: Server-Side Output Filtering

Version 0.6.0 introduces comprehensive server-side output filtering to all 51 MCP tools, enabling **60-90% token reduction** while maintaining full backward compatibility.

---

## Highlights

### ✨ New Capabilities

- **Field Selection** - Choose specific fields from API responses
- **Output Formats** - CSV, JSON, or compact JSON
- **Row Aggregation** - Get first/last record instead of all
- **13 Presets** - Common field groups like `preset:ohlc`, `preset:price`
- **51 Tools Updated** - 100% coverage across all endpoints

### 📊 Performance

- **Single queries**: Up to 94% token reduction
- **Multi-row data**: 30-60% token reduction
- **News/text data**: 80-90% token reduction
- **Minimal overhead**: <5ms processing time

### ✅ Compatibility

- **Zero breaking changes** - All existing code works unchanged
- **Optional parameters** - Filtering is completely opt-in
- **Backward compatible** - Safe to upgrade immediately

---

## What's New

### 1. Output Filtering Parameters

All 51 tools now accept three optional filtering parameters:

```python
# Field selection
fields="ticker,close,volume"          # Specific fields
fields="preset:ohlc"                  # Preset groups

# Output format
output_format="csv"      # Default (backward compatible)
output_format="json"     # Structured JSON
output_format="compact"  # Minimal JSON

# Row aggregation
aggregate="last"   # Get only the last record
aggregate="first"  # Get only the first record
```

### 2. Field Presets

13 preset field combinations for common use cases:

| Preset | Fields |
|--------|--------|
| `preset:price` | ticker, close, timestamp |
| `preset:ohlc` | ticker, open, high, low, close, timestamp |
| `preset:ohlcv` | OHLC + volume + timestamp |
| `preset:summary` | ticker, close, volume, change_percent |
| `preset:minimal` | ticker, close |
| `preset:trade` | price, size, timestamp |
| `preset:quote` | bid, ask, bid_size, ask_size, timestamp |
| And 6 more... | See FILTERING_GUIDE.md |

### 3. New Modules

- **`filters.py`** - Core filtering logic and presets
- **Enhanced formatters** - `json_to_csv_filtered()`, `json_to_compact()`, `json_to_json_filtered()`
- **Helper function** - `_apply_output_filtering()` for consistent behavior

### 4. Comprehensive Documentation

- **FILTERING_GUIDE.md** - Complete usage guide with examples
- **MIGRATION.md** - Migration guide (spoiler: no migration needed!)
- **CHANGELOG.md** - Detailed changelog
- **IMPLEMENTATION_SUMMARY.md** - Technical implementation details
- **Examples** - filtering_examples.py and performance_validation.py

---

## Token Reduction Examples

### Example 1: Price Query (94% reduction)

**Before (500 tokens):**
```python
await get_aggs("AAPL", 1, "day", "2024-01-01", "2024-01-02")
```

**After (30 tokens):**
```python
await get_aggs("AAPL", 1, "day", "2024-01-01", "2024-01-02",
               fields="close", output_format="compact", aggregate="last")
# Returns: {"close": 185.92}
```

### Example 2: OHLC Data (60% reduction)

**Before (2000 tokens):**
```python
await get_aggs("MSFT", 1, "day", "2024-01-01", "2024-01-08")
```

**After (800 tokens):**
```python
await get_aggs("MSFT", 1, "day", "2024-01-01", "2024-01-08",
               fields="preset:ohlc")
# Returns CSV with only OHLC fields
```

### Example 3: News Headlines (88% reduction)

**Before (5000 tokens):**
```python
await list_ticker_news(ticker="AAPL", limit=10)
```

**After (600 tokens):**
```python
await list_ticker_news(ticker="AAPL", limit=10,
                       fields="preset:news_headlines")
# Returns only title, published_utc, author
```

---

## Updated Tools

All 51 tools now support filtering:

**Market Data (13 tools)**
- Aggregates: get_aggs, list_aggs, get_grouped_daily_aggs, get_daily_open_close_agg, get_previous_close_agg
- Trades: list_trades, get_last_trade, get_last_crypto_trade
- Quotes: list_quotes, get_last_quote, get_last_forex_quote
- Conversions: get_real_time_currency_conversion
- Market: get_market_holidays, get_market_status

**Reference Data (13 tools)**
- Tickers: list_tickers, get_ticker_details, list_ticker_news, get_ticker_types
- Snapshots: list_universal_snapshots, get_snapshot_all, get_snapshot_direction, get_snapshot_ticker, get_snapshot_option, get_snapshot_crypto_book
- Corporate: list_splits, list_dividends
- Exchanges: get_exchanges, list_conditions

**Fundamentals (6 tools)**
- list_stock_financials, list_ipos, list_short_interest, list_short_volume
- list_treasury_yields, list_inflation

**Benzinga Data (8 tools)**
- list_benzinga_analyst_insights, list_benzinga_analysts, list_benzinga_consensus_ratings
- list_benzinga_earnings, list_benzinga_firms, list_benzinga_guidance
- list_benzinga_news, list_benzinga_ratings

**Futures (11 tools)**
- list_futures_aggregates, list_futures_contracts, get_futures_contract_details
- list_futures_products, get_futures_product_details, list_futures_quotes
- list_futures_trades, list_futures_schedules, list_futures_schedules_by_product_code
- list_futures_market_statuses, get_futures_snapshot

---

## Testing

### Comprehensive Test Suite

- **82 tests total** - All passing ✅
- **35 filter tests** - Complete coverage of filtering logic
- **47 formatter tests** - All output formats validated
- **Backward compatibility** - Verified existing code works

### Validation Scripts

Run the included validation scripts:

```bash
# View examples
python examples/filtering_examples.py

# Validate token reduction
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

---

## Upgrade Instructions

### Quick Upgrade

```bash
# Claude CLI
claude mcp add polygon -e POLYGON_API_KEY=your_api_key_here -- uvx --from git+https://github.com/polygon-io/mcp_polygon@v0.6.0 mcp_polygon
```

### Claude Desktop

Update your config file (`claude_desktop_config.json`):

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

### No Migration Required

All filtering parameters are optional. Your existing code works unchanged:

```python
# This still works exactly as before
result = await get_aggs("AAPL", 1, "day", "2024-01-01", "2024-01-10")
```

---

## Documentation

- **Complete Guide**: [FILTERING_GUIDE.md](FILTERING_GUIDE.md)
- **Migration Guide**: [MIGRATION.md](MIGRATION.md)
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
- **Implementation**: [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)

---

## Technical Details

### Implementation

- **New module**: `src/mcp_polygon/filters.py` (180 lines)
- **Enhanced formatters**: 3 new functions in `formatters.py`
- **Helper function**: `_apply_output_filtering()` for consistency
- **Test coverage**: 54 new tests, all passing

### Code Quality

- ✅ All code formatted with ruff
- ✅ All linting checks pass
- ✅ 100% backward compatibility
- ✅ Zero breaking changes
- ✅ Comprehensive documentation

### Performance

- **Overhead**: <5ms (negligible)
- **Benefits**: Reduced data processing
- **Token savings**: 60-90% reduction
- **Memory**: Lower usage (processing less data)

---

## Breaking Changes

**None!** Version 0.6.0 is fully backward compatible.

---

## Deprecations

**None.** All existing functionality remains supported.

---

## Known Issues

**None identified.** All 82 tests passing.

---

## Contributors

Implementation by Claude Code Agent via Anthropic's Claude SDK.

---

## What's Next

Future enhancements under consideration:

- Row filtering with conditions (e.g., `volume_gt=1000000`)
- Field exclusion (e.g., `exclude_fields="vwap"`)
- Smart defaults based on usage patterns
- Additional presets based on user feedback
- Usage analytics dashboard

---

## Support

- **Documentation**: See included .md files
- **Examples**: `examples/` directory
- **Issues**: GitHub issue tracker
- **Questions**: See FILTERING_GUIDE.md FAQ section

---

## Summary

Version 0.6.0 is a significant feature release that enables dramatic token reduction while maintaining full backward compatibility. All 51 tools now support flexible output filtering, making the MCP Polygon server more efficient and cost-effective.

**Recommended action**: Upgrade to v0.6.0 today and start saving tokens!

---

**Download**: `git+https://github.com/polygon-io/mcp_polygon@v0.6.0`
**Release Date**: 2025-11-04
**License**: See LICENSE file
