# Password Strength Checker

A command-line tool that rates a password as **Weak**, **Medium**, or **Strong**
and explains *why*, so the user gets actionable feedback instead of just a label.

This is "Project 1" of a cybersecurity internship track. The design deliberately
follows modern guidance (NIST SP 800-63B) rather than the older "must contain an
uppercase, a number and a symbol" rules.

## What it does

1. **Gates** the password (instant *Weak*, no scoring) if it is too short or
   already known-bad:
   - shorter than 8 characters, or
   - found in a local list of ~100k common/leaked passwords
     (`data/common_passwords.txt`), including after undoing trailing digits/
     symbols and common leetspeak (`P@ssw0rd123!` &rarr; `password`), or
   - *(optional, opt-in)* found in the online
     [Have I Been Pwned](https://haveibeenpwned.com/Passwords) breach corpus.
2. **Scores** everything that passes the gates:

   | Check | Effect |
   |---|---|
   | Length 8&ndash;11 / 12&ndash;15 / 16&ndash;19 / 20+ | +1 / +2 / +3 / +4 |
   | Contains an uppercase letter | +1 |
   | Contains a digit | +1 |
   | Contains a symbol | +1 |
   | Contains a predictable pattern (ascending/descending run, repeated char, keyboard walk) | &minus;2 |

3. **Classifies** the final score: `&le; 2` &rarr; Weak, `3` &rarr; Medium,
   `&ge; 4` &rarr; Strong.
   A password shorter than 16 characters cannot reach *Strong* on length alone;
   it needs genuine character variety. A 16+ character passphrase **can** be
   Strong while being all lowercase &mdash; length is doing the work, which is
   exactly the trade-off NIST endorses.

## Install & run

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements-dev.txt   # only needed to run the tests
```

The tool itself has **no runtime dependencies** &ndash; it uses the Python
standard library only.

Run it from the repository root:

```bash
python -m src.main
```

You will be asked once whether to enable the online breach check, then prompted
for passwords in a loop. Input is hidden (via `getpass`). Type `exit` to quit.

Run the tests:

```bash
python -m pytest              # unit tests (no network)
python -m pytest -m network   # also hit the real HIBP API
```

## Design rationale

**Why gates on length + a blocklist, instead of mandatory character classes?**

- **NIST SP 800-63B &sect;5.1.1.2** removed composition rules (forced mixes of
  character types) from its recommendations. It instead requires a minimum
  length and screening every new password against a list of commonly-used,
  expected, or compromised values. Length and "is it already known" are the
  properties that actually predict how hard a password is to guess.
- **Carnegie Mellon / Lorrie Cranor's research** on password-composition
  policies found that requiring multiple character classes delivers minimal
  security benefit: users satisfy the rule in predictable ways
  (`password` &rarr; `Password1!`), which *shrinks* the effective search space
  an attacker must cover, while making passwords harder to remember.

So character classes here are a small bonus, not a gate, and length is weighted
most heavily.

**Pattern detection** (`src/patterns.py`) is a simplified, zxcvbn-style
heuristic: it catches ascending/descending sequences, repeated characters, and a
fixed set of keyboard rows/columns (substring match, forward and reversed). It is
not a full keyboard-adjacency graph or a guess-count estimator &ndash; that is
overkill for this project.

**Optional online breach check** (`src/hibp.py`) uses the Have I Been Pwned
*range* API with the **k-anonymity** model:

- the password is SHA-1 hashed locally;
- only the **first 5 hex characters** of that hash are sent to the API;
- the API returns every hash suffix sharing that prefix (hundreds of them) and
  the match is decided on our side.

The password and its full hash never leave the machine. The request also sends
`Add-Padding: true` so the response size does not leak whether there was a hit.
The check is **opt-in** and **fails open**: if the network is unavailable the
tool falls back to the local list and says so in the reasons.

## Future work

- **Personal-detail checks** &ndash; reject passwords containing the user's
  name, username, email, or date of birth.
- **Password history / reuse checks** &ndash; "you used this before". Deferred to
  Project 2 because it requires hashing (bcrypt/scrypt/Argon2) plus persistent
  storage, which is that project's scope per the internship roadmap.
- **Local mirror of the HIBP corpus** &ndash; download and index the full
  Pwned Passwords set so the breach check works offline and at full coverage.

## Known limitations

- The bundled blocklist is ~100k entries; the full breach corpus is ~850M+.
  The optional online check closes that gap but needs network access.
- Leetspeak reversal covers only six common substitutions
  (`@031$7` &rarr; `aoeist`).
- Keyboard-walk detection is a substring match against 8 known rows/columns, not
  a full adjacency graph, so novel walks are missed.
- Scoring is threshold-based, not an attack-cost model. A password like
  `Tr0ub4dor&3` rates *Strong* here because it clears the length and
  character-variety bars &ndash; pattern detection does not reverse leetspeak
  before looking for dictionary words.
