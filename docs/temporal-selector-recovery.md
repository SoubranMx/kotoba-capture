# Temporal selector review proposals

`temporal-review/v1` is an opt-in, cached-data sidecar. It never replaces a v17 selection, runs OCR, reads an image, or claims continuous caption identity.

## Input contract

The caller supplies a frozen source identity and timestamp-ordered slots. A populated slot contains the original pilot record plus its timestamp and source identity. The caller first validates every original record and frame against its stored pilot plan; the sidecar then rechecks the canonical record hash, source identity, style binding, full-source geometry, and an exact v17 replay.

| Field | Requirement |
| --- | --- |
| `frozen.source` | Exact video, run, native, style, and model provenance hashes; v17 profile. |
| `frozen.policy` | Stored v17 policy used for the original record. |
| populated slot | Original record, its timestamp, and an identity exactly equal to `frozen.source`. |
| planned slot | Timestamp only; it is audited as unknown and consumes an in-window attempt. |

Malformed, non-finite, changed, or unbound payloads fail closed. The helper does not create, resume, or rebind historical records.

## Selection rule

Only an original v17 review result with reason `ambiguous_groups` or `unknown_visual_style` is eligible. A proposal needs exactly one current candidate group whose ordered native rows, full ROI coverage, orientation, typography, and measured style all survive an exact v17 replay. Its NFKC/whitespace-normalized text must equal a valid neighboring selected v17 anchor and its aggregate source-normalized box IoU must be at least `0.85`.

The proposed text is the current group's raw text. The anchor only corroborates a match; it never supplies text. Competing current groups remain in the audit. More than one current group matching an anchor abstains.

## Temporal audit

The fixed configuration is a two-second window and at most eight attempted in-window slots. Timestamp placement is admitted before payload inspection. Every attempted in-window slot consumes the budget, including unknown, malformed, rejected, or provenance-invalid slots. Out-of-window slots are audited but do not consume it.

A valid selected neighboring record with different normalized text is a changed-caption barrier for only that time direction. It prevents a farther matching anchor from crossing that boundary. Matching endpoint agreement never proves a continuous caption.

## Output semantics

The function returns an immutable copy of the original baseline selection in `result` and, at most, a separate `proposal`. All outcomes set:

- `reviewRequired: true`
- `continuityVerified: false`
- `captionIntentVerified: false`

A proposal is review assistance, not automatic recovery, an OCR improvement, a CER result, or a whole-video reliability claim.

## Frozen replay boundary

The private replay manifest freezes membership, timestamp context, provenance hashes, and the fixed rule before any cached replay. It contains no public transcription or reference material. A replay may report only proposals, abstentions, and control retention; it cannot tune this configuration or alter original records.

## Measured frozen replay

One frozen CPU-only replay produced one review-only proposal from sixteen target records; fifteen targets abstained. All seven original selected positive controls were retained. Three separate cached CPU signage controls remain limited abstention evidence and are not a full-frame GPU negative corpus. This is not a character-recognition, CER, or automatic-recovery result.

## Candidate-local style qualification

Every structurally valid current candidate group remains in the audit. Style qualification applies only to a group considered for a proposal: an unknown or mismatched proposed group cannot qualify, while an unknown competitor does not veto a distinct fully matched group. Duplicate qualified matches still abstain. This correction leaves the window, budget, geometry threshold, source bindings, and review-only semantics unchanged.

The second frozen replay produced six review-only proposals and ten abstentions from the unchanged target membership. It retained all selected positive controls. This remains review assistance rather than automatic recovery or a recognition-quality metric.

## Validation before selected-baseline retention

A selected baseline is preserved only after its configuration, frozen identity, canonical record, style binding, native result, and exact v17 replay validate. Invalid selected payloads remain immutable audit input but fail closed; they are not reported as validated preservation. This ordering change does not alter temporal thresholds or proposal rules.
