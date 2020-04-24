"""Event configuration."""
from validators import pull_request_validator, issue_validator, issue_closed_validator, github_comment_validator, \
    review_validator, bug_fixed_validator
from validators import trello_comment_validator, new_idea_validator, task_completed_validator, \
    task_moved_to_backlog_validator, task_moved_to_inprogress_validator


config = {
    'pull_request': {
        'validator': pull_request_validator.schema,
        'formatter': 'pull_request_formatter'
    },
    'issue': {
        'validator': issue_validator.schema,
        'formatter': 'issue_formatter'
    },
    'issue_closed': {
        'validator': issue_closed_validator.schema,
        'formatter': 'issue_closed_formatter'
    },
    'github_comment': {
        'validator': github_comment_validator.schema,
        'formatter': 'github_comment_formatter'
    },
    'bug_fixed': {
        'validator': bug_fixed_validator.schema,
        'formatter': 'bug_fixed_formatter'
    },
    'review': {
        'validator': review_validator.schema,
        'formatter': 'review_formatter'
    },
    'trello_comment': {
        'validator': trello_comment_validator.schema,
        'formatter': 'trello_comment_formatter'
    },
    'new_idea': {
        'validator': new_idea_validator.schema,
        'formatter': 'new_idea_formatter'
    },
    'task_moved_to_backlog': {
        'validator': task_moved_to_backlog_validator.schema,
        'formatter': 'task_moved_to_backlog_formatter'
    },
    'task_moved_to_inprogress': {
        'validator': task_moved_to_inprogress_validator.schema,
        'formatter': 'task_moved_to_inprogress_formatter'
    },
    'task_completed': {
        'validator': task_completed_validator.schema,
        'formatter': 'task_completed_formatter'
    }
}
