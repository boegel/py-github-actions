import os
import pytest

import actions

TEST_EVENT_DATA_RAW = """
{
    "actions": "created",
    "comment": {
        "body": "test",
        "created_at": "1970-01-01T00:00:01",
        "user": {"login": "boegel"}
    },
    "issue": {
        "number": 123,
        "user": {"login": "boegel"}
    },
    "repository": {
        "full_name": "boegel/github-actions",
        "owner": {"login": "boegel"}
    },
    "sender": {"login": "boegel"}
}
"""


def test_get_env_var(monkeypatch):
    """Test get_env_var function."""

    name = 'TEST123'

    # OSError is raised if environment is not defined
    monkeypatch.delenv(name, raising=False)
    with pytest.raises(OSError):
        actions.get_env_var(name)

    monkeypatch.setenv(name, 'test123')
    value = actions.get_env_var(name)
    assert(value == 'test123')


def verify_parsed_test_event_data(event_data):
    """Verify parsed test event data."""

    assert(isinstance(event_data, dict))
    assert(sorted(event_data.keys()) == ['actions', 'comment', 'issue', 'repository', 'sender'])
    assert(event_data['actions'] == 'created')
    assert(event_data['comment']['body'] == 'test')
    assert(event_data['issue']['number'] == 123)
    assert(event_data['repository']['owner']['login'] == 'boegel')


def test_get_event_data(capsys, monkeypatch, tmpdir):
    """Test get_event_data function."""

    monkeypatch.delenv('GITHUB_EVENT_PATH', raising=False)
    with pytest.raises(OSError):
        actions.get_event_data()

    test_event_data = tmpdir.join('test_event_data.json')
    test_event_data.write(TEST_EVENT_DATA_RAW)

    monkeypatch.setenv('GITHUB_EVENT_PATH', str(test_event_data))
    event_data = actions.get_event_data()
    verify_parsed_test_event_data(event_data)

    # by default, no output is produced by get_event_data()
    captured = capsys.readouterr()
    assert(captured[0] == captured[1] == '')

    event_data = actions.get_event_data(verbose=True)
    verify_parsed_test_event_data(event_data)

    captured = capsys.readouterr()
    assert(captured[0].startswith("{u'actions': u'created',"))
    assert('' == captured[1])


def test_get_event_name(monkeypatch):
    """Test get_event_name function."""

    monkeypatch.delenv('GITHUB_EVENT_NAME', raising=False)
    with pytest.raises(OSError):
        actions.get_event_name()

    monkeypatch.setenv('GITHUB_EVENT_NAME', 'test123')
    event_name = actions.get_event_name()
    assert(event_name == 'test123')
