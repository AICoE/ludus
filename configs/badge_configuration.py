"""Badge configuration."""
badges = {
    'first-pull': {
        'description': 'first pull request merged',
        'event_type': 'pull_request',
        'criteria': {
            'type': 'count',
            'value': 1
        },
        'image_file': None
    },
    'pull-master': {
        'description': '5 pull requests merged',
        'event_type': 'pull_request',
        'criteria': {
            'type': 'count',
            'value': 5
        },
        'image_file': None
    },
    'pull-king': {
        'description': '10 pull requests merged',
        'event_type': 'pull_request',
        'criteria': {
            'type': 'count',
            'value': 10
        },
        'image_file': None
    },
    'first-issue': {
        'description': 'awarded for creating first issue',
        'event_type': 'issue',
        'criteria': {
            'type': 'count',
            'value': 1
        },
        'image_file': None
    },
    'first-github-comment': {
        'description': 'awarded for first github comment',
        'event_type': 'github_comment',
        'criteria': {
            'type': 'count',
            'value': 1
        },
        'image_file': None
    },
    'bug-squasher': {
        'description': 'awarded for fixing an issue with the tag bug',
        'criteria': {
            'type': 'match',
            'matching_events': [
                {
                    'event_type': 'bug_fixed',
                    'field': 'raw_github.issue.number'
                },
                {
                    'event_type': 'pull_request',
                    'field': 'issue_closes'
                }
            ]
        },
        'image_file': None
    },
    'first-review': {
        'description': 'awarded for reviewing and merging first pull-request',
        'event_type': 'review',
        'criteria': {
            'type': 'count',
            'value': 1
        },
        'image_file': None
    },
    'review-master': {
        'description': 'awarded for reviewing and merging 5 pull-requests',
        'event_type': 'review',
        'criteria': {
            'type': 'count',
            'value': 5
        },
        'image_file': None
    },
    'review-king': {
        'description': 'awarded for reviewing and merging 10 pull-requests',
        'event_type': 'review',
        'criteria': {
            'type': 'count',
            'value': 10
        },
        'image_file': None
    },
    'homerun': {
        'description': 'awarded for opening an issue, creating pull request, closing the issue',
        'criteria': {
            'type': 'match',
            'matching_events': [
                {
                    'event_type': 'issue_closed',
                    'field': 'raw_github.issue.number'
                },
                {
                    'event_type': 'pull_request',
                    'field': 'issue_closes'
                },
                {
                    'event_type': 'issue',
                    'field': 'raw_github.issue.number'
                }
            ]
        },
        'image_file': None
    },
    'first-trello-comment': {
        'description': 'awarded for first trello comment',
        'event_type': 'trello_comment',
        'criteria': {
            'type': 'count',
            'value': 1
        },
        'image_file': None
    },
    'first_idea': {
        'description': 'awarded for creating first trello card in New list',
        'event_type': 'new_idea',
        'criteria': {
            'type': 'count',
            'value': 1
        },
        'image_file': None
    },
    'think-tank': {
        'description': 'awarded for creating 5 trello cards in New list',
        'event_type': 'new_idea',
        'criteria': {
            'type': 'count',
            'value': 5
        },
        'image_file': None
    },
    'finisher': {
        'description': 'awarded for moving a card in the completed list',
        'event_type': 'task_completed',
        'criteria': {
            'type': 'every_event'
        },
        'image_file': None
    },
    'trellorun': {
        'description': 'awarded for creating a card in new list, moving it through backlog and in-progress lists\
             and finally in completed list',
        'criteria': {
            'type': 'match',
            'matching_events': [
                {
                    'event_type': 'new_idea',
                    'field': 'raw_trello.action.data.card.id'
                },
                {
                    'event_type': 'task_moved_to_backlog',
                    'field': 'raw_trello.action.data.card.id'
                },
                {
                    'event_type': 'task_moved_to_inprogress',
                    'field': 'raw_trello.action.data.card.id'
                },
                {
                    'event_type': 'task_completed',
                    'field': 'raw_trello.action.data.card.id'
                },
            ]
        },
        'image_file': None
    }
}
