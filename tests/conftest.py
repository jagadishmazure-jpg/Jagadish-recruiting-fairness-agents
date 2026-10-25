import pytest

from recfair.data import make_candidates
from recfair.pipeline import run


@pytest.fixture(scope="session")
def cands():
    return make_candidates(400, 7)


@pytest.fixture(scope="session")
def result():
    return run(400, 7)
