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


class AutoClosePullRequest:
    """Auto Close Pull Request Plugin"""

    def __init__(self, app, repo_name, plugin_rules, logger=None):
        self._app = app
        self._issue = Issue(self._app)
        self._repo_name = repo_name
        self._plugin_rules = plugin_rules
        self._logger = Logger().get_logger(__name__) if logger is None else logger

    def run(self):
        """Run the Plugin"""
        self._logger.info(
            f"Running Auto Close Pull Request Plugin for repository: {self._repo_name}"
        )
        self._process_pull_requests()

    def _process_pull_requests(self):
        """Process open pull requests and close them based on rules."""
        pulls = self._issue.get_issues(self._repo_name, "open")

        for pull in pulls:
            if pull.pull_request is None:
                continue  # Skip non-pull request issues

            pull_number = pull.number
            pull_labels = [label.name for label in pull.labels]

            # Check for merge conflicts based closure
            if self._plugin_rules.mergeConflict.enabled and pull.mergeable is False:
                self._close_pull_request(
                    pull_number, self._plugin_rules.mergeConflict.comment
                )
                continue

            # Check for label-based closure
            if self._plugin_rules.labels.enabled:
                if any(
                    label in pull_labels
                    for label in self._plugin_rules.labels.closeLabels
                ):
                    if not any(
                        label in pull_labels
                        for label in self._plugin_rules.labels.exemptLabels
                    ):
                        self._close_pull_request(
                            pull_number, self._plugin_rules.labels.comment
                        )

    def _close_pull_request(self, pull_number, comment):
        """Close the pull request and post a comment."""
        try:
            # Post a comment before closing
            self._issue.add_comment(self._repo_name, pull_number, comment)
            # Close the pull request
            self._issue.close_issue(self._repo_name, pull_number)
            self._logger.info(f"Closed PR #{pull_number} with comment: {comment}")
        except Exception as e:
            self._logger.error(
                f"Failed to close PR #{pull_number} in repository {self._repo_name}: {str(e)}"
            )
