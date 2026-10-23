"""Seed content for the FutureReady portal. Question banks, branches, admission routes and resources are loaded into the database
(`engine.seed_content`) so administrators can edit and version them. Everything here is original EduAakashaa material."""


def Q(code, skill, prompt, options=None, answer=None, explanation='', distractors=None, qtype='mcq', level=None, gmin=8, gmax=9, reverse=False, meta=None):
    return dict(code=code, skill=skill, prompt=prompt, options=options or [], answer=answer, explanation=explanation,
                distractors=distractors or {}, qtype=qtype, level=level, grade_min=gmin, grade_max=gmax, reverse=reverse, meta=meta or {})


def LK(code, skill, prompt, reverse=False, gmin=8, gmax=9, meta=None):
    """5-point agreement item (1 = not like me … 5 = very much like me). Reported as a self-perception, never as an objective score."""
    return Q(code, skill, prompt, qtype='likert', reverse=reverse, gmin=gmin, gmax=gmax, meta=meta)


def CH(code, skill, prompt, opts, meta=None):
    """Scenario choice: opts = [(text, {tag: weight})]. Used for interest maps; no right or wrong answer."""
    return Q(code, skill, prompt, options=[{'t': t, 'tags': tags} for t, tags in opts], qtype='choice', meta=meta)


def TX(code, skill, prompt, meta=None):
    return Q(code, skill, prompt, qtype='text', meta=meta)
