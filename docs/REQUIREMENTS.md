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