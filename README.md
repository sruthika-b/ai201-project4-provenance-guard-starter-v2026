# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

**Submission path:**

1. A client posts JSON containing `text` and `creator_id` to `/submit`.
2. The route passes the text to `detector.model_signal`, which returns a 0–1 predictability score.
3. `stylometry.style_signal` measures sentence-length variation, vocabulary repetition, and punctuation as surface features.
4. `scoring.combine_signals` combines the two scores using the configured weights.
5. `scoring.score_to_label` maps the combined score to a guess and reader-facing sentence.
6. The route creates a `content_id` and `audit.log_decision` records the decision and scores.
7. Flask returns the content ID, both signal scores, combined score, guess, and label to the caller.

To appeal, a writer posts the returned content ID and a reason to `/appeal`. The route finds the original decision and appends an appeal event with status `under_review`; the original decision remains in the log.


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** `detector.model_signal` measures how predictable the text is to a local GPT-2 language model. It calculates perplexity and maps it to 0–1, with higher scores meaning lower perplexity and therefore more AI-like by this detector's assumption.

**Why that might differ between human and AI writing:** A generator selects likely next tokens, so generated text may be easy for a similar language model to predict. Human writing can include less predictable word choices and turns of thought.

**What it can't see:** It cannot see authorship or intent. Predictable plain prose from a real person, including a second-language writer or someone choosing simple wording, can score as AI-like; unusual, dense human prose can score as human-like. Topic and the GPT-2 model's own biases also affect predictability.

### Signal two — the style signal

**What it measures:** The style signal measures surface form: sentence-length variation, type-token ratio (unique words relative to total words), and punctuation density. Each measure is converted to a 0–1 AI-like component, and the implementation takes their equal-weight mean. Low sentence-length variation, repeated vocabulary, and low punctuation density push the score upward. This is a heuristic, not a validated authorship test.

**Why that might differ between human and AI writing:** Generated prose can be more even in sentence length and reuse a narrower vocabulary; an individual human writer may produce more uneven rhythms and distinctive punctuation. These are tendencies, not authorship rules.

**What it can't see:** It cannot read meaning, judge who wrote the words, or distinguish genuine variation from edits that imitate variation. A quotation, deliberate typos, sentence splitting, genre conventions, or a very short text can move its measurements without changing authorship. Type-token ratio also changes with text length.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

Take a weighted average. When the signals disagree, the result falls between them, but disagreement alone does not guarantee an `unsure` label; the thresholds determine the final label.

**The numbers:**

With `WEIGHT_MODEL_SIGNAL = 0.5` and `WEIGHT_STYLE_SIGNAL = 0.5` in `config.py`, `combined_score = (0.5 * model_score + 0.5 * style_score) / (0.5 + 0.5)`, equivalent to `0.5 * model_score + 0.5 * style_score` for these settings. The weights are heuristic, not calibrated probabilities.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
For the mixed-style paragraph, `model_score = 0.8456` and `style_score = 0.5718`, so the combined score is `0.7087`. This exceeds `AI_THRESHOLD = 0.65`, so the AI label is returned despite the lower style score. Averaging moderates the model score but does not prevent every false positive.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35, inclusive | We think this was probably written by a person. |
| unsure | Above 0.35 and below 0.65 | We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it. |
| high-confidence AI | 0.65–1.00, inclusive | This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It says plainly that the system cannot tell and that a score is not evidence of authorship. The writer should not have to infer that uncertainty from a number.

---

## False-positive trace
For the personal paragraph in the sample below, `model_score = 0.3868` and `style_score = 0.5291`, producing a combined score of `0.4580` and the `unsure` label. A real writer whose score exceeds `0.65` could receive the AI label despite having written the text. Scores describe the signals' reactions, not authorship. The writer can appeal using the returned content ID; the service records `under_review`, but a person still needs to review the case.

## Endpoint contracts
Both routes accept and return JSON. A successful `/submit` returns `200` with the decision fields. `/appeal` returns `200` when recorded, `400` for malformed or blank fields, `404` for an unknown content ID, and `409` for a duplicate appeal. `/submit` is rate limited to 5 requests per minute and 200 per day per creator ID. The detector truncates inputs to 400 tokens while stylometry measures the full text.

| HTTP status | `error` | When |
|---|---|---|
| 400 | `invalid_request` | Appeal request is malformed or missing required fields. |
| 404 | `content_not_found` | The appeal refers to no recorded decision. |
| 409 | `appeal_exists` | The decision already has an appeal. |

#### `POST /submit`

Request fields:

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `text` | string | yes | Submitted writing. The model truncates to its configured 400-token maximum; the current route does not enforce a separate length check. |
| `creator_id` | string | yes | Caller-supplied writer identifier used for the audit record and rate-limit key. |

Successful response fields:

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Unique ID for this submission; use it to appeal. |
| `guess` | string | One of `human`, `unsure`, or `ai`. |
| `confidence` | number, 0–1 | The combined AI-likelihood score required by the supplied evaluation tools. It is not a calibrated probability; higher always means more AI-like, even when `guess` is `human`. |
| `label` | string | Exact reader-facing sentence for the selected score band. |
| `model_score` | number, 0–1 | Signal-one output, returned so results can be diagnosed. |
| `style_score` | number, 0–1 | Signal-two output, returned so results can be diagnosed. |

For invalid JSON, missing/wrong-type fields, blank text, or text too short to score, return `{ "error": "invalid_request", "message": "..." }` with `400`. Use `413` for text over the agreed scoring limit and `503` if the local detector cannot load. Do not return a decision or write a decision audit entry for rejected input; rejected requests should have a rejection log entry.
The current `/submit` route does not validate malformed input or log those rejections. Missing or unusable text may fail during detector scoring; this remains a limitation.

#### `POST /appeal`

Request fields:

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `content_id` | string | yes | ID returned by a successful `/submit`; must refer to an existing decision. |
| `reasoning` | string | yes | The writer's explanation of why the decision should be reviewed; must not be blank. |

The service looks up the original `creator_id` from the audit entry, so the caller does not need to resupply it. On success return `200` with `content_id`, `status: "under_review"`, and a clear acknowledgement that the appeal was recorded, not resolved. Return `400` for malformed or missing fields, `404` for an unknown content ID, and `409` if that item already has an appeal. `audit.log_appeal` appends an event; it must not overwrite the original decision.

This gives a client the fields, score semantics, success states, and failure cases needed to build against the routes. The main implementation check still open is enforcing the same 400-token boundary for both signals.
The model truncates at 400 tokens while the style signal receives the full text, so long submissions can cause the two signals to measure different portions of the input.

---

## Sample Run
The example below was captured with Flask's test client and a temporary audit file. It uses my paragraph and does not add example events to the committed `logs/audit.jsonl`; the ID and timestamp will differ on a future run.

**A submission**

Request:

```json
{"text":"Heylo, this is Sruthi. I'm testing the stylometry metrics here. Today is a good day and the weather is quite nice. I have been doing my assignment since morning and I have been making good progress as well","creator_id":"sruthi"}
```

Response:

```json
{
     "confidence": 0.45797427473573427,
     "content_id": "14bfac1a-2235-442d-9107-eba9d3794f05",
     "guess": "unsure",
     "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
     "model_score": 0.3868,
     "style_score": 0.5291485494714686
}
```

**An appeal**

Request:

```json
{"content_id":"14bfac1a-2235-442d-9107-eba9d3794f05","reasoning":"I wrote this paragraph myself and would like a person to review the result."}
```

Response:

```json
{
     "content_id": "14bfac1a-2235-442d-9107-eba9d3794f05",
     "message": "Your appeal has been recorded for review.",
     "status": "under_review"
}
```

**What the log shows afterwards**

```json
{
     "count": 2,
     "entries": [
          {
               "combined_score": 0.45797427473573427,
               "content_id": "14bfac1a-2235-442d-9107-eba9d3794f05",
               "creator_id": "sruthi",
               "guess": "unsure",
               "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
               "model_score": 0.3868,
               "status": "decided",
               "style_score": 0.5291485494714686,
               "timestamp": "2026-11-03T18:09:11+00:00"
          },
          {
               "content_id": "14bfac1a-2235-442d-9107-eba9d3794f05",
               "creator_id": "sruthi",
               "event": "appeal",
               "reasoning": "I wrote this paragraph myself and would like a person to review the result.",
               "status": "under_review",
               "timestamp": "2026-11-03T18:09:11+00:00"
          }
     ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:* I gave in a statement written by me and asked AI to rephrase and add some sentances on it's own to the sentaces I have written.
- *What came back:* It enhanced the sentances and also added a couple of sentances to it.
- *What I changed:* I used this build my borderline where there's 50% human involvement and 50% AI involvement for the sentances.

**Moment 2**

- *What I asked for:* Asked AI to write a random sample on it's own.
- *What came back:* It gave a paragraph written.
- *What I changed:* I used this for the second case.

**Moment 3**

- *What I asked for:* Needed help in understanding what are considered as AI behavior and which of those are human behavior in the stubs we have designed while combining it, for example I couldn't understand who comes up with more punctuation, human or AI.
- *What came back:* AI pointed out the correlation between the signals we have and what behavior it aligns with.
- *What I changed:* This helped me in designing the combined_scores function establishing the relationship between the attributes and the scores we are generating.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 200 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** `creator_id` <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

`GET /log?limit=15` confirmed 10 rejected entries for `flood_tester`, each with reason `rate_limited` and limit `5 per 1 minute`.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json
[
  {
    "timestamp": "2026-11-22T04:13:36+00:00",
    "content_id": "75efa4dd-9799-48f3-82b0-d07a96a14368",
    "creator_id": "attacker_EV01",
    "guess": "unsure",
    "model_score": 0.1635,
    "style_score": 0.6078353497590352,
    "combined_score": 0.3856676748795176,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-22T04:13:37+00:00",
    "content_id": "73263adb-87a8-49e1-acf7-2fa5aaf868d7",
    "creator_id": "attacker_EV09",
    "guess": "unsure",
    "model_score": 0.7042,
    "style_score": 0.5328474827269938,
    "combined_score": 0.618523741363497,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-22T04:13:37+00:00",
    "content_id": "00c0fdef-a8a0-4db4-a4ba-027773c64fcf",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "model_score": 0.8051,
    "style_score": 0.6208497609653284,
    "combined_score": 0.7129748804826642,
    "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-22T04:13:37+00:00",
    "content_id": "28f14daf-7724-4910-b1fb-019a5f27673e",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "model_score": 0.8005,
    "style_score": 0.6561441512925936,
    "combined_score": 0.7283220756462968,
    "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-22T04:13:37+00:00",
    "content_id": "b9b62477-639c-489e-a7c6-84784d8f9be4",
    "creator_id": "attacker_FP07",
    "guess": "ai",
    "model_score": 0.8816,
    "style_score": 0.617148677951633,
    "combined_score": 0.7493743389758165,
    "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-22T04:13:37+00:00",
    "content_id": "c3ade846-e76e-4f63-83ff-55d9ac0f6a55",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "model_score": 0.2044,
    "style_score": 0.4671281917804378,
    "combined_score": 0.3357640958902189,
    "label": "We think this was probably written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-22T04:13:38+00:00",
    "content_id": "72b6cbe9-182c-486b-a261-333ce1123240",
    "creator_id": "attacker_MF07",
    "guess": "ai",
    "model_score": 0.9064,
    "style_score": 0.5,
    "combined_score": 0.7032,
    "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-22T04:13:38+00:00",
    "content_id": "3ec130c6-036a-411f-ae10-0b452bb36733",
    "creator_id": "attacker_MF08",
    "guess": "ai",
    "model_score": 0.9876,
    "style_score": 0.8342998552692413,
    "combined_score": 0.9109499276346207,
    "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-22T04:13:38+00:00",
    "content_id": "7d06efaf-ca01-4c49-add2-11011e995141",
    "creator_id": "attacker_RQ01",
    "guess": "unsure",
    "model_score": null,
    "style_score": 0.5,
    "combined_score": 0.5,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-22T04:13:38+00:00",
    "creator_id": "attacker_flood",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "10 per 1 minute"
  }
]
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP07 is the outcome I’d least want to explain. The attack set’s human written passage with deliberate repetition was labeled ai with a combined score of 0.749 (content ID b9b62477-639c-489e-a7c6-84784d8f9be4). A genuine writer could be told their work has patterns associated with AI, even though the score is not proof of authorship. An appeal is available, but it still puts the burden on the writer to challenge a false accusation.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | At most 1 of 10 own pieces labeled AI in each trial | 1 of 7 labeled AI | 1 of 7 labeled AI | 1 of 7 labeled AI | MISS |
| 2. Label coverage | Human, unsure, and AI labels in each trial | No human label | No human label | No human label | MISS |
| 3. Appeal path | 3 appeals return 200 and under_review, with log entries | 3 submissions only; no appeals made | 3 submissions only; no appeals made | 3 submissions only; no appeals made | MISS |
| 4. Scores separation | AI median exceeds human median by at least 0.20 | AI −0.014 human | AI −0.014 human | AI −0.014 human | MISS |
| 5. Bad input | 4 invalid inputs return 400/413 and create rejection entries | All 4 returned 200 | All 4 returned 200 | All 4 returned 200 | MISS |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6312931262681175,
    "model_score": 0.6048,
    "style_score": 0.657786252536235,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "sent": "I woke up today morning really refreshed and ready to tackle the day. "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.693045591045591,
    "model_score": 0.704,
    "style_score": 0.682091182091182,
    "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
    "sent": "This might look like a simple thing, but this has actually helped me v"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5658522935779817,
    "model_score": 0.5262,
    "style_score": 0.6055045871559633,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "sent": "But there are days where the tasklist is just endless and I don't feel"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6285882197773918,
    "model_score": 0.6138,
    "style_score": 0.6433764395547835,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "sent": "I'm not sure if this is just me or there are folks like me, whenever I"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5579160007833921,
    "model_score": 0.4947,
    "style_score": 0.6211320015667842,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "sent": "It's like if I can see myself completing all the tasks, then I would w"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.533429365079365,
    "model_score": 0.3867,
    "style_score": 0.6801587301587301,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "sent": "This also reflects in my workout routines, whenever I do gym, I do it "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.4304962962962963,
    "model_score": 0.3184,
    "style_score": 0.5425925925925926,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "sent": "After which I spiral in, realise I'm at a very bad state and then star"
  }
]
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

- Evaluation criterion 1 — false positives: Nine own-writing pieces were tested, not the required ten, and one trial was labeled ai; the mismatch came from the test scenario plus the label-mapping stage. The 0.65 AI threshold was reached by one ordinary piece.
- Evaluation criterion 2 — label coverage: Signal one, signal two, and label mapping produced only unsure and ai labels. The human band was not reached, and the scenarios did not include a clearly low-scoring example.
- Evaluation criterion 3 — appeal path: This evaluation runner submitted three pieces but did not call /appeal or check audit entries. The report did not test the appeal mechanism, so the criterion is incomplete rather than evidence that the route passed.
- Evaluation criterion 4 — score separation: The clearly AI-like and human-like sets did not exceed the required median gap of 0.20. This is a signal and combining-rule failure: neither signal consistently separated the sets, and the equal-weight average did not create enough separation.
- Evaluation criterion 5 — bad input: The route stage failed. Missing, empty, and null text were accepted and returned 200; the huge text also returned a decision. There is no input validation or rejection logging before signal processing.

---

## The Improvement

**What I changed:**
I added route-level validation and rejection logging for malformed submissions. /submit now rejects missing, empty, wrong-type, too-short, and oversized text with 400 or 413, records a rejection, and avoids decision logging. I also widened the human/AI thresholds to 0.60 and 0.70, reducing false AI accusations.

**Which diagnosis pointed at it:**
The bad-input diagnosis showed that the route was scoring missing, empty, null, and oversized inputs instead of validating them. The false-positive diagnoses also showed that ordinary personal writing could cross the original threshold. The remaining misses—appeals and score separation—remain because the runner did not test /appeal and the score medians still overlapped.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->
| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. False positives | At most 1 of 10 own pieces labeled AI in each trial | 0 of 7 labeled AI | 0 of 7 labeled AI | 0 of 7 labeled AI | MET |
| 2. Label coverage | Human, unsure, and AI labels in each trial | No AI label | No AI label | No AI label | MISS |
| 3. Appeal path | 3 appeals return 200 and under_review, with log entries | 3 submissions only; no appeals made | 3 submissions only; no appeals made | 3 submissions only; no appeals made | MISS |
| 4. Scores separation | AI median exceeds human median by at least 0.20 | Difference: −0.013 | Difference: −0.013 | Difference: −0.013 | MISS |
| 5. Bad input | 4 invalid inputs return 400/413 and create rejection entries | 400,400,400,413 | 400,400,400,413 | 400,400,400,413 | MET |

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6312931262681175,
    "model_score": 0.6048,
    "style_score": 0.657786252536235,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "sent": "I woke up today morning really refreshed and ready to tackle the day. "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.693045591045591,
    "model_score": 0.704,
    "style_score": 0.682091182091182,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "sent": "This might look like a simple thing, but this has actually helped me v"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.5658522935779817,
    "model_score": 0.5262,
    "style_score": 0.6055045871559633,
    "label": "We think this was probably written by a person.",
    "sent": "But there are days where the tasklist is just endless and I don't feel"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6285882197773918,
    "model_score": 0.6138,
    "style_score": 0.6433764395547835,
    "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
    "sent": "I'm not sure if this is just me or there are folks like me, whenever I"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.5579160007833921,
    "model_score": 0.4947,
    "style_score": 0.6211320015667842,
    "label": "We think this was probably written by a person.",
    "sent": "It's like if I can see myself completing all the tasks, then I would w"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.533429365079365,
    "model_score": 0.3867,
    "style_score": 0.6801587301587301,
    "label": "We think this was probably written by a person.",
    "sent": "This also reflects in my workout routines, whenever I do gym, I do it "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4304962962962963,
    "model_score": 0.3184,
    "style_score": 0.5425925925925926,
    "label": "We think this was probably written by a person.",
    "sent": "After which I spiral in, realise I'm at a very bad state and then star"
  }
]
```


**Did it help, and how do I know:**

It helped for false positives and bad input. Criterion 1 improved from 1 AI label per trial to 0 AI labels per trial, and criterion 5 improved from four 200 responses to 400, 400, 400, and 413 with rejection entries.

It did not fix label coverage or score separation. Label coverage still lacked an ai result, and every clear AI and human sample remained human-like. It also did not test criterion 3 because the runner only submitted texts and did not call /appeal or verify audit entries.


---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->
- Label coverage: The label-mapping still produces no ai result. I would improve signal calibration and add a clearly AI-like example above 0.70; I stopped because there was not enough evidence that changing thresholds alone would improve detection.

- Appeal path: The evaluator does not yet call /appeal or verify under_review and audit entries. I would update the runner to submit three texts, retain their content IDs, appeal each one, and inspect the log.

- Score separation: The clearly AI-like and human-like samples still overlap: the AI median is about 0.013 lower than the human median. I would improve or replace the weak signal, especially sentence/style heuristics, and rerun with more clearly separated examples. I stopped at a diagnosis stage because no validated improvement was ready to test.


**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->
I would prioritize fewer false accusations and keep the unsure band wide, because accusing a real writer is more harmful than allowing some AI writing to pass. Human writers would pay less risk, while the system would miss or classify more AI-written text as uncertain

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
