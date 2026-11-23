"""Loading the EduPulse Reinforcement question bank: complete in one go, resumable when time runs out, and repeatable. Run from college-predictor/:  python tests/test_rf_seed.py"""
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
_fd, _db = tempfile.mkstemp(suffix='.db')
os.close(_fd)
os.environ.update(DATABASE_URL='sqlite:///' + _db, SECRET_KEY='test', FLASK_DEBUG='0')

from app import create_app  # noqa: E402
from app.extensions import db  # noqa: E402
from app.models_reinforce import RfQuestion  # noqa: E402
from app.services import reinforce as rf  # noqa: E402

app = create_app()
with app.app_context():
    db.create_all()
    n1 = rf.seed_bank(budget=0.0001)                    # time is up at once: a clean partial load, nothing half-written
    part = RfQuestion.query.count()
    assert rf.seed_partial() and 0 < part < 3000 and n1 == part, (n1, part)
    n2 = rf.seed_bank(budget=120)                       # picks up where it stopped
    total = RfQuestion.query.count()
    assert not rf.seed_partial() and total == part + n2 and total > 3000, (part, n2, total)
    assert rf.seed_bank() == 0 and RfQuestion.query.count() == total          # repeating adds nothing
    jee = rf.approved('JEE')
    from app.data.jee_topics import RF_CHAPTER
    for ch in {v for v in RF_CHAPTER.values() if v}:
        assert jee.filter_by(chapter=ch).count() >= 3, ch                       # every mapped gap-map chapter has questions
    # PostgreSQL enforces column lengths (SQLite does not): no stored text may be longer than its column
    from app.models_reinforce import RfQuestionImage, RfTaxonomy
    for M in (RfQuestion, RfQuestionImage, RfTaxonomy):
        for col in M.__table__.columns:
            n = getattr(col.type, 'length', None)
            if n and col.name != 'id':
                longest = max((len(str(getattr(r, col.name) or '')) for r in M.query.all()), default=0)
                assert longest <= n, (M.__tablename__, col.name, longest, n)
print('rf seed checks passed')
