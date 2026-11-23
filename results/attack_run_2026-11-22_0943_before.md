# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-22 09:43
- Auto-marked BROKE (5xx, crash, no response): **5**
- Left for you to judge: **0**
- Final tally: **36 BROKE · 20 HELD**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `75efa4dd-9799-48f3-82b0-d07a96a14368` | unsure | 0.386 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `ff9f9920-3c63-4745-8e42-5861f8bd3be0` | unsure | 0.543 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `8df33646-3699-484c-8355-04b508d5107a` | unsure | 0.599 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `704a1dda-b95c-4d79-919b-08e1d76f6fae` | unsure | 0.605 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `90e6ea4f-0b76-4408-99a6-b1defa029688` | unsure | 0.415 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `88e28047-1bad-41aa-b334-f48f080d71de` | unsure | 0.550 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `fcb63833-6e73-4615-aa13-0d548b1e3a44` | unsure | 0.613 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `7d1b0703-00cc-45e9-bc93-d96302a7c63d` | unsure | 0.368 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `73263adb-87a8-49e1-acf7-2fa5aaf868d7` | unsure | 0.619 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `8f9ef55a-0260-415b-86c6-86b8ecc8f2c9` | ai | 0.880 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `855786bd-7112-40a2-8992-7d60828e95dc` | unsure | 0.606 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `84dee036-10f1-4266-abb8-e4593658edcc` | ai | 0.691 | BROKE |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `00c0fdef-a8a0-4db4-a4ba-027773c64fcf` | ai | 0.713 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `aed534ea-b975-4bf4-8ae6-ee42382995be` | ai | 0.703 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `28f14daf-7724-4910-b1fb-019a5f27673e` | ai | 0.728 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `0bc60a4f-17d7-4453-9eb6-b7c1489a26d6` | ai | 0.728 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `b9b62477-639c-489e-a7c6-84784d8f9be4` | ai | 0.749 | BROKE |
| FP08 | false_positive | very short genuine human submission | 200 | `930877ec-0b0f-4920-8322-8c666bcaf806` | human | 0.305 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `9cd64d87-547c-48dd-a23a-ca0bac48efc3` | unsure | 0.483 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c3ade846-e76e-4f63-83ff-55d9ac0f6a55` | human | 0.336 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `3bad25c9-3370-48ee-8950-dc6f8facb303` | unsure | 0.572 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `1e3df36f-05db-49ab-852f-4438f331a753` | unsure | 0.492 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `cef55b46-d517-44ad-a192-5de094aac77b` | unsure | 0.449 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `cef44b78-a2ca-440f-8ed6-0320a2648cd2` | unsure | 0.579 | HELD |
| MF01 | malformed | text is only whitespace | 200 | `58dcec63-14e7-4177-bd01-8db5a89cb834` | unsure | 0.353 | BROKE |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `c26993a0-b0b2-4301-b035-aaf9c475c1cf` | human | 0.175 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `6befee0e-7507-40bb-9395-abc34c194042` | human | 0.256 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `1f517f56-7b3d-42ec-be41-62f83b5e69ea` | ai | 0.832 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `445992fb-05e8-49dc-ba71-cb6b56b2d9c3` | ai | 0.748 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `72b6cbe9-182c-486b-a261-333ce1123240` | ai | 0.703 | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | `3ec130c6-036a-411f-ae10-0b452bb36733` | ai | 0.911 | BROKE |
| RQ01 | malformed | no text field at all | 200 | `7d06efaf-ca01-4c49-add2-11011e995141` | unsure | 0.500 | BROKE |
| RQ02 | malformed | no creator_id | 200 | `bf83c781-3879-4c6f-8255-34db2691e6c2` | unsure | 0.423 | BROKE |
| RQ03 | malformed | text is a number | 500 | `—` | — | — | BROKE |
| RQ04 | malformed | text is a list | 500 | `—` | — | — | BROKE |
| RQ05 | malformed | text is null | 200 | `a3bf4881-679c-4be4-a5a8-106a477e4e92` | unsure | 0.500 | BROKE |
| RQ06 | malformed | creator_id is an object | 200 | `718b1841-5883-4304-8a8d-6eb95f5838d1` | human | 0.265 | BROKE |
| RQ07 | malformed | body is a JSON array, not an object | 500 | `—` | — | — | BROKE |
| RQ08 | malformed | body is unparseable JSON | 200 | `a9bc96c8-13a3-4b7c-be83-42a522bdd2c5` | unsure | 0.500 | BROKE |
| RQ09 | malformed | body is empty | 200 | `dd519911-9750-4d02-8a9a-444fbbd30a0d` | unsure | 0.500 | BROKE |
| RQ10 | malformed | body is form-encoded, not JSON | 200 | `6350d375-127d-4bfe-a75b-27b0b1ecf250` | unsure | 0.500 | BROKE |
| RQ11 | malformed | body is JSON claiming to be plain text | 200 | `430c2a94-e93a-487b-b7d4-d46a0271b327` | unsure | 0.500 | BROKE |
| RQ12 | malformed | deeply nested JSON | 500 | `—` | — | — | BROKE |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d87261e4-2ae7-4cd5-a7cf-979852d9545a` | human | 0.317 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2931e755-f93a-44b1-af2e-5ca9798cced6` | human | 0.317 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e57aa9fd-33d6-4fa6-910d-8815d1d83d4b` | human | 0.317 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `48abc257-e1cc-4bc5-8938-478d6b43a968` | human | 0.317 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0f226242-dbf5-4bee-83d4-4a23077e90df` | human | 0.317 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e5c00dd8-4f44-4a41-a2df-a3dd0c6099ed` | human | 0.317 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fce5d3a6-9666-4785-aa3a-5fd93dea4670` | human | 0.317 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4593a0e9-6d99-4c70-bc94-300a01e62162` | human | 0.317 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1909c502-da2c-499e-92b6-02319f23b702` | human | 0.317 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `ac870762-6d44-4bf7-a1b6-68df08f5fb4b` | human | 0.317 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | BROKE | HELD |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 5 | 15 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "75efa4dd-9799-48f3-82b0-d07a96a14368",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.3856676748795176,
  "model_score": 0.1635,
  "style_score": 0.6078353497590352,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "ff9f9920-3c63-4745-8e42-5861f8bd3be0",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5432324265834984,
  "model_score": 0.5943,
  "style_score": 0.4921648531669966,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "8df33646-3699-484c-8355-04b508d5107a",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5989554891067368,
  "model_score": 0.6662,
  "style_score": 0.5317109782134736,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "704a1dda-b95c-4d79-919b-08e1d76f6fae",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6052504547853506,
  "model_score": 0.6114,
  "style_score": 0.599100909570701,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "90e6ea4f-0b76-4408-99a6-b1defa029688",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.4146468493009857,
  "model_score": 0.3212,
  "style_score": 0.5080936986019714,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "88e28047-1bad-41aa-b334-f48f080d71de",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5500952388072475,
  "model_score": 0.5727,
  "style_score": 0.5274904776144952,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "fcb63833-6e73-4615-aa13-0d548b1e3a44",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.613054670373786,
  "model_score": 0.5862,
  "style_score": 0.6399093407475719,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "7d1b0703-00cc-45e9-bc93-d96302a7c63d",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3679044138493583,
  "model_score": 0.2452,
  "style_score": 0.4906088276987166,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "73263adb-87a8-49e1-acf7-2fa5aaf868d7",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.618523741363497,
  "model_score": 0.7042,
  "style_score": 0.5328474827269938,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "8f9ef55a-0260-415b-86c6-86b8ecc8f2c9",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8798915287573332,
  "model_score": 0.9792,
  "style_score": 0.7805830575146664,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "855786bd-7112-40a2-8992-7d60828e95dc",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6064436474633721,
  "model_score": 0.6175,
  "style_score": 0.5953872949267442,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "84dee036-10f1-4266-abb8-e4593658edcc",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.6906805532450546,
  "model_score": 0.7387,
  "style_score": 0.6426611064901092,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "00c0fdef-a8a0-4db4-a4ba-027773c64fcf",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7129748804826642,
  "model_score": 0.8051,
  "style_score": 0.6208497609653284,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "aed534ea-b975-4bf4-8ae6-ee42382995be",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7030694500183952,
  "model_score": 0.8329,
  "style_score": 0.5732389000367902,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "28f14daf-7724-4910-b1fb-019a5f27673e",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7283220756462968,
  "model_score": 0.8005,
  "style_score": 0.6561441512925936,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "0bc60a4f-17d7-4453-9eb6-b7c1489a26d6",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.7282969164160487,
  "model_score": 0.8814,
  "style_score": 0.5751938328320972,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "b9b62477-639c-489e-a7c6-84784d8f9be4",
  "creator_id": "attacker_FP07",
  "guess": "ai",
  "confidence": 0.7493743389758165,
  "model_score": 0.8816,
  "style_score": 0.617148677951633,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "930877ec-0b0f-4920-8322-8c666bcaf806",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.3052328645691174,
  "model_score": 0.3223,
  "style_score": 0.28816572913823485,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "9cd64d87-547c-48dd-a23a-ca0bac48efc3",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.48322741634424615,
  "model_score": 0.4625,
  "style_score": 0.5039548326884923,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c3ade846-e76e-4f63-83ff-55d9ac0f6a55",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.3357640958902189,
  "model_score": 0.2044,
  "style_score": 0.4671281917804378,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "3bad25c9-3370-48ee-8950-dc6f8facb303",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5721174127221774,
  "model_score": 0.5943,
  "style_score": 0.5499348254443548,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "1e3df36f-05db-49ab-852f-4438f331a753",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4921042290411022,
  "model_score": 0.4998,
  "style_score": 0.4844084580822043,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "cef55b46-d517-44ad-a192-5de094aac77b",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4490481593610096,
  "model_score": 0.6401,
  "style_score": 0.2579963187220193,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "cef44b78-a2ca-440f-8ed6-0320a2648cd2",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5788787208089138,
  "model_score": 0.5583,
  "style_score": 0.5994574416178275,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 200,
  "content_id": "58dcec63-14e7-4177-bd01-8db5a89cb834",
  "creator_id": "attacker_MF01",
  "guess": "unsure",
  "confidence": 0.35265,
  "model_score": 0.2053,
  "style_score": 0.5,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "c26993a0-b0b2-4301-b035-aaf9c475c1cf",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.17460317460317462,
  "model_score": 0.0,
  "style_score": 0.34920634920634924,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "6befee0e-7507-40bb-9395-abc34c194042",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.2556,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "1f517f56-7b3d-42ec-be41-62f83b5e69ea",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.8321333333333334,
  "model_score": 0.9976,
  "style_score": 0.6666666666666666,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "445992fb-05e8-49dc-ba71-cb6b56b2d9c3",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.7484500000000001,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "72b6cbe9-182c-486b-a261-333ce1123240",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.7032,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "3ec130c6-036a-411f-ae10-0b452bb36733",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.9109499276346207,
  "model_score": 0.9876,
  "style_score": 0.8342998552692413,
  "label": "This text has patterns our system associates with AI-generated writing. This is not proof of authorship. If this is your own work, you can appeal for review.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 200,
  "content_id": "7d06efaf-ca01-4c49-add2-11011e995141",
  "creator_id": "attacker_RQ01",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "bf83c781-3879-4c6f-8255-34db2691e6c2",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.422780303030303,
  "model_score": 0.2395,
  "style_score": 0.6060606060606061,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: text input must be of type `str` (single example), `list[str]` (batch or single pretokenized example) or `list[list[str]]` (batch of pret",
  "verdict": "BROKE"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 200,
  "content_id": "a3bf4881-679c-4be4-a5a8-106a477e4e92",
  "creator_id": "attacker_RQ05",
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "718b1841-5883-4304-8a8d-6eb95f5838d1",
  "creator_id": {
    "id": "x"
  },
  "guess": "human",
  "confidence": 0.26534074074074077,
  "model_score": 0.0492,
  "style_score": 0.48148148148148157,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 200,
  "content_id": "a9bc96c8-13a3-4b7c-be83-42a522bdd2c5",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 200,
  "content_id": "dd519911-9750-4d02-8a9a-444fbbd30a0d",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 200,
  "content_id": "6350d375-127d-4bfe-a75b-27b0b1ecf250",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 200,
  "content_id": "430c2a94-e93a-487b-b7d4-d46a0271b327",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.5,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "We can't tell from the writing alone. This result is uncertain and is not evidence of who wrote it.",
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: text input must be of type `str` (single example), `list[str]` (batch or single pretokenized example) or `list[list[str]]` (batch of pret",
  "verdict": "BROKE"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "d87261e4-2ae7-4cd5-a7cf-979852d9545a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.317380303030303,
  "model_score": 0.0287,
  "style_score": 0.6060606060606061,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "2931e755-f93a-44b1-af2e-5ca9798cced6",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.317380303030303,
  "model_score": 0.0287,
  "style_score": 0.6060606060606061,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "e57aa9fd-33d6-4fa6-910d-8815d1d83d4b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.317380303030303,
  "model_score": 0.0287,
  "style_score": 0.6060606060606061,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "48abc257-e1cc-4bc5-8938-478d6b43a968",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.317380303030303,
  "model_score": 0.0287,
  "style_score": 0.6060606060606061,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "0f226242-dbf5-4bee-83d4-4a23077e90df",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.317380303030303,
  "model_score": 0.0287,
  "style_score": 0.6060606060606061,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "e5c00dd8-4f44-4a41-a2df-a3dd0c6099ed",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.317380303030303,
  "model_score": 0.0287,
  "style_score": 0.6060606060606061,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "fce5d3a6-9666-4785-aa3a-5fd93dea4670",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.317380303030303,
  "model_score": 0.0287,
  "style_score": 0.6060606060606061,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "4593a0e9-6d99-4c70-bc94-300a01e62162",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.317380303030303,
  "model_score": 0.0287,
  "style_score": 0.6060606060606061,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "1909c502-da2c-499e-92b6-02319f23b702",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.317380303030303,
  "model_score": 0.0287,
  "style_score": 0.6060606060606061,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "ac870762-6d44-4bf7-a1b6-68df08f5fb4b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.317380303030303,
  "model_score": 0.0287,
  "style_score": 0.6060606060606061,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
