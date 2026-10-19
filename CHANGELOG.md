# Changelog

## [0.2.0] - 2026-10-19

### Added

- Add `preserve_order` parameter to `FettaLoader` to control output order: match the input URL list order, or yield results as they complete.
- Add `include_sections` parameter to `FettaLoader` to control which sections populate `Document.page_content` (`metadata`, `links`, `images`, `html`, `text`).
- Add new fields to `Document.metadata`.
