# EduAakashaA portal: working rules

## Keep the portal guide current (required)
The step-by-step guide for admins, mentors, students and parents is `app/services/portal_guide.py`, shown at `/portal-guide/` (Admin menu "Guide", mentor menu, Member Home "Portal guide").

Whenever you add, change or remove a portal feature (a page, a tool, a Member Home tile, an admin screen, a workflow step, a price or plan):
1. edit or add the matching entry in `GUIDE` (steps, `where` links, `tiles`),
2. add a line at the top of `CHANGELOG` and set `UPDATED` to the same date,
3. new Member Home tile: name it in an entry's `tiles`. New blueprint: add it to `COVERED_BLUEPRINTS`.

`tests/test_portal_guide.py` fails if a tile or blueprint is undocumented, if a guide link no longer resolves, or if CHANGELOG/UPDATED are out of step.

## Other conventions
* Tests are standalone scripts in `tests/` (run `python tests/<name>.py` from `college-predictor/`).
* The database has no migrations: new features use new tables (`db.create_all()`).
* Guide pages carry the premium alert (see `dg-alert` blocks); premium-only pages word it for active members.
