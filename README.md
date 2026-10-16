# Fault-Refusing Codec Reference Implementation

C(7,48) improved instance.

Single faults repaired. Multi-faults refused — never silent miscorrection on the measured model.

## Measured results

Built-in verification battery:
- Singles: 55/55
- All tested pairs refused (0 miscorrected)
- Sampled triples refused

## Quick start

```python
from final_codec import Codec
c = Codec()
parity, u = c.encode(payload)
outcome, detail = c.decode(v, t, u)
```

## Commercial path

Reference code for evaluation. Underlying technology patent-pending. Commercial or production use requires a paid license.

Landing page: http://codec-reference-pack.netlify.app

Square storefront: https://monsters-ink-107139.square.site

Companion residual admission layer: https://github.com/snowphamtom/refuse

By Taylor Heller / Monsters Ink LLC
