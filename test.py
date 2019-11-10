import copy
import json
import os
import pytest

import actions.issues
from actions.constants import STATUS_SUCCESS
from actions.event import get_event_data, get_event_trigger, triggered_by
from actions.issues import get_issue_comments, get_label_names, get_pr_review_comments, get_pr_status
from actions.issues import issue_or_pr_context, pr_context, post_comment
from actions.utils import get_env_var, get_github_token

TEST_EVENT_NAME = 'issue_comment'
TEST_EVENT_DATA = {
    'action': 'created',
    'comment': {
        'body': 'testing, 1, 2, 3',
        'created_at': '1970-01-01T00:00:01',
        'user': {'login': 'boegel'},
    },
    'issue': {
        'labels': [
            {'name': 'critical'},
            {'name': 'bug'},
        ],
        'number': 123,
        'user': {'login': 'boegel'},
    },
    'repository': {
        'full_name': 'boegel/py-github-actions',
        'owner': {'login': 'boegel'},
    },
    'sender': {'login': 'boegel'},
}


class MockedComment(object):
    def __init__(self, body):
        self.body = body


class MockedCommit(object):
    def __init__(self, sha):
        self.sha = sha

    def get_combined_status(self):
        class MockedCombinedStatus(object):
            @property
            def state(self):
                return 'success'

        return MockedCombinedStatus()


class MockedLabel(object):
    def __init__(self, name):
        self.name = name


class MockedIssue(object):
    def create_comment(self, txt):
        return txt

    def get_comments(self):
        return [MockedComment(c) for c in ["hello world", "this is a comment"]]


class MockedPR(object):
    def get_comments(self):
        return [MockedComment('lgtm')]

    @property
    def head(self):
        class MockedHead(object):
            @property
            def sha(self):
                return 'sha123'

        return MockedHead()


class MockedRepo(object):
    def get_commit(self, sha):
        return MockedCommit(sha)

    def get_issue(self, number):
        return MockedIssue()

    def get_pull(self, number):
        return MockedPR()


class MockedGithub(object):
    def __init__(self, token):
        pass

    def get_repo(self, repo_name):
        return MockedRepo()


@pytest.fixture(scope='function', autouse=True)
def clear_caches():
    get_event_data.clear_cache()


def install_test_event_data(monkeypatch, tmpdir, event_name=TEST_EVENT_NAME, event_data=TEST_EVENT_DATA):
    """Install test event data."""
    monkeypatch.setenv('GITHUB_EVENT_NAME', event_name)
    test_event_data_fp = tmpdir.join('test_event_data.json')
    test_event_data_fp.write(json.dumps(event_data))
    monkeypatch.setenv('GITHUB_EVENT_PATH', str(test_event_data_fp))


def test_get_env_var(monkeypatch):
    """Test get_env_var function."""

    name = 'TEST123'

    # OSError is raised if environment is not defined
    monkeypatch.delenv(name, raising=False)
    with pytest.raises(OSError):
        get_env_var(name)

    monkeypatch.setenv(name, 'test123')
    value = get_env_var(name)
    assert(value == 'test123')


def verify_parsed_test_event_data(event_data):
    """Verify parsed test event data."""
    assert(isinstance(event_data, dict))
    assert(sorted(event_data.keys()) == ['action', 'comment', 'issue', 'repository', 'sender'])
    assert(event_data['action'] == 'created')
    assert(event_data['comment']['body'] == 'testing, 1, 2, 3')
    assert(event_data['issue']['number'] == 123)
    assert(event_data['repository']['owner']['login'] == 'boegel')


def test_get_event_data(capsys, monkeypatch, tmpdir):
    """Test get_event_data function."""

    monkeypatch.delenv('GITHUB_EVENT_PATH', raising=False)
    with pytest.raises(OSError):
        get_event_data()

    install_test_event_data(monkeypatch, tmpdir, event_data={})
    assert(get_event_data() == {})

    # put test event data in place
    install_test_event_data(monkeypatch, tmpdir)
    event_data = get_event_data()

    # by default, cached result is returned, so we still get empty event data
    assert(event_data == {})

    # can be disabled via use_cache=False
    event_data = get_event_data(use_cache=False)
    verify_parsed_test_event_data(event_data)

    # cache can also be cleared using clear_cache()
    get_event_data.clear_cache()
    install_test_event_data(monkeypatch, tmpdir, event_data={})
    assert(get_event_data() == {})
    get_event_data.clear_cache()

    # by default, no output is produced by get_event_data()
    install_test_event_data(monkeypatch, tmpdir)
    event_data = get_event_data()
    verify_parsed_test_event_data(event_data)

    captured = capsys.readouterr()
    assert(captured[0] == captured[1] == '')

    event_data = get_event_data(verbose=True)
    verify_parsed_test_event_data(event_data)

    captured = capsys.readouterr()
    assert("'action': " in captured[0])
    assert("'created'," in captured[0])
    assert('' == captured[1])


def test_get_event_trigger(monkeypatch, tmpdir):
    """Test get_event_trigger function."""

    monkeypatch.delenv('GITHUB_EVENT_NAME', raising=False)
    with pytest.raises(OSError):
        get_event_trigger()

    # event type is determined via event data
    install_test_event_data(monkeypatch, tmpdir)

    event_name = get_event_trigger()
    assert(event_name == 'issue_comment.created')


def test_triggered_by(monkeypatch, tmpdir):
    """Test triggered_by function."""
    install_test_event_data(monkeypatch, tmpdir)

    assert(triggered_by('issue_comment'))
    assert(triggered_by('push') is False)
    assert(triggered_by('issue_comment', activity_type='created'))
    assert(triggered_by('issue_comment', activity_type='deleted') is False)
    assert(triggered_by('issue_comment', activity_type='edited') is False)

    # using unknown event names or activity types triggers an exception
    with pytest.raises(ValueError):
        triggered_by('no_such_event_name')
        triggered_by('delete')  # 'deleted' is correct, 'delete' is not
        triggered_by('issue_comment', activity_type='no_such_activity_type')
        triggered_by('issue_comment', activity_type='opened')
        triggered_by('no_such_event_name', activity_type='no_such_activity_type')
        triggered_by('delete', activity_type='opened')


def test_get_github_token(monkeypatch):
    """Test get_github_token function."""

    monkeypatch.delenv('GITHUB_TOKEN', raising=False)
    with pytest.raises(OSError):
        get_github_token()

    monkeypatch.setenv('GITHUB_TOKEN', 'thisisjustatest')
    assert(get_github_token() == 'thisisjustatest')


def test_issue_or_pr_context(monkeypatch, tmpdir):
    """Test issue_or_pr_context function."""
    install_test_event_data(monkeypatch, tmpdir)

    assert(issue_or_pr_context())
    assert(pr_context() is False)

    test_event_data = copy.copy(TEST_EVENT_DATA)
    test_event_data['issue']['pull_request'] = {}
    install_test_event_data(monkeypatch, tmpdir, event_data=test_event_data)
    get_event_data.clear_cache()

    assert(issue_or_pr_context())
    assert(pr_context())

    del test_event_data['issue']
    install_test_event_data(monkeypatch, tmpdir, event_data=test_event_data)
    get_event_data.clear_cache()

    assert(issue_or_pr_context() is False)
    assert(pr_context() is False)


def test_get_label_names(monkeypatch, tmpdir):
    """Test get_label_names function."""
    monkeypatch.setattr(actions.issues, 'Github', MockedGithub)
    install_test_event_data(monkeypatch, tmpdir)

    monkeypatch.setenv('GITHUB_TOKEN', 'thisisjustatest')
    assert(get_label_names() == ['bug', 'critical'])


def test_get_issue_comments(monkeypatch, tmpdir):
    """Test get_issue_comments function."""
    monkeypatch.setattr(actions.issues, 'Github', MockedGithub)
    install_test_event_data(monkeypatch, tmpdir)

    monkeypatch.setenv('GITHUB_TOKEN', 'thisisjustatest')
    assert(get_issue_comments() == ["hello world", "this is a comment"])


def test_get_pr_review_comments(monkeypatch, tmpdir):
    monkeypatch.setattr(actions.issues, 'Github', MockedGithub)
    install_test_event_data(monkeypatch, tmpdir)

    monkeypatch.setenv('GITHUB_TOKEN', 'thisisjustatest')
    assert(get_pr_review_comments() == ['lgtm'])


def test_get_pr_status(monkeypatch, tmpdir):
    monkeypatch.setattr(actions.issues, 'Github', MockedGithub)
    install_test_event_data(monkeypatch, tmpdir)

    monkeypatch.setenv('GITHUB_TOKEN', 'thisisjustatest')
    assert(get_pr_status() == STATUS_SUCCESS)


def test_post_comment(monkeypatch, tmpdir):
    """Test post_comment function."""
    monkeypatch.setattr(actions.issues, 'Github', MockedGithub)
    install_test_event_data(monkeypatch, tmpdir)

    # exception is raised if $GITHUB_TOKEN is not defined
    monkeypatch.delenv('GITHUB_TOKEN', raising=False)
    with pytest.raises(OSError):
        post_comment("this is just a test")

    monkeypatch.setenv('GITHUB_TOKEN', 'thisisjustatest')
    txt = "this is just a test"
    assert(post_comment(txt) == txt)

    txt = "Replying to comment '%(comment_body)s' sent by @%(sender_login)s"
    assert(post_comment(txt) == "Replying to comment 'testing, 1, 2, 3' sent by @boegel")

    # check what happens when unknown templates are used
    for txt in ["What if we use an %(unknown_template_value)s?", "replying to @%(sender_login)s: %(foobar)s"]:
        with pytest.raises(KeyError):
            post_comment(txt)
