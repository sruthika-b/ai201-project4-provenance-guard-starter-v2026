"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # ⚠️ PUT YOUR OWN WRITING HERE. Not AI text, not a sample from the web —
        # things you actually wrote. This is the criterion that matters most and
        # it's meaningless with someone else's prose.
        "texts": [
            "I woke up today morning really refreshed and ready to tackle the day. The first thing I do nowadays as soon as I wake up is write a TODOlist",
            "This might look like a simple thing, but this has actually helped me visualise how my day is going to look like",
            "But there are days where the tasklist is just endless and I don't feel like even finishing off a single task.",
            "I'm not sure if this is just me or there are folks like me, whenever I have a long list I get really overwhelmed and tend to not complete even a single task.",
            "It's like if I can see myself completing all the tasks, then I would work on it and if not I wouldn't even finish one, I read somewhere that this all or nothing behaviour is quite bad.",
            "This also reflects in my workout routines, whenever I do gym, I do it perfectly and if at all I eat one wrong meal or a couple of missed workout days back to back, then I sabotage my health as a whole",
            "After which I spiral in, realise I'm at a very bad state and then startover again, while starting over is good, it's not sustainable unless we are consistent, else, there's just a lot of lost progress"
        ],
    },
    {
        "name": "label coverage",
        "criterion": 2,
        # Inputs spread across your score range, so you can check all three
        # labels are actually reachable.
        "texts": [
            " spent Saturday afternoon organizing my room and sorting through old boxes of books and stationery. It felt surprisingly calming once I cleared enough space to see the desk again. I had been postponing the task for weeks, even though it only took a few hours to complete. By the evening, I was more relaxed and felt a small sense of accomplishment.",
            "I recently visited Georgia, it was my dream from the last few months to visit this place, and trust me, it was magical, and the weather, the itinerary everything was just perfect! Georgia is truly an underrated place!",
            "I had been considering my plans for the next few months, although I did not want to commit to a definite direction too quickly. I enjoy having structure, but I also know that my interests tend to change as new opportunities appear. For now, I am trying to balance careful planning with enough flexibility to adjust when circumstances change.",
        ],
    },
        {
        "name": "appeal path",
        "criterion": 3,
        "texts": [
            "I wrote this paragraph myself and am requesting a person to review the result.",
            "This second paragraph describes an ordinary event from my week and was written by me.",
            "I am submitting this third personal passage for review because I wrote it myself.",
        ],
        "appeals": 3,
    },
    {
        "name": "score separation",
        "criterion": 4,
        "texts": [
            "Artificial intelligence systems process information through layered mathematical representations that transform inputs into probabilistic outputs.",
            "Organizations implement governance frameworks to establish accountability, evaluate operational risk, and document recurring decisions.",
            "Effective software architecture separates responsibilities to improve maintainability and support future changes.",
            "The evidence suggests that consistent monitoring, standardized procedures, and periodic review improve system reliability.",
            "Environmental policy requires accurate measurements, transparent assumptions, and reliable methods for evaluating long-term outcomes.",
            "I missed the bus and walked home in the rain.",
            "We cooked dinner together and burned the vegetables.",
            "My sister called me while I was studying, and we talked longer than planned.",
            "I bought coffee before class, but the cup spilled in my bag.",
            "The library printer stopped working, so a staff member helped me try the machine nearby.",
        ],
    },
    {
        "name": "bad input",
        "criterion": 5,
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
