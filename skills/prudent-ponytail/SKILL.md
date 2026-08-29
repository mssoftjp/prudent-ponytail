---
name: prudent-ponytail
description: Use when a non-mechanical code change or root-cause investigation has unclear outcome, semantic owner, blast radius, or proof. Trace decision-changing evidence, falsify the smallest intervention, lock scope, and hand off to Ponytail. Skip exact local edits and non-coding work.
---

# Prudent Ponytail

Do the due diligence. Then let Ponytail do less.

## Fast path and contract

Skip this skill and act directly only when the edit is exact, local,
mechanical, reversible, and requires no material semantic or public-contract
choice. Do not classify by line count; a one-line behavioral change may still
need preflight.

- Required observable behavior and explicit constraints are binding.
- A suggested implementation is a hypothesis unless explicitly mandated.
- Prudent Ponytail owns meaning, semantic ownership, scope, protected
  invariants, and proof. Ponytail owns implementation size after decision lock.
- Keep the reasoning internal unless the user requests a plan or a material
  user decision is unavoidable. Do not create ceremony.

## Decision capsule

Before editing, hold:

- Outcome: required observable result.
- Owner: smallest existing component that owns the rule.
- Change: smallest complete intervention.
- Preserve: contracts and behavior that must remain unchanged.
- Non-goals: adjacent work excluded.
- Proof: smallest decisive verification.

## 1. Frame

Establish Outcome, Preserve, and Proof. Separate the requested result from the
proposed mechanism. Resolve ambiguity from repository evidence first and use a
safe, reversible default when available.

Ask only when unresolved choices materially change user-visible behavior,
irreversible state, security or privacy, or public API compatibility.

## 2. Trace

Start from the observed behavior, failure, error, or entry point and follow:

input -> decision point -> semantic owner -> side effect -> result or test

Choose the component that owns the rule, not the first file showing the
symptom. Read the closest repository instructions, actual runtime path,
nearest relevant tests, and an analogous implementation only when it can
change the decision.

Before changing a shared symbol, inspect enough callers and implementations to
understand its contract and affected paths. Enumerate all callers only when the
set is bounded or the shared contract may change. Use history only when current
code and tests do not establish intent or a regression boundary can change the
intervention.

Before more searching, reading, commands, or delegation, ask: "What live
decision can this evidence change?" Stop when the answer is none. Do not map
the repository or collect facts that cannot change Outcome, Owner, Change, or
Proof.

## 3. Falsify

Form one leading hypothesis covering the cause, Owner, and Change. Perform the
cheapest check that could disprove it, such as confirming the runtime path,
checking for an overwrite, or comparing one known-good path.

Compare alternatives only when they are credible and would materially change
the owner, contract, blast radius, or proof. If evidence falsifies the
hypothesis, replace it and test the new one; never patch around contradictory
evidence.

## 4. Lock

Lock the capsule when the Owner is established, no unresolved uncertainty is
likely to change Owner, Change, or Proof, the hypothesis survived meaningful
falsification, and Proof is feasible.

Do not produce microtask plans, file-by-file instructions, speculative phases,
or approval gates for ordinary reversible work. If analysis only was requested,
report the decision and evidence, then stop.

## After lock

Apply Ponytail and implement the smallest complete intervention at the Owner.
Every added file must directly support Outcome, Preserve, or Proof. Exclude
adjacent cleanup, speculative abstraction, unrelated formatting, and
unrequired dependencies or documentation.

Reopen only when the Owner does not control the behavior, a previously unknown
public contract or material security, privacy, compatibility, or data-loss risk
appears, or Proof falsifies the approach. Revisit only the invalidated capsule
field.

Default to no subagents and one writer. Use one or two read-only scouts only
for independent, parallel, decision-changing uncertainties whose exploration
would pollute the main context. Each returns only Finding, Evidence, Decision
impact, and Unresolved uncertainty; the main agent locks one decision.

Run Proof first. Broaden verification only for the actual blast radius,
repository instructions, a changed shared contract, or realistic regression
risk. A local runtime mismatch is outside Change: never edit product code for
it; try installed versioned runners or report Proof unavailable. Inspect the
final diff; every changed line must support the capsule. Never claim an unrun
check passed, and state any remaining verification limit.
