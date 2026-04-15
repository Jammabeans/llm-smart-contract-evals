# Scoring Rubric (v0.1)

This benchmark uses manual or semi-manual grading for model outputs. v0.1 does **not** attempt automatic semantic grading of free-text responses.

## Scored dimensions (0/1/2 each)

### `detection_score`
- `0`: Misses the vulnerability or says no vulnerability exists.
- `1`: Flags a potential issue but uncertain/weak conclusion.
- `2`: Clearly identifies that a vulnerability exists.

### `localization_score`
- `0`: Does not localize the issue to relevant function(s)/logic.
- `1`: Partially localizes (some relevant logic mentioned, incomplete/ambiguous).
- `2`: Correctly localizes the primary vulnerable function(s) or logic path.

### `exploit_reasoning_score`
- `0`: No plausible exploit reasoning.
- `1`: Basic exploit idea but incomplete or partially incorrect.
- `2`: Clear, plausible exploit path with coherent attack reasoning.

### `severity_score`
- `0`: Clearly wrong severity framing.
- `1`: Reasonable but not well justified or slightly off.
- `2`: Severity is appropriate and well justified.

### `fix_score`
- `0`: Missing or incorrect remediation.
- `1`: Partially useful but incomplete remediation.
- `2`: Practical, correct, and sufficiently specific remediation.

## Failure taxonomy

`failure_mode` must be exactly one of:

- `missed_vulnerability`
- `vague_suspicion`
- `wrong_vulnerability`
- `right_vulnerability_wrong_severity`
- `right_vulnerability_weak_fix`
- `hallucinated_issue`
- `no_major_failure`

## Manual scoring CSV schema

Each row is one `(run_id, model_name, prompt_style, case_id)` evaluation with these columns:

- `run_id`
- `model_name`
- `prompt_style`
- `case_id`
- `detection_score`
- `localization_score`
- `exploit_reasoning_score`
- `severity_score`
- `fix_score`
- `failure_mode`
- `evaluator_notes`

Notes:
- `prompt_style` is one of `baseline` or `senior_auditor_concise`.
- Each score column is an integer in `{0, 1, 2}`.
- `total_score` is computed as the sum of the five score columns.

