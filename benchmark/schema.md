# Benchmark Case Schema (v0.1)

Each entry in `benchmark/cases.json` is a single benchmark case object.

## Required top-level fields

- `case_id` (string): stable unique identifier (e.g., `case_001`)
- `title` (string): short human-readable case title
- `category` (string): vulnerability family (e.g., `access_control`)
- `severity` (string): expected severity label (`low`/`medium`/`high`/`critical`)
- `contract_file` (string): path to Solidity source file from repo root
- `language` (string): language of target contract (`solidity`)
- `public_reference` (string): external reference URL
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

