# Changelog
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