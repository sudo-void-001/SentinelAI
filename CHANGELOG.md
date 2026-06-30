# Changelog

## [1.0.0] — 2026-06-28

### Added
- Project foundation and folder structure
- Data models: Article and CVE dataclasses
- SQLite database layer with full CRUD operations
- Cybersecurity news collection from HackerNews and RSS feeds
- CVE tracking from NVD and CISA KEV APIs
- AI summarization, categorization, and severity estimation via Groq
- Telegram bot notifications — daily digest and critical alerts
- Automated pipeline scheduler using APScheduler
- Daily and weekly report generation
- Complete documentation skeleton in docs/

## [1.0.1] — 2026-06-30

### Fixed
- Updated Groq model from deprecated llama3-8b-8192 to openai/gpt-oss-20b
- Fixed Telegram bot token and chat ID configuration issues
- Resolved .env loading inconsistencies between terminals

### Changed
- Improved Telegram digest with severity emoji indicators
- Added digest statistics header showing threat count by severity
- Better fallback text when AI summary is unavailable
- Updated requirements.txt with correct groq SDK version

### Added
- Category and source metadata shown in Telegram digest



## [1.0.2] — 2026-06-30

### Added
- Full-article content scraping in news.py to improve AI summary quality

### Fixed
- Added graceful handling for scraping failures (403 Forbidden from sources that block bots)
- Added "insufficient content" check before sending articles to Groq, preventing wasted API calls on near-empty text
- Pipeline now skips problematic articles instead of crashing, logging the reason for each skip

### Notes
- BleepingComputer and similar sites block direct scraping with 403 errors — this is expected behavior, not a bug
- Articles with too little scraped content fall back to being skipped rather than generating a poor or empty AI summary
- Future improvement: use RSS description text as a fallback summary source when full-article scraping fails
