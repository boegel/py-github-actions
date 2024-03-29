# keywords in event data
ACTION = 'action'

# GitHub environment variables
# see https://help.github.com/en/actions/automating-your-workflow-with-github-actions/using-environment-variables
GITHUB_ACTOR = 'GITHUB_ACTOR'
GITHUB_ACTION = 'GITHUB_ACTION'
GITHUB_ACTIONS = 'GITHUB_ACTIONS'
GITHUB_EVENT_NAME = 'GITHUB_EVENT_NAME'
GITHUB_EVENT_PATH = 'GITHUB_EVENT_PATH'
GITHUB_BASE_REF = 'GITHUB_BASE_REF'
GITHUB_HEAD_REF = 'GITHUB_HEAD_REF'
GITHUB_REF = 'GITHUB_REF'
GITHUB_REPOSITORY = 'GITHUB_REPOSITORY'
GITHUB_SHA = 'GITHUB_SHA'
GITHUB_TOKEN = 'GITHUB_TOKEN'
GITHUB_WORKFLOW = 'GITHUB_WORKFLOW'
GITHUB_WORKSPACE = 'GITHUB_WORKSPACE'

# set of event names & associated event types (if any)
# see https://help.github.com/en/actions/automating-your-workflow-with-github-actions/events-that-trigger-workflows

# event names
CHECK_RUN = 'check_run'
CHECK_SUITE = 'check_suite'
CREATE = 'create'
DELETE = 'delete'
DEPLOYMENT = 'deployment'
DEPLOYMENT_STATUS = 'deployment_status'
FORK = 'fork'
GOLLUM = 'gollum'
ISSUE_COMMENT = 'issue_comment'
ISSUES = 'issues'
LABEL = 'label'
MEMBER = 'member'
MILESTONE = 'milestone'
PAGE_BUILD = 'page_build'
PROJECT = 'project'
PROJECT_CARD = 'project_card'
PROJECT_COLUMN = 'project_column'
PUBLIC = 'public'
PULL_REQUEST = 'pull_request'
PULL_REQUEST_REVIEW = 'pull_request_review'
PULL_REQUEST_REVIEW_COMMENT = 'pull_request_review_comment'
PUSH = 'push'
RELEASE = 'release'
REPOSITORY_DISPATCH = 'repository_dispatch'
SCHEDULED = 'scheduled'
STATUS = 'status'
WATCH = 'watch'

# activity types for events
ADDED = 'added'
ASSIGNED = 'assigned'
CLOSED = 'closed'
COMPLETED = 'completed'
CONVERTED = 'converted'
CREATED = 'created'
DELETED = 'deleted'
DEMILESTONED = 'demilestoned'
DISMISSED = 'dismissed'
EDITED = 'edited'
LABELED = 'labeled'
LOCKED = 'locked'
MILESTONED = 'milestoned'
MOVED = 'moved'
OPENED = 'opened'
PINNED = 'pinned'
PRERELEASED = 'prereleased'
PUBLISHED = 'published'
READY_FOR_REVIEW = 'ready_for_review'
REOPENED = 'reopened'
REREQUESTED = 'rerequested'
REQUESTED = 'requested'
REQUESTED_ACTION = 'REQUESTED_action'
REVIEW_REQUEST_REMOVED = 'review_request_removed'
REVIEW_REQUESTED = 'review_requested'
STARTED = 'started'
SUBMITTED = 'submitted'
SYNCHRONIZE = 'synchronize'
TRANSFERRED = 'transferred'
UNASSIGNED = 'unassigned'
UPDATED = 'updated'
UNLABELED = 'unlabeled'
UNLOCKED = 'unlocked'
UNPINNED = 'unpinned'
UNPUBLISHED = 'unpublished'

# mapping of event names to valid activity types
EVENT_TRIGGERS = {
    # webhook events
    CHECK_RUN: {CREATED, COMPLETED, REREQUESTED, REQUESTED_ACTION},
    CHECK_SUITE: {COMPLETED, REREQUESTED, REQUESTED},
    CREATE: {},
    DELETE: {},
    DEPLOYMENT: {},
    DEPLOYMENT_STATUS: {},
    FORK: {},
    GOLLUM: {},
    ISSUE_COMMENT: {CREATED, DELETED, EDITED},
    ISSUES: {
        ASSIGNED, CLOSED, DELETED, DEMILESTONED, EDITED, LABELED, LOCKED, MILESTONED,
        OPENED, PINNED, REOPENED, TRANSFERRED, UNASSIGNED, UNLABELED, UNLOCKED, UNPINNED,
    },
    LABEL: {CREATED, DELETED, EDITED},
    MEMBER: {ADDED, DELETED, EDITED},
    MILESTONE: {CLOSED, CREATED, DELETED, EDITED, OPENED},
    PAGE_BUILD: {},
    PROJECT: {CLOSED, CREATED, DELETED, EDITED, REOPENED, UPDATED},
    PROJECT_CARD: {CONVERTED, CREATED, DELETED, EDITED, MOVED},
    PROJECT_COLUMN: {CREATED, DELETED, MOVED, UPDATED},
    PUBLIC: {},
    PULL_REQUEST: {
        ASSIGNED, CLOSED, EDITED, LABELED, LOCKED, OPENED, READY_FOR_REVIEW, REOPENED,
        REVIEW_REQUEST_REMOVED, REVIEW_REQUESTED, SYNCHRONIZE, UNASSIGNED, UNLABELED, UNLOCKED,
    },
    PULL_REQUEST_REVIEW: {DISMISSED, EDITED, SUBMITTED},
    PULL_REQUEST_REVIEW_COMMENT: {CREATED, DELETED, EDITED},
    PUSH: {},
    RELEASE: {CREATED, DELETED, EDITED, PRERELEASED, PUBLISHED, UNPUBLISHED},
    STATUS: {},
    WATCH: {STARTED},
    # scheduled events
    SCHEDULED: {},
    # external events
    REPOSITORY_DISPATCH: {},
}

# commit statuses
# see https://developer.github.com/v3/repos/statuses
STATUS_ERROR = 'error'
STATUS_FAILURE = 'failure'
STATUS_PENDING = 'pending'
STATUS_SUCCESS = 'success'
