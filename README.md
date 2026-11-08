# Fault-Refusing Codec Reference Implementation

**C(7,48) improved instance — single faults repaired, multi-faults refused.**

This repository is the public reference implementation of the fault-refusing codec family (patent-pending, Monsters Ink LLC / Taylor Heller). It demonstrates the measured contract:

- Single-bit (and signed single) faults are uniquely repaired.
- Multi-fault patterns that are not uniquely decodable are **refused** (never silently miscorrected).
- The decoder proves its own limits (triple-alias / door gate) before sealing.

## Current Status (2026-11-08) — Residual-Honest

| Claim | Status |
|-------|--------|
| 48-node window (masks 3..97, 7-bit) | Measured |
| Signed singles uniquely decoded | 96/96 measured |
| Signed pairs decoded (0 collisions) | 4,512 measured |
| Triple-alias gate | 14,280 aliases = 2 × 7,140 doors measured |
| Multi-fault refuse on non-unique patterns | By construction (targets table) |
| Clean public API (`Codec`) | Added this pass |
| Full golden-vector suite beyond the stage-6 self-tests | Open (diagnostic `code_breaker.py` remains the exhaustive runner) |
| Hardware / RTL | Not in this repo (see related Viasat proposal materials; Class C) |

No claim is made of perfect coverage outside the measured window or of production hardware readiness. This is a software reference + verification battery.

## Quick start

```bash
python3 -m venv .venv && . .venv/bin/activate
# stdlib only for core; numpy optional for spectrum stage

# Run the full measured battery + breaker self-tests
python3 code_breaker.py

# Or use the clean Codec API
python3 -c "
from codec import Codec
c = Codec()
print(c.summary())
outcome, detail = c.decode_syndrome(c.single_syndrome(0, +1))
print(outcome, detail)
"
```

## Files

| File | Role |
|------|------|
| `codec.py` | Clean, importable reference `Codec` class (H14 repair-or-refuse) |
| `code_breaker.py` | Full 6-stage diagnostic battery (doors, never-pairs, flow, zeros, breaker self-tests) |
| `README.md` | This status document |

## Measured battery (from `code_breaker.py` stage 6)

- All 96 signed singles decode uniquely.
- All 4,512 signed pairs decode with 0 refusals / 0 collisions inside the targets table.
- Triple gate: 14,280 measured aliases exactly equal 2 × number of doors; every aliasing triple completes a door relation.
- Contract: ≤2 spikes repaired when unique; non-unique patterns (including most triples) refuse.

Re-run any time with `python3 code_breaker.py`. All numbers printed by the script are measured in that process.

## Commercial / IP boundary

- This repository is a **reference implementation for evaluation**.
- Underlying technology is patent-pending (related filings include the fault-refusing codec family).
- The demonstration code may be inspected under the terms of the repository.
- **Commercial or production use requires a paid license.**

Landing: http://codec-reference-pack.netlify.app  
Square storefront: https://monsters-ink-107139.square.site  
Companion admission-control layer: https://github.com/snowphamtom/refuse

By Taylor Heller / Monsters Ink LLC
