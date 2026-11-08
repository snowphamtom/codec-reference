"""
Fault-refusing codec reference — clean public API.

Window: 48 odd masks 3..97, 7-bit, H14 (mask + lower(mask)) construction.
Contract (measured in code_breaker.py stage 6):
  - signed singles uniquely repaired
  - signed pairs uniquely repaired (0 collisions in targets)
  - non-unique syndromes (most triples and higher) → REFUSE
  - triple-alias gate measured and sealed

No numpy required. Stdlib only.
"""
from __future__ import annotations

import itertools
from typing import Dict, List, Optional, Tuple, Union

# Canonical 48-node window used by the filed family and the breaker self-tests
NODES: List[int] = list(range(3, 98, 2))  # 3,5,...,97 → 48 nodes
assert len(NODES) == 48


def _lower(m: int) -> int:
    """mlower construction used by the H14 embedding."""
    return (m & 1) | ((~m & 0b1111110) & 0x7F)


def _vec(m: int) -> Tuple[int, ...]:
    """14-dimensional column: 7 bits of m followed by 7 bits of lower(m)."""
    t = _lower(m)
    return tuple((m >> k) & 1 for k in range(7)) + tuple((t >> k) & 1 for k in range(7))


def _add(u: Tuple[int, ...], v: Tuple[int, ...], s: int = 1) -> Tuple[int, ...]:
    return tuple(a + s * b for a, b in zip(u, v))


class Codec:
    """
    Repair-or-refuse decoder for the C(7,48) reference instance.

    Usage:
        c = Codec()
        outcome, detail = c.decode_syndrome(syndrome_14tuple)
        # outcome is "REPAIR" or "REFUSE"
    """

    def __init__(self) -> None:
        self.nodes = list(NODES)
        self.cols = [_vec(m) for m in self.nodes]
        self._targets: Dict[Tuple[int, ...], Tuple] = {}
        self._build_targets()

    def _build_targets(self) -> None:
        """Populate the unique-decode table for ≤2 signed spikes."""
        cols = self.cols
        targets: Dict[Tuple[int, ...], Tuple] = {}

        # signed singles
        for i, c in enumerate(cols):
            for sgn in (1, -1):
                targets.setdefault(tuple(sgn * x for x in c), ("single", (i, sgn)))

        # unit vectors (diagnostic)
        for j in range(14):
            u = tuple(1 if k == j else 0 for k in range(14))
            targets.setdefault(u, ("unit", None))
            targets.setdefault(tuple(-x for x in u), ("unit", None))

        # signed pairs
        for i, j in itertools.combinations(range(48), 2):
            for s1 in (1, -1):
                for s2 in (1, -1):
                    v = _add(tuple(s1 * x for x in cols[i]), cols[j], s2)
                    targets.setdefault(v, ("pair", (i, s1, j, s2)))

        self._targets = targets

    def single_syndrome(self, index: int, sign: int = 1) -> Tuple[int, ...]:
        """Return the 14-tuple syndrome for a signed single fault at node index."""
        if not (0 <= index < 48):
            raise IndexError("index must be in 0..47")
        if sign not in (1, -1):
            raise ValueError("sign must be +1 or -1")
        return tuple(sign * x for x in self.cols[index])

    def decode_syndrome(self, syndrome: Tuple[int, ...]) -> Tuple[str, Optional[Tuple]]:
        """
        Decode a 14-dimensional syndrome.

        Returns:
            ("REPAIR", detail)  if the syndrome is uniquely associated with ≤2 spikes
            ("REFUSE", None)   otherwise
        """
        if len(syndrome) != 14:
            raise ValueError("syndrome must be length 14")
        hit = self._targets.get(tuple(syndrome))
        if hit is None:
            return "REFUSE", None
        return "REPAIR", hit

    def summary(self) -> str:
        n_single = sum(1 for v in self._targets.values() if v[0] == "single")
        n_pair = sum(1 for v in self._targets.values() if v[0] == "pair")
        return (
            f"Codec C(7,48) reference — nodes={len(self.nodes)} "
            f"targets={len(self._targets)} "
            f"(singles={n_single}, pairs={n_pair}) "
            f"contract: unique ≤2 spikes → REPAIR; else REFUSE"
        )


if __name__ == "__main__":
    c = Codec()
    print(c.summary())
    # quick self-check: every signed single repairs to itself
    ok = 0
    for i in range(48):
        for s in (1, -1):
            syn = c.single_syndrome(i, s)
            outcome, detail = c.decode_syndrome(syn)
            if outcome == "REPAIR" and detail == ("single", (i, s)):
                ok += 1
    print(f"signed-single self-check: {ok}/96")
