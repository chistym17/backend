import pytest
from core.libs.exceptions import FyleError

def test_fyle_error_initialization():
    error = FyleError(status_code=404, message='Resource not found')

    assert error.status_code == 404
    assert error.message == 'Resource not found'


def test_fyle_error_to_dict():
    error = FyleError(status_code=403, message='Access Denied')

    error_dict = error.to_dict()
    assert error_dict == {'message': 'Access Denied'}
