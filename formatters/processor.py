"""Utilty functions for formatters."""
import re


class Processor:
    """Processor."""

    def get_processor(event_type):
        """Get processor."""
        if event_type == 'pull_request':
            return PullRequestEventProcessor()
        else:
            return DefaultEventProcessor()


class DefaultEventProcessor:
    """Default event processor."""

    def get_variables(self, event_type, event):
        """Get variables."""
        variables = dict()
        return variables


class PullRequestEventProcessor:
    """Pull request event processor."""

    def get_variables(self, event_type, event):
        """Get variables."""
        variables = dict()

        if event_type != 'pull_request':
            raise Exception

        body = event['pull_request']['body']
        issue_number = None

        match_found = re.search(r'(closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s*#[0-9]+', body,
                                flags=re.IGNORECASE)
        if match_found:
            issue_closes = match_found.group(0)
            issue_number = re.search('[0-9]+', issue_closes).group(0)

        variables['issue_number'] = issue_number
        return variables
