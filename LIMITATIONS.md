Known limitations and cautions

There is no published third-party audit. Do not assume the code is free of vulnerabilities.

The project runs on Python; platform-level guarantees for secure memory wiping are limited (garbage collection, swap, core dumps).

RAM-only operation reduces disk artifacts but cannot absolutely prevent memory remnants (OS-dependent).

Tor/peer-to-peer integration reduces metadata risk but may leak if misconfigured.

Ephemeral messages mean data is lost on crash; this is intentional but can cause accidental loss.

Use at your own risk; the author is not responsible for third-party misuse.

Remove or avoid defaults that could help criminals (bootstrap servers, pre-filled invites).

First-run warning in app should display: "Use only for lawful purposes; the developers are not liable."
