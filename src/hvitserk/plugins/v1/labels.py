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

from hvitserk.api import Label
from hvitserk.util import Logger


class Labels:
    """Labels Plugin"""

    def __init__(self, app, repo_name, plugin_rules, logger):
        self._app = app
        self._label = Label(self._app)
        self._repo_name = repo_name
        self._plugin_rules = plugin_rules
        self._logger = Logger().get_logger(__name__) if logger is None else logger

    def run(self):
        """Run the Plugin"""
        if not self._plugin_rules.enabled:
            self._logger.info(
                f"Labels V1 Plugin is disabled for {self._repo_name}. Skipping."
            )
            return True

        gh_labels = self._label.get_labels(self._repo_name)
        gh_label_names = {label.name: label for label in gh_labels}

        self._logger.info(f"Start labels sync for repository {self._repo_name}")

        # Synchronize labels based on configuration
        for cfg_label in self._plugin_rules.labels:
            if cfg_label.name in gh_label_names:
                # Update existing label properties if necessary
                gh_label = gh_label_names[cfg_label.name]

                if (
                    gh_label.color != cfg_label.color
                    or gh_label.description != cfg_label.description
                ):
                    self._logger.info(
                        f"Updating existing label {cfg_label.name} in repository {self._repo_name}"
                    )

                    self._label.update_label(
                        self._repo_name,
                        cfg_label.name,
                        cfg_label.name,
                        cfg_label.color,
                        cfg_label.description,
                    )
            else:
                # Create new label if it doesn't exist
                self._logger.info(
                    f"Creating new label {cfg_label.name} in repository {self._repo_name}"
                )

                self._label.create_label(
                    self._repo_name,
                    cfg_label.name,
                    cfg_label.color,
                    cfg_label.description,
                )

        # Remove labels that are not in the configuration
        for gh_label in gh_labels:
            if gh_label.name not in (cfg_label.name for cfg_label in self._cfg_labels):
                self._logger.info(
                    f"Deleting label {gh_label.name} from repository {self._repo_name}"
                )

                self._label.delete_label(self._repo_name, gh_label.name)

        self._logger.info(f"Finished labels sync for repository {self._repo_name}")

        return True
