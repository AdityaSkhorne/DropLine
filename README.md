# DropLine

A concise, code-free GitHub repo blueprint for DropLine: a decentralized, offline-first chat and file-sharing app that uses Bluetooth, Wi‑Fi Direct, and the internet (only when available).

---

## One-line pitch

DropLine: private, peer-to-peer messaging and file transfer that works without the internet.

---

## Repo purpose

This repository is a clear, contribution-ready home for DropLine’s documentation, design decisions, and project governance. It is intentionally code-free: focus is on product scope, architecture, protocols (specification only), security, and community processes so developers can implement from a well-defined spec.

---

## Top-level structure

* README.md — project overview, quick start (conceptual), and roadmap
* LICENSE — MIT or chosen license
* CONTRIBUTING.md — how to contribute, coding standards, review process
* CODE_OF_CONDUCT.md — contributor guidelines
* /docs — design and operational docs (protocol, architecture, security checklist, UX flows)
* /design — wireframes, user journeys, onboarding copy, and app-store text
* /.github — issue and pull-request templates, community settings
* /roadmap — short- and long-term milestones and release plan
* /assets — logos, icons, illustrations, mockups

---

## README (what to include)

Keep README short and actionable. Include:

* Project tagline and short description (1–2 lines)
* Key features (bullet list)
* Primary use-cases (who benefits and why)
* High-level architecture summary (transport, discovery, crypto, storage, transfer engine) — conceptual only
* Quick conceptual "how to run a local dev test" checklist (devices needed, permissions to expect) — no code
* Where to find detailed docs (link to /docs)
* Roadmap summary and how to help (link to CONTRIBUTING)

---

## Docs (what belongs in /docs)

Organize docs into focused files:

* architecture.md — modules, responsibilities, and transport selection strategy
* protocol-spec.md — JSON message envelope, versioning rules, message types, and file-transfer lifecycle (meta, chunking, resume) expressed in plain language and examples (no code)
* security-privacy.md — crypto primitives to use (named, not implemented), key management, verification UX, threat model, and opt-in telemetry policy
* ux-onboarding.md — concise onboarding flows, verification options (QR, fingerprint), and permission rationale for users
* testing-plan.md — scenarios, devices, and acceptance criteria
* release-plan.md — milestones, alpha/beta criteria, and release checklist

---

## CONTRIBUTING.md and community

Make contributing frictionless:

* Clear issue labels and templates for bugs, features, and docs
* Branch naming and commit message guideline
* PR checklist (builds, tests, changelog, screenshots where applicable)
* Code review expectations and merge policy
* How to run tests and manual acceptance checks (conceptual)

---

## Security & privacy checklist (short)

* End-to-end encryption default for all messages and files
* Device-only private keys (use platform keystore/keychain)
* Human-verifiable key exchange (QR, fingerprints), described in docs
* Minimal, opt-in telemetry only; no message content leaves devices
* Secure default storage (encrypted at rest) and clear TTL options for ephemeral messages

---

## Roadmap (concise)

* MVP: offline discovery + encrypted text messaging + resumable file transfer
* Phase 2: polished onboarding, group chats, cross-transport continuity
* Phase 3: optional relay/WebRTC bridging, offline mesh enhancements, audits

---

## Governance & license

* Recommend MIT for easy contributions; note any trademark or logo rules in /assets
* Community governance: small core team + contributors, maintainers listed in README


