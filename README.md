# MultiEngineSearch (mse)

A unified command-line interface for multiple search engines that follows Unix philosophy principles.

## Overview

MultiEngineSearch (mse) is a lightweight, extensible command-line tool that provides a unified interface to query multiple search engines. It focuses on doing one thing well: searching across different engines with consistent output formats and flexible configuration options.

## Features

- **Multiple Search Engine Support**: Query Google, Bing, DuckDuckGo, and other popular search engines
- **Flexible Output Formats**: Export results in JSON, Markdown, or plain text
- **Unix-friendly**: Supports piping, redirection, and follows Unix conventions
- **Configurable**: Easy-to-use configuration file for API keys and preferences
- **Extensible**: Plugin architecture for adding new search engines
- **Lightweight**: Minimal dependencies and fast execution

## Installation

```bash
# Install from PyPI (coming soon)
pip install multienginesearch

# Or install from source
git clone https://github.com/yourusername/MultiEngineSearch.git
cd MultiEngineSearch
pip install -e .
```

## Quick Start

```bash
# Basic search
mse "python programming tutorial"

# Search with specific engine
mse -e google "machine learning basics"

# Output to JSON format
mse -f json "web development" > results.json

# Search multiple engines and compare
mse -e google,bing "climate change" -f markdown -o comparison.md
```

## Usage

```
mse [OPTIONS] QUERY

Arguments:
  QUERY                 Search query string

Options:
  -e, --engine TEXT     Search engine(s) to use [default: google]
                        Available: google, bing, duckduckgo, yandex
                        Use comma-separated values for multiple engines
  -f, --format TEXT     Output format [default: text]
                        Available: text, json, markdown
  -o, --output PATH     Output file path (default: stdout)
  -n, --num-results INT Number of results per engine [default: 10]
  -l, --lang TEXT       Search language [default: en]
  -r, --region TEXT     Search region/country code
  -c, --config PATH     Custom configuration file path
  -v, --verbose         Enable verbose output
  -q, --quiet           Suppress all output except results
  --version             Show version information
  --help                Show this help message
```

## Configuration

Create a configuration file at `~/.config/mse/config.yaml`:

```yaml
# Default search engine
default_engine: google

# API Keys and credentials
engines:
  google:
    api_key: "your-google-api-key"
    search_engine_id: "your-search-engine-id"
  bing:
    api_key: "your-bing-api-key"
  duckduckgo:
    # No API key required
    enabled: true

# Output preferences
output:
  default_format: text
  max_results: 10
  include_metadata: true

# Search preferences
search:
  default_language: en
  default_region: us
  safe_search: moderate
```

## Output Formats

### Text Format (Default)
```
1. Title: "Python Programming Tutorial - Learn Python"
   URL: https://example.com/python-tutorial
   Description: A comprehensive guide to learning Python programming...

2. Title: "Python for Beginners - Official Documentation"
   URL: https://docs.python.org/tutorial/
   Description: The official Python tutorial covering all basics...
```

### JSON Format
```json
{
  "query": "python programming tutorial",
  "engine": "google",
  "timestamp": "2024-06-11T10:30:00Z",
  "total_results": 2,
  "results": [
    {
      "title": "Python Programming Tutorial - Learn Python",
      "url": "https://example.com/python-tutorial",
      "description": "A comprehensive guide to learning Python programming...",
      "rank": 1
    },
    {
      "title": "Python for Beginners - Official Documentation",
      "url": "https://docs.python.org/tutorial/",
      "description": "The official Python tutorial covering all basics...",
      "rank": 2
    }
  ]
}
```

### Markdown Format
```markdown
# Search Results: "python programming tutorial"

**Engine:** Google | **Date:** 2024-06-11 | **Results:** 2

## 1. [Python Programming Tutorial - Learn Python](https://example.com/python-tutorial)
A comprehensive guide to learning Python programming...

## 2. [Python for Beginners - Official Documentation](https://docs.python.org/tutorial/)
The official Python tutorial covering all basics...
```

## Examples

### Basic Usage
```bash
# Simple search
mse "best pizza recipes"

# Search with specific engine
mse -e bing "weather forecast New York"

# Multiple engines comparison
mse -e google,duckduckgo "privacy tools" -f markdown
```

### Advanced Usage
```bash
# Search in different language
mse -e google "machine learning" -l zh -r cn

# Limit results and save to file
mse -e bing "stock market analysis" -n 5 -f json -o market_results.json

# Quiet mode for scripting
mse -q -e duckduckgo "command line tools" | grep -i "terminal"

# Verbose mode for debugging
mse -v -e google "debugging techniques" -f text
```

### Unix Pipeline Integration
```bash
# Filter results by domain
mse "open source projects" -f json | jq '.results[] | select(.url | contains("github.com"))'

# Count total results
mse "python libraries" -f json | jq '.total_results'

# Extract only URLs
mse "documentation sites" -f json | jq -r '.results[].url'

# Search and grep for specific terms
mse "web frameworks" | grep -i "django\|flask"
```

## Supported Search Engines

| Engine | Status | API Required | Notes |
|--------|--------|--------------|-------|
| Google | ✅ | Yes | Custom Search JSON API |
| Bing | ✅ | Yes | Bing Search API v7 |
| DuckDuckGo | ✅ | No | Instant Answer API |
| Yandex | 🚧 | Yes | Yandex Search API |
| Baidu | 🚧 | Yes | Baidu Search API |

Legend: ✅ Implemented | 🚧 Planned | ❌ Not supported

## Error Handling

The tool follows Unix conventions for error handling:
- Exit code 0: Success
- Exit code 1: General error
- Exit code 2: Invalid arguments
- Exit code 3: Network/API error
- Exit code 4: Configuration error

Error messages are sent to stderr, while results go to stdout.

## Privacy and Rate Limiting

- No search queries are logged by default
- Respects search engine rate limits
- Supports proxy configuration for privacy
- Option to disable telemetry and tracking

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

### Requirements
- Python 3.8+
- Poetry for dependency management
- API keys for commercial search engines

### Running Tests
```bash
poetry install
poetry run pytest
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please read the contributing guidelines and submit pull requests for any improvements.

## Roadmap

- [ ] v0.1.0: Basic CLI with Google and DuckDuckGo support
- [ ] v0.2.0: Add Bing support and improved output formats
- [ ] v0.3.0: Plugin system for custom search engines
- [ ] v0.4.0: Search result caching and offline mode
- [ ] v0.5.0: Web interface and API server mode

---

**Note**: This tool is for educational and research purposes. Please respect search engine terms of service and rate limits.