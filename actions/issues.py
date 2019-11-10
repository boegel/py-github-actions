from github import Github

from actions.event import get_event_data
from actions.utils import get_github_token


def issue_or_pr_context():
    """Check if current workflow was triggered by an issue or pull request."""
    event_data = get_event_data()
    return 'issue' in event_data


def pr_context():
    """Check if current workflow was triggered by a pull request."""
    event_data = get_event_data()
    return 'pull_request' in event_data.get('issue', {})


def post_comment(txt):
    """Post comment in issue (or pull reuqest) that triggered current workflow."""
    if not issue_or_pr_context():
        raise RuntimeError("Current workflow was not triggered by an issue or pull request!")

    event_data = get_event_data()

    gh = Github(get_github_token())

    repo = gh.get_repo(event_data['repository']['full_name'])

    issue = repo.get_issue(number=event_data['issue']['number'])

    return issue.create_comment(txt)