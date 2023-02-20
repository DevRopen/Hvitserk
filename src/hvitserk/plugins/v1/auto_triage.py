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


class AutoTriage:
    """Auto Triage Plugin"""

    def __init__(self, app, repo_name, plugin_rules, logger):
        self._app = app
        self._issue = Issue(self._app)
        self._repo_name = repo_name
        self._plugin_rules = plugin_rules
        self._logger = Logger().get_logger(__name__) if logger is None else logger

    def run(self):
        """Run the Plugin"""
        self._logger.info(
            f"Running Auto Triage V1 Plugin for repository: {self._repo_name}"
        )

        if self._plugin_rules.issues.enabled:
            self._logger.info(
                f"Auto Triage V1 Plugin is enabled for {self._repo_name} issues."
            )
            self._process_items("issues", self._plugin_rules.issues)
        else:
            self._logger.info(
                f"Auto Triage V1 Plugin is disabled for {self._repo_name} issues. Skipping!"
            )

        if self._plugin_rules.pulls.enabled:
            self._logger.info(
                f"Auto Triage V1 Plugin is enabled for {self._repo_name} pull requests."
            )
            self._process_items("pulls", self._plugin_rules.pulls)
        else:
            self._logger.info(
                f"Auto Triage V1 Plugin is disabled for {self._repo_name} pull requests. Skipping!"
            )

    def _process_items(self, item_type, rules):
        items = self._issue.get_issues(self._repo_name, "open")

        for item in items:
            if item_type == "pulls" and item.pull_request is None:
                continue
            if item_type == "issues" and item.pull_request is not None:
                continue

            item_title = item.title.lower()
            item_body = item.body.lower()
            item_number = item.number
            item_labels = [label.name for label in item.labels]

            # Skip if the item has already been triaged
            if rules.triagedLabel in item_labels:
                self._logger.info(
                    f"Skip triaged {item_type[:-1]} #{item_number} in repository {self._repo_name}"
                )
                continue

            labels_to_add = []

            for term_rule in rules.with_terms:
                if any(
                    term.lower() in item_title or term.lower() in item_body
                    for term in term_rule.terms
                ):
                    labels_to_add.append(term_rule.label)

            if labels_to_add:
                labels_to_add.append(rules.triagedLabel)

                try:
                    self._issue.add_labels(self._repo_name, item_number, labels_to_add)

                    self._logger.info(
                        f"Added labels {labels_to_add} to {item_type[:-1]} #{item_number} in repository {self._repo_name}"
                    )
                except Exception as e:
                    self._logger.error(
                        f"Failed to add labels {labels_to_add} to {item_type[:-1]} #{item_number} in repository {self._repo_name}: {str(e)}"
                    )
            else:
                self._logger.info(
                    f"{item_type[:-1]} #{item_number} in repository {self._repo_name} doesn't have any known terms, Skipping triage"
                )
