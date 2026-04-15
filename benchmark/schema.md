# Benchmark Case Schema (v0.1)

Each entry in `benchmark/cases.json` is a single benchmark case object.

## Required top-level fields

- `case_id` (string): stable unique identifier (e.g., `case_001`)
- `title` (string): short human-readable case title
- `category` (string): vulnerability family (e.g., `access_control`)
- `severity` (string): expected severity label (`low`/`medium`/`high`/`critical`)
- `contract_file` (string): path to Solidity source file from repo root
- `language` (string): language of target contract (`solidity`)
- `public_reference` (string): provenance label + URL
  - exact finding URL when using an exact snippet
  - `Minimized reconstruction based on public finding: <url>` when simplified
  - `Sanitized variant based on public finding: <url>` when materially adapted
- `task_prompt` (string): short case-specific audit task text
- `ground_truth` (object): expected security finding details
- `tags` (array of strings): search/filter labels

## Required `ground_truth` fields

- `vulnerability_exists` (boolean)
- `vulnerability_type` (string)
- `affected_functions` (array of strings)
- `root_cause` (string)
- `exploit_path` (string)
- `impact` (string)
- `severity_rationale` (string)
- `recommended_fix` (string)

## Notes

- Paths should resolve when running from repository root.
- Keep Solidity snippets minimal and readable.
- Ground truth should describe one primary vulnerability clearly.
- Do not imply exact one-to-one source code provenance when case code is reconstructed/sanitized.
