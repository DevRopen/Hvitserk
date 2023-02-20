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

from .v1.configs import *


class ConfigParser:
    """
    A class for parsing and processing configuration data for GitHub issue management.
    """

    def __init__(self, configs: Dict = {}):
        """
        Initialize the ConfigParser with configuration data.

        Args:
            configs (Dict): A dictionary containing the configuration data.
        """
        self._configs = configs
        self._parsed = {}

    def parse(self) -> Dict:
        """
        Parse the entire configuration.

        Returns:
            Dict: A dictionary containing the parsed configuration.
        """
        self._parsed["plugins"] = self.parse_plugins(self._configs.get("plugins", {}))

        return self._parsed

    def parse_plugins(self, plugins_data: Dict) -> Dict:
        """
        Parse the plugins configuration.

        Args:
            plugins_data (Dict): A dictionary containing plugin configurations.

        Returns:
            Dict: A dictionary of parsed plugin configurations.
        """
        parsed_plugins = {}

        for plugin_name, plugin_data in plugins_data.items():
            if plugin_name == "auto_triage_v1":
                parsed_plugins[plugin_name] = self._parse_auto_triage_v1(plugin_data)
            elif plugin_name == "stale_v1":
                parsed_plugins[plugin_name] = self._parse_stale_v1(plugin_data)
            elif plugin_name == "labels_v1":
                parsed_plugins[plugin_name] = self._parse_labels_v1(plugin_data)
            elif plugin_name == "auto_close_pr_v1":
                parsed_plugins[plugin_name] = self._parse_auto_close_pr_v1(plugin_data)

        return parsed_plugins

    def _parse_labels_v1(self, labels_v1_data: Dict) -> V1LabelsConfig:
        """
        Parse the labels_v1 plugin configuration.

        Args:
            labels_v1_data (Dict): A dictionary containing labels plugin configurations.

        Returns:
            V1LabelsConfig: A structured configuration object for labels.
        """
        enabled = labels_v1_data.get("enabled", False)

        # Extracting labels from the provided data
        labels = []
        for label_data in labels_v1_data.get("labels", []):
            label = V1Label(
                name=label_data.get("name"),
                description=label_data.get("description"),
                color=label_data.get("color"),
            )
            labels.append(label)

        return V1LabelsConfig(enabled=enabled, labels=labels)

    def _parse_auto_triage_v1(self, auto_triage_v1_data: Dict) -> V1AutoTriageConfig:
        """
        Parse the auto_triage_v1 plugin configuration.

        Args:
            auto_triage_v1_data (Dict): A dictionary containing auto triage plugin configurations.

        Returns:
            V1AutoTriageConfig: A structured configuration object for auto triage.
        """

        # Parse issues configuration
        issues_config = auto_triage_v1_data.get("issues", {})
        issues_enabled = issues_config.get("enabled", False)
        issues_triaged_label = issues_config.get("triagedLabel", "triaged")

        issues_with_terms_rules = []
        for rule in issues_config.get("with_terms", []):
            issues_with_terms_rules.append(
                V1AutoTriageRule(label=rule.get("label"), terms=rule.get("terms", []))
            )

        issues_config_obj = V1AutoTriageIssuesConfig(
            enabled=issues_enabled,
            triaged_label=issues_triaged_label,
            with_terms=issues_with_terms_rules,
        )

        # Parse pulls configuration
        pulls_config = auto_triage_v1_data.get("pulls", {})
        pulls_enabled = pulls_config.get("enabled", False)
        pulls_triaged_label = pulls_config.get("triagedLabel", "triaged")

        pulls_with_terms_rules = []
        for rule in pulls_config.get("with_terms", []):
            pulls_with_terms_rules.append(
                V1AutoTriageRule(label=rule.get("label"), terms=rule.get("terms", []))
            )

        pulls_config_obj = V1AutoTriagePullsConfig(
            enabled=pulls_enabled,
            triaged_label=pulls_triaged_label,
            with_terms=pulls_with_terms_rules,
        )

        return V1AutoTriageConfig(issues=issues_config_obj, pulls=pulls_config_obj)

    def _parse_stale_v1(self, stale_v1_data: Dict) -> V1StaleConfig:
        """
        Parse the stale_v1 plugin configuration.

        Args:
            stale_v1_data (Dict): A dictionary containing stale plugin configurations.

        Returns:
            V1StaleConfig: A structured configuration object for stale plugin.
        """

        # Parse issues configuration
        issues_config = stale_v1_data.get("issues", {})
        issues_enabled = issues_config.get("enabled", False)
        days_until_stale_issues = issues_config.get("daysUntilStale", 0)
        days_until_close_issues = issues_config.get("daysUntilClose", 0)
        stale_label_issues = issues_config.get("staleLabel", "stale")
        mark_comment_issues = issues_config.get("markComment", "")
        close_comment_issues = issues_config.get("closeComment", "")
        exempt_labels_issues = issues_config.get("exemptLabels", [])

        issues_config_obj = V1StaleConfigBase(
            enabled=issues_enabled,
            days_until_stale=days_until_stale_issues,
            days_until_close=days_until_close_issues,
            stale_label=stale_label_issues,
            mark_comment=mark_comment_issues,
            close_comment=close_comment_issues,
            exempt_labels=exempt_labels_issues,
        )

        # Parse pulls configuration
        pulls_config = stale_v1_data.get("pulls", {})
        pulls_enabled = pulls_config.get("enabled", False)
        days_until_stale_pulls = pulls_config.get("daysUntilStale", 0)
        days_until_close_pulls = pulls_config.get("daysUntilClose", 0)
        stale_label_pulls = pulls_config.get("staleLabel", "stale")
        mark_comment_pulls = pulls_config.get("markComment", "")
        close_comment_pulls = pulls_config.get("closeComment", "")
        exempt_labels_pulls = pulls_config.get("exemptLabels", [])

        pulls_config_obj = V1StaleConfigBase(
            enabled=pulls_enabled,
            days_until_stale=days_until_stale_pulls,
            days_until_close=days_until_close_pulls,
            stale_label=stale_label_pulls,
            mark_comment=mark_comment_pulls,
            close_comment=close_comment_pulls,
            exempt_labels=exempt_labels_pulls,
        )

        return V1StaleConfig(issues=issues_config_obj, pulls=pulls_config_obj)

    def _parse_auto_close_pr_v1(
        self, auto_close_pr_v1_data: Dict
    ) -> V1AutoClosePRConfig:
        """
        Parse the auto_close_pr_v1 plugin configuration.

        Args:
            auto_close_pr_v1_data (Dict): A dictionary containing auto close PR plugin configurations.

        Returns:
            V1AutoClosePRConfig: A structured configuration object for auto close PR plugin.
        """

        # Parse merge conflict configuration
        merge_conflict_config = auto_close_pr_v1_data.get("mergeConflict", {})
        merge_conflict_enabled = merge_conflict_config.get("enabled", False)
        merge_conflict_comment = merge_conflict_config.get("comment", "")
        merge_conflict_exempt_labels = merge_conflict_config.get("exemptLabels", [])

        merge_conflict_config_obj = V1AutoClosePRMergeConflictConfig(
            enabled=merge_conflict_enabled,
            comment=merge_conflict_comment,
            exempt_labels=merge_conflict_exempt_labels,
        )

        # Parse labels configuration
        labels_config = auto_close_pr_v1_data.get("labels", {})
        labels_enabled = labels_config.get("enabled", False)
        labels_close_labels = labels_config.get("closeLabels", [])
        labels_exempt_labels = labels_config.get("exemptLabels", [])

        labels_config_obj = V1AutoClosePRLabelsConfig(
            enabled=labels_enabled,
            close_labels=labels_close_labels,
            exempt_labels=labels_exempt_labels,
        )

        return V1AutoClosePRConfig(
            merge_conflict=merge_conflict_config_obj, labels=labels_config_obj
        )
