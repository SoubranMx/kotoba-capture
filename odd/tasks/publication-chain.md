# Publish the reviewed prototype as a feature branch chain

Prepare the existing prototype for review under approved issue [#1](https://github.com/SoubranMx/kotoba-capture/issues/1), without changing behavior. Use one draft, no-merge tracker against `main` and five children, each targeting its immediate predecessor. Publishing and PR creation are separate authorized steps after local preparation and verification.

## Scope and decisions

- Preserve all 22 original commits, tests, documentation, and explicitly authorized tracked `.engram` artifacts through cherry-picking; do not rewrite the original branch.
- Author only this passive tracker. Keep `.local` inputs, OCR output, images, models, references, and detailed reports private and ignored.
- No new behavior, warning correction, dependency installation, OCR, merge, force-push, or original-branch rebase is included.
- Keep the existing general issue form from the new `main` boundary.
- Existing source review authority was consumed; do not create duplicate native reviews for identical source bytes. This tracker needs structural verification only.
- The user accepted cohesive slices larger than 400 changed lines. Tests and explanatory documentation stay with their behavior; one honest slicing pass is complete, with no code-golf or further artificial splitting.

## Boundaries and route

Original predecessor: `cc7cc45f8a593d2dd040800408465eb64722ba9d`.
Original final boundary: `845269aa7121260156f729df84548486ae303aca`.
Tracker base: `b642d4161bcb4dde0dd0aeff98ce59e0c610eccd` (`main`, including the general issue form).
Delivery strategy: `exception-ok`, Feature Branch Chain. All reconstruction tasks use delegated direct execution because history preparation, multiple branches, and full checks require a bounded worker. Original refs remain unchanged; every child keeps all prior chain commits.

| ID | Branch | PR base | Original commit boundary | Count |
|---|---|---|---|---:|
| P0 | `feat/prototype-publication` | `main` | New passive tracker only | 1 |
| P1 | `feat/prototype-publication-01-core` | `feat/prototype-publication` | `d60ffa9` | 1 |
| P2 | `feat/prototype-publication-02-history` | `feat/prototype-publication-01-core` | `57b8a73` through `4a5bce5` | 10 |
| P3 | `feat/prototype-publication-03-selector` | `feat/prototype-publication-02-history` | `6766776`, `d7aa888` | 2 |
| P4 | `feat/prototype-publication-04-gpu-pilot` | `feat/prototype-publication-03-selector` | `c9b8f92` through `974b8ac` | 8 |
| P5 | `feat/prototype-publication-05-temporal` | `feat/prototype-publication-04-gpu-pilot` | `845269a` | 1 |

```text
main
└── publication (draft tracker; do not merge)
    └── 01-core
        └── 02-history
            └── 03-selector
                └── 04-gpu-pilot
                    └── 05-temporal
```

## Acceptance and checks

- [ ] P0: Commit and structurally read back this nonempty documentation-only tracker.
- [ ] P1–P5: Reconstruct the exact approved commit groups without speculative conflict resolution.
- [ ] Verify all parent-child ancestry and isolated diffs; retain tests and docs with their behavior.
- [ ] Run the full unittest suite in each child's `apps/server` directory with the existing GPU-environment interpreter, `PYTHONPATH=.`, and `-B -m unittest discover -s tests`.
- [ ] Run `/usr/bin/python3 -B -S tests/check_selector_stdlib.py` for children 3, 4, and 5.
- [ ] Run `git diff --check` for each parent-child range. Shellcheck is N/A only after confirming no shell scripts changed.
- [ ] Compare final tree blobs and modes with the original final boundary; permit only `.github/ISSUE_TEMPLATE/general.yml` and this tracker as exceptions.
- [ ] Confirm no `.local` artifacts enter any branch; do not inspect or transcribe `.engram` contents.
- [ ] Confirm the original worktree, index, HEAD, and branch remain unchanged.
- [ ] Parent spot-checks results before a separate actor publishes branches and creates PRs.

No meaningful runnable RED applies: this is branch-only delivery of already implemented bytes, not a behavior change. No source-mutating formatters are allowed. Record observed command results, failures, skips, branch identities, and changed-line counts in the preparation handoff and eventual PR descriptions. Do not amend the tracker after children exist: that would pollute their bases.

## Deferred warning

The known malformed-baseline warning is intentionally unchanged. Existing prototype limitations and failed diagnostics remain visible; successful code checks do not establish subtitle accuracy or production readiness. Fixing the warning requires separate approval.

## Progress and next step

Initial checkpoint: authorization, approved issue, source boundaries, the 1/10/2/8/1 partition, and delivery strategy are established. Local reconstruction and per-child checks are pending at this commit. The tracker remains draft/no-merge when published. PR bodies must state each boundary, dependency diagram, rollback scope, honest applicable checks and N/A items, and link issue #1. Do not claim labels, CI, publication, or PR creation before they are observed.
