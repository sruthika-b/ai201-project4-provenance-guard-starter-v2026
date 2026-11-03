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
Both routes accept and return JSON. A successful `/submit` returns `200` with the decision fields. `/appeal` returns `200` when recorded, `400` for malformed or blank fields, `404` for an unknown content ID, and `409` for a duplicate appeal. Rate limiting is currently disabled. The detector truncates inputs to 400 tokens while stylometry measures the full text.

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

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
