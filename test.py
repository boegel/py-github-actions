import os
import pytest

from actions import get_event_data

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

def test_get_event_data(tmpdir):
    """Test get_event_data function."""

    # EnvironmentError is raised if $GITHUB_EVENT_PATH is not defined
    if 'GITHUB_EVENT_PATH' in os.environ:
        del os.environ['GITHUB_EVENT_PATH']
    with pytest.raises(OSError):
        get_event_data()

    test_event_data = tmpdir.join('test_event_data.json')
    test_event_data.write(TEST_EVENT_DATA_RAW)

    os.environ['GITHUB_EVENT_PATH'] = str(test_event_data)
    event_data = get_event_data()

    assert(isinstance(event_data, dict))
    assert(sorted(event_data.keys()) == ['actions', 'comment', 'issue', 'repository', 'sender'])
    assert(event_data['actions'] == 'created')
    assert(event_data['comment']['body'] == 'test')
    assert(event_data['issue']['number'] == 123)
    assert(event_data['repository']['owner']['login'] == 'boegel')
