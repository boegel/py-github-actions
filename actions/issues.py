from github import Github

from actions.event import get_event_data
from actions.utils import get_github_token


def issue_or_pr_context():
    """Check if current workflow was triggered by an issue or pull request."""
    event_data = get_event_data()
    return 'issue' in event_data or 'pull_request' in event_data


def pr_context():
    """Check if current workflow was triggered by a pull request."""
    event_data = get_event_data()
    return 'pull_request' in event_data or 'pull_request' in event_data.get('issue', {})


def _get_repo():
    """Get repository that triggered current workflow."""
    event_data = get_event_data()
    gh = Github(get_github_token())
    repo = gh.get_repo(event_data['repository']['full_name'])

    return repo


def _get_event_data_key_from_issue_or_pr(key):
    """Get value corresponding to specified key from event data for current workflow."""
    event_data = get_event_data()
    if 'issue' in event_data:
        res = event_data['issue'][key]
    else:
        res = event_data['pull_request'][key]

    return res


def _get_issue(repo=None):
    """Get issue that triggered current workflow."""
    if not issue_or_pr_context():
        raise RuntimeError("Current workflow was not triggered by an issue or pull request!")

    if repo is None:
        repo = _get_repo()

    issue_id = _get_event_data_key_from_issue_or_pr('number')
    return repo.get_issue(issue_id)


def _get_pr(repo=None):
    """Get pull request that triggered current workflow."""
    if not pr_context():
        raise RuntimeError("Current workflow was not triggered by a pull request!")

    if repo is None:
        repo = _get_repo()

    pr_id = _get_event_data_key_from_issue_or_pr('number')
    return repo.get_pull(pr_id)


def get_issue_comments():
    """Get comments for issue (or pull request) that triggered current workflow."""
    issue = _get_issue()

    comments = issue.get_comments()

    return [c.body for c in comments]


def get_pr_review_comments():
    """Get pull request review comments for PR that triggered current workflow."""
    pr = _get_pr()

    comments = pr.get_comments()

    return [c.body for c in comments]


def get_pr_status():
    """Get (combined) status of pull request that triggered current workflow."""
    repo = _get_repo()
    pr = _get_pr(repo=repo)

    last_pr_commit = repo.get_commit(pr.head.sha)
    status = last_pr_commit.get_combined_status().state

    return status


def get_label_names():
    """Get (sorted) list label names for issue (or pull request) that triggered current workflow."""
    if not issue_or_pr_context():
        raise RuntimeError("Current workflow was not triggered by an issue or pull request!")

    labels = _get_event_data_key_from_issue_or_pr('labels')

    return sorted([l['name'] for l in labels])


def get_milestone_title():
    """Get milestone title (if any) for issue (or pull request) that triggered current workflow."""
    if not issue_or_pr_context():
        raise RuntimeError("Current workflow was not triggered by an issue or pull request!")

    milestone = _get_event_data_key_from_issue_or_pr('milestone')
    if milestone is None:
        res = None
    else:
        res = milestone['title']

    return res


def post_comment(txt):
    """Post comment in issue (or pull request) that triggered current workflow."""
    event_data = get_event_data()

    templates = {}
    if 'comment' in event_data:
        templates['comment_body'] = event_data['comment']['body']
    if 'sender' in event_data:
        templates['sender_login'] = event_data['sender']['login']

    # try to complete templates before posting comment
    try:
        templated_txt = txt % templates
    except KeyError as err:
        raise KeyError("One or more unknown templates used in comment body: %s" % err)

    # post comment in issue that triggered current workflow
    issue = _get_issue()
    return issue.create_comment(templated_txt)
