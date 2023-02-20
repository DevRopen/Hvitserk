# MIT License
#
# Copyright (c) 2022 Clivern
#
# This software is licensed under the MIT License. The full text of the license
# is provided below.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from hvitserk.api import Issue
from hvitserk.util import Logger
from datetime import datetime
from dateutil.tz import tzutc


class Stale:
    """Stale Plugin"""

    def __init__(self, app, repo_name, plugin_rules, logger):
        self._app = app
        self._issue = Issue(self._app)
        self._repo_name = repo_name
        self._plugin_rules = plugin_rules
        self._logger = Logger().get_logger(__name__) if logger is None else logger

    def run(self):
        """Execute the plugin to process issues and pull requests."""
        self._logger.info(f"Running Stale V1 Plugin for repository: {self._repo_name}")

        # Check for issues
        if self._plugin_rules.issues.enabled:
            self._logger.info(f"Stale rules are enabled for {self._repo_name} issues.")
            self._process_issues()
        else:
            self._logger.info(
                f"Stale rules are not enabled for {self._repo_name} issues. Skipping!"
            )

        # Check for pull requests
        if self._plugin_rules.pulls.enabled:
            self._logger.info(
                f"Stale rules are enabled for {self._repo_name} pull requests."
            )
            self._process_pull_requests()
        else:
            self._logger.info(
                f"Stale rules are not enabled for {self._repo_name} pull requests. Skipping!"
            )

    def _process_issues(self):
        """Process open issues in the repository."""
        issues = self._issue.get_issues(self._repo_name, state="open")

        self._logger.info(f"Process open issues for repository: {self._repo_name}")

        for issue in issues:
            # Only process if it's not a pull request
            if issue.pull_request is None:
                self._process_item(issue, self._plugin_rules.issues)

    def _process_pull_requests(self):
        """Process open pull requests in the repository."""
        pulls = self._issue.get_issues(self._repo_name, state="open")

        self._logger.info(
            f"Process open pull requests for repository: {self._repo_name}"
        )

        for pull in pulls:
            # Only process if it is a pull request
            if pull.pull_request is not None:
                self._process_item(pull, self._plugin_rules.pulls)

    def _process_item(self, item, rules):
        """Evaluate an issue or pull request against stale rules.

        Args:
            item: The issue or pull request to evaluate.
            rules: The rules to apply for determining staleness.
        """
        if self._is_exempt(item, rules):
            self._logger.info(f"Item #{item.number} has one of the exempt labels")
            return

        last_updated = item.updated_at
        now = datetime.now(tzutc())

        if self._is_stale(item, last_updated, now, rules):
            self._mark_as_stale(item, rules)
        elif self._should_close(item, last_updated, now, rules):
            self._close_item(item, rules)

    def _is_exempt(self, item, rules):
        """Check if the item has any exempt labels.

        Args:
            item: The issue or pull request to check.

        Returns:
            bool: True if exempt; False otherwise.
        """
        return any(label.name in rules.exempt_labels for label in item.labels)

    def _is_stale(self, item, last_updated, now, rules):
        """Determine if an item is considered stale.

        Args:
            item: The issue or pull request to evaluate.
            last_updated: The last updated timestamp of the item.
            now: The current timestamp.
            rules: The rules defining staleness.

        Returns:
            bool: True if the item is stale; False otherwise.
        """
        return (
            now - last_updated
        ).days >= rules.days_until_stale and not self._has_stale_label(item, rules)

    def _should_close(self, item, last_updated, now, rules):
        """Determine if an item should be closed.

        Args:
            item: The issue or pull request to evaluate.
            last_updated: The last updated timestamp of the item.
            now: The current timestamp.
            rules: The rules defining closure criteria.

        Returns:
            bool: True if the item should be closed; False otherwise.
        """
        return (now - last_updated).days >= (
            rules.days_until_stale + rules.days_until_close
        ) and self._has_stale_label(item, rules)

    def _has_stale_label(self, item, rules):
        """Check if an item has the stale label.

        Args:
            item: The issue or pull request to check.
            rules: The rules defining the stale label.

        Returns:
            bool: True if the stale label exists; False otherwise.
        """
        return any(label.name == rules.stale_label for label in item.labels)

    def _mark_as_stale(self, item, rules):
        """Mark an item as stale and add a comment.

        Args:
            item: The issue or pull request to mark as stale.
            rules: The rules defining the marking process.
        """
        self._logger.info(f"Marking item #{item.number} as stale")
        self._issue.add_labels(self._repo_name, item.number, [rules.stale_label])
        self._issue.add_comment(self._repo_name, item.number, rules.mark_comment)

    def _close_item(self, item, rules):
        """Close a stale item and add a closing comment.

        Args:
            item: The issue or pull request to close.
            rules: The rules defining the closing process.
        """
        self._logger.info(f"Closing stale item #{item.number}")
        self._issue.close_issue(self._repo_name, item.number)
        self._issue.add_comment(self._repo_name, item.number, rules.close_comment)
