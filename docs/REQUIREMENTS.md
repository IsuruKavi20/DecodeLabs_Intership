FR1: Accept a password string as input
FR2: Check password length (PDF says: <8 chars = immediate fail)
FR3: Check for presence of uppercase letters
FR4: Check for presence of digits
FR5: Check for presence of symbols
FR6: Classify result into Weak / Medium / Strong
FR7: Display the result to the user

Non-Functional Requirements (from the theory slides):

NFR1: Validation must run in O(n) time — single pass, no nested loops
NFR2: Use Pythonic idioms (any(), built-ins) over manual loops, for performance
(Stretch, mentioned in conclusion) NFR3: Optionally check against a list of common/leaked passwords

## Extended Scope (v2 — post-research)

Based on NIST SP 800-63B and zxcvbn design principles, scope was extended beyond the base PDF spec:

- Common/leaked password detection
- Sequential/repeated character pattern detection
- Length-weighted scoring (length prioritized over character variety)
- Simplified entropy estimate (character pool size ^ length)

## v3 (implemented)

- Two hard gates (length < 8, common/blocklist hit) return "Weak" before scoring.
- Length bonus tiers: 8-11 = +1, 12-15 = +2, 16-19 = +3, 20+ = +4.
  (20+ tier added so a long all-lowercase passphrase can reach "Strong".)
- +1 each for uppercase / digit / symbol; -2 for a weak pattern.
- Classification: score <= 2 Weak, == 3 Medium, >= 4 Strong.
- Diversity guard: a password shorter than 16 chars needs 2+ character classes
  to rate Strong; 16+ char passphrases are exempt (NIST length trade-off).
- Blocklist matching also reverses leetspeak (@031$7 -> aoeist) before lookup.
- Pattern detection extended: descending sequences + keyboard-walk substrings.
- Optional opt-in online check against Have I Been Pwned (k-anonymity range API).
- Entropy-bits estimate was dropped: raw entropy is a poor guessability
  predictor (see zxcvbn); threshold scoring + pattern detection used instead.
