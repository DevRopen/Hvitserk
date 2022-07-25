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

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Label:
    """Represents a label for categorizing issues or pull requests."""

    name: str
    description: str
    color: str


@dataclass
class AutoTriageRule:
    """Defines a rule for automatic issue triaging."""

    label: str
    terms: List[str]


@dataclass
class AutoTriageConfig:
    """Configuration for the auto-triage plugin."""

    enabled: bool
    triagedLabel: str
    issues: List[AutoTriageRule]
    pulls: List[AutoTriageRule]


@dataclass
class StaleConfig:
    """Configuration for the stale plugin."""

    enabled: bool
    issues: Dict[str, Any]
    pulls: Dict[str, Any]
    exemptLabels: List[str]


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
        self._parsed["labels"] = self.parse_labels(self._configs.get("labels", []))
        self._parsed["plugins"] = self.parse_plugins(self._configs.get("plugins", {}))

        return self._parsed

    def parse_labels(self, label_data: List[dict]) -> List[Label]:
        """
        Parse the labels configuration.

        Args:
            label_data (List[dict]): A list of dictionaries, each representing a label.

        Returns:
            List[Label]: A list of Label objects.
        """
        return [Label(**label) for label in label_data]

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
                parsed_plugins[plugin_name] = self.parse_auto_triage(plugin_data)
            elif plugin_name == "stale_v1":
                parsed_plugins[plugin_name] = self.parse_stale(plugin_data)

        return parsed_plugins

    def parse_auto_triage(self, auto_triage_data: Dict) -> AutoTriageConfig:
        """
        Parse the auto-triage plugin configuration.

        Args:
            auto_triage_data (Dict): A dictionary containing auto-triage configuration.

        Returns:
            AutoTriageConfig: An object representing the parsed auto-triage configuration.
        """
        issues_rules = [
            AutoTriageRule(**rule) for rule in auto_triage_data.get("issues", [])
        ]

        pulls_rules = [
            AutoTriageRule(**rule) for rule in auto_triage_data.get("pulls", [])
        ]

        return AutoTriageConfig(
            enabled=auto_triage_data.get("enabled", False),
            triagedLabel=auto_triage_data.get("triagedLabel", "triaged"),
            issues=issues_rules,
            pulls=pulls_rules,
        )

    def parse_stale(self, stale_data: Dict) -> StaleConfig:
        """
        Parse the stale plugin configuration.

        Args:
            stale_data (Dict): A dictionary containing stale plugin configuration.

        Returns:
            StaleConfig: An object representing the parsed stale configuration.
        """
        return StaleConfig(
            enabled=stale_data.get("enabled", False),
            issues=stale_data.get("issues", {}),
            pulls=stale_data.get("pulls", {}),
            exemptLabels=stale_data.get("exemptLabels", []),
        )
