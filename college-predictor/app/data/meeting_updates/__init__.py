"""Meeting updates that an admin can apply to one student's mentorship record (Admin, Mentorship, the student's row, "Apply a meeting update").

Each pack is a dict (see yusra_2026_11_02.py for the fields). To add one, write a module with a PACKS list and add it to _MODULES.
"""
from . import yusra_2026_11_02

_MODULES = [yusra_2026_11_02]
PACKS = {p['key']: p for m in _MODULES for p in m.PACKS}
