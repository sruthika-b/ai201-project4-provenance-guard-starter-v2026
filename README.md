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

**Current submission path (`/appeal` is not implemented yet):**

1. A client sends JSON containing `text` and `creator_id` to `POST /submit`.
2. Flask parses the JSON body and the route extracts `text` and `creator_id`.
3. `detector.model_signal(text)` runs the local GPT-2 model and adds `model_score`, a 0–1 predictability-based AI-likelihood signal.
4. `stylometry.style_signal(text)` measures sentence lengths, vocabulary repetition, and punctuation; it adds `style_score` without interpreting the meaning.
5. `scoring.combine_signals(...)` combines both scores into one AI-likelihood score.
6. `scoring.score_to_label(...)` maps that score to a machine-readable guess and reader-facing sentence; the route creates a `content_id` for later reference.
7. `audit.log_decision(...)` records the scores and decision; Flask returns the content ID, scores, guess, confidence score, and label to the client.

`POST /submit` currently runs this path. `POST /appeal` still returns `501 not_implemented`.


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

**What it measures:** The style signal measures surface form: sentence-length variation, type-token ratio (unique words relative to total words), and punctuation density. The implementation converts each into a 0–1 AI like component and takes their equal weight mean. Low sentence length variation, repeated vocabulary, and low punctuation density push the score upward. This is a heuristic not a validated authorship test.

**Why that might differ between human and AI writing:** Generated prose can be more even in sentence length and reuse a narrower vocabulary; an individual human writer may produce more uneven rhythms and distinctive punctuation. These are tendencies, not authorship rules.

**What it can't see:** It cannot read meaning, judge who wrote the words, or distinguish genuine variation from edits that imitate variation. A quotation, deliberate typos, sentence splitting, genre conventions, or a very short text can move its measurements without changing authorship. Type-token ratio also changes with text length.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:**

Take a weighted average using the configured signal weights. Disagreement pulls the combined score between the two signals, but does not automatically mean `unsure`; the configured label thresholds decide the final label. This lets one signal temper the other without allowing disagreement alone to override the score.

**The numbers:**

With `WEIGHT_MODEL_SIGNAL = 0.5` and `WEIGHT_STYLE_SIGNAL = 0.5` in `config.py`, `combined_score = (0.5 * model_score + 0.5 * style_score) / (0.5 + 0.5)`. The weights currently give each signal equal influence; they should be calibrated against real writing before being treated as validated.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
For the mixed-style paragraph, `model_score = 0.8456` and `style_score = 0.5718`, so the equal-weight average is `0.7087`. Since that exceeds the current `AI_THRESHOLD = 0.65`, the label is high-confidence AI, even though the style signal is less AI-like. The average tempers the model score, but not enough to change its label in this example; that is a remaining false-positive risk to evaluate.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | `0.00 <= score <= 0.35` | We think this was probably written by a person. |
| unsure | `0.35 < score < 0.65` | We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it. |
| high-confidence AI | `0.65 <= score <= 1.00` | This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review. |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It says plainly that the system cannot tell and that a score is not evidence of authorship. The writer should not have to infer that uncertainty from a number.

---

## False-positive trace
Consider a real writer who uses short, ordinary sentences. For an illustrative score path, suppose their text gets `model_score = 0.92` and `style_score = 0.50`. The combined score is `(0.92 + 0.50) / 2 = 0.71`, above the current `0.65` AI threshold. These scores illustrate how a false positive could occur; they are not a measured model run.

The service would return `guess: "ai"` and the high-confidence-AI wording above. That is a serious false positive: the score describes how the signals reacted to the text, not who wrote it. The writer can send `POST /appeal` with the returned `content_id` and a reason. The intended endpoint appends an appeal to the audit log and marks the item `under_review`; it does not rerun the detector, erase the original score, or itself decide the appeal. A human review step is still needed. `/submit` is implemented; `/appeal` still returns `501` and is not yet available.

## Endpoint contracts
These are the target contracts for the two routes students build. Both accept and return JSON. A successful submission is `200`; malformed requests are `400`; a text exceeding the detector's 400-token scoring limit should be rejected as `413` rather than silently giving the style signal a longer text than the model signal sees. If rate limiting is enabled, a rejected request is `429`. The implementation must keep this behavior aligned with the detector, which currently truncates at 400 tokens.

Every error response has two string fields: `error` is the stable code below, and `message` is a human-readable explanation.

| HTTP status | `error` | When |
|---|---|---|
| 400 | `invalid_request` | Invalid JSON or missing, wrongly typed, blank, or unscorable fields. |
| 404 | `content_not_found` | The appeal refers to no recorded decision. |
| 409 | `appeal_exists` | The decision already has an appeal. |
| 413 | `text_too_long` | Submission text exceeds the agreed scoring limit. |
| 429 | `rate_limited` | The configured request limit was reached. |
| 503 | `detector_unavailable` | The local model cannot be loaded. |

#### `POST /submit`

Request fields:

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `text` | string | yes | Non-empty submitted writing; must contain enough tokens for the detector (at least three), and must fit within its 400-token scoring limit. |
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

#### `POST /appeal`

Request fields:

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `content_id` | string | yes | ID returned by a successful `/submit`; must refer to an existing decision. |
| `reasoning` | string | yes | The writer's explanation of why the decision should be reviewed; must not be blank. |

The service looks up the original `creator_id` from the audit entry, so the caller does not need to resupply it. On success return `200` with `content_id`, `status: "under_review"`, and a clear acknowledgement that the appeal was recorded, not resolved. Return `400` for malformed or missing fields, `404` for an unknown content ID, and `409` if that item already has an appeal. `audit.log_appeal` appends an event; it must not overwrite the original decision.

This gives a client the fields, score semantics, success states, and failure cases needed to build against the routes. The main implementation check still open is enforcing the same 400-token boundary for both signals.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**
Request:
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test submission with several words.", "creator_id": "sruthi"}'

Response:
{
  "confidence": 0.0,
  "content_id": "48fb7d38-3e92-4aa6-939b-79521e1fbf70",
  "guess": "...",
  "label": "...",
  "model_score": 0.1027,
  "style_score": 0.0
}

Log entry: audit.jsonl
{
  "count": 2,
  "entries": [
    {
      "combined_score": null,
      "content_id": "48fb7d38-3e92-4aa6-939b-79521e1fbf70",
      "creator_id": "sruthi",
      "guess": "...",
      "label": "...",
      "model_score": 0.1027,
      "status": "decided",
      "style_score": 0.0,
      "timestamp": "2026-11-03T16:19:53+00:00"
    },
    {
      "combined_score": null,
      "content_id": "8ef1a1ec-c935-4057-bd1c-6e6b30a0f496",
      "creator_id": "sruthi_sample",
      "guess": "...",
      "label": "...",
      "model_score": 0.3622,
      "status": "decided",
      "style_score": 0.0,
      "timestamp": "2026-11-03T16:22:57+00:00"
    }
  ]
}

Example runs after including the stylometry metrics:
Case 1: Written by human - works well
(.venv) sruthi@Sruthikas-MacBook-Air ai201-project4-provenance-guard-starter-v2026 % python stylometry.py "Heylo, this is Sruthi. I'm testing the stylometry metrics here. Today is a good day and the weather is quite nice. I have been doing my assignment since morning and I have been making good progress as well"
4 sentences, 38 words

sentence_length_spread   0.6107682521238319
type_token_ratio         0.7894736842105263
punctuation_density      0.024390243902439025
style_signal             0.5928729962078677   (higher = more likely AI)

All zeros? These are stubs — Milestone 4 is where you build them.
(.venv) sruthi@Sruthikas-MacBook-Air ai201-project4-provenance-guard-starter-v2026 % python detector.py "Hi, this is Sruthi. I'm having a pleasant day, and therefore writing a journal entry. The day has been calm and productive, giving me time to appreciate simple moments and reflect on what I hope to accomplish next."                                                                       
Loading gpt2 (first run downloads ~550 MB)…
`loss_type=None` was set in the config but it is unrecognized. Using the default loss: `ForCausalLMLoss`.
perplexity     37.8
model_signal   0.5690   (higher = more likely AI)
(.venv) sruthi@Sruthikas-MacBook-Air ai201-project4-provenance-guard-starter-v2026 % python stylometry.py
3 sentences, 22 words

sentence_length_spread   0.39364791081110845
type_token_ratio         0.9090909090909091
punctuation_density      0.022556390977443608
style_signal             0.5276288429107557   (higher = more likely AI)

All zeros? These are stubs — Milestone 4 is where you build them.

Case 2: Written by AI - In this case, the model's response and our response is not really aligned.
(.venv) sruthi@Sruthikas-MacBook-Air ai201-project4-provenance-guard-starter-v2026 % python stylometry.py "I started the morning with a cup of tea and a short walk around the neighborhood. The air felt cool, and the streets were quiet. When I got home, I made a list of the tasks I wanted to finish before dinner, then began with the easiest one."
3 sentences, 48 words

sentence_length_spread   0.4375
type_token_ratio         0.7291666666666666
punctuation_density      0.02510460251046025
style_signal             0.5718131607139249   (higher = more likely AI)

All zeros? These are stubs — Milestone 4 is where you build them.
(.venv) sruthi@Sruthikas-MacBook-Air ai201-project4-provenance-guard-starter-v2026 % python detector.
py "I started the morning with a cup of tea and a short walk around the neighborhood. The air felt cool, and the streets were quiet. When I got home, I made a list of the tasks I wanted to finish before dinner, then began with the easiest one."
Loading gpt2 (first run downloads ~550 MB)…
`loss_type=None` was set in the config but it is unrecognized. Using the default loss: `ForCausalLMLoss`.
perplexity     15.5
model_signal   0.8456   (higher = more likely AI)

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

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
