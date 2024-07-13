import pytest
from server.controllers.getEchoChamberStatus import validateInput


def test_validateInput():
    validateInput("abc", "youtube")
    assert True

    with pytest.raises(Exception):
        validateInput("abc", None)

    with pytest.raises(Exception):
        validateInput(None, "youtube")
