# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

<!-- Your criterion. It must name a number. -->

Across each of three evaluation trials, at most 1 of 10 pieces I wrote myself is labeled high-confidence AI.


**Why this target:**

I allow a small number of false positives because detector signals are imperfect, but a wrong AI accusation has a real cost for the writer. The limit must hold in every trial, not just on average.


---

## 2.

<!-- Your criterion. -->

In each of three trials, the calibration set produces at least one `human`, one `unsure`, and one `ai` label.


**Why this target:**

All three outcomes need to be reachable for the service to communicate both its conclusions and its uncertainty; a label that never appears is not useful.


---

## 3.

<!-- Your criterion. -->

For 3 appeals submitted against 3 valid content IDs, all 3 requests return HTTP 200 with status `under_review`, and each creates an appeal entry in the audit log while preserving the original decision entry.


**Why this target:**

Writers need a dependable way to challenge a wrong result. Checking both the response and append-only log confirms the appeal was recorded without erasing what the system originally decided.


---

## 4.

<!-- Your criterion. -->

In each of three trials, the median combined score for 5 clearly AI-written samples is at least 0.20 higher than the median combined score for 5 clearly human-written samples.


**Why this target:**

The signals should separate clear examples on average, but they will not perfectly identify every author. A 0.20 gap is large enough to be useful while allowing overlap between individual texts.


---

## 5.

<!-- Your criterion. -->

For each of 4 invalid submissions (missing `text`, empty `text`, `null` text, and text over the scoring limit), the service returns the documented `400` or `413` response and records a rejection instead of returning a `5xx` error.


**Why this target:**

Malformed input should not crash the service or disappear without a trace. Testing four distinct cases makes the expected behavior concrete and helps diagnose failures.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
