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
class V1Label:
    """Defines a label used in GitHub issues or pull requests."""

    name: str
    description: str
    color: str


@dataclass
class V1LabelsConfig:
    """Configuration for the labels plugin."""

    enabled: bool
    labels: List[V1Label]


@dataclass
class V1AutoTriageRule:
    """Defines a rule for automatic issue triaging."""

    label: str
    terms: List[str]


@dataclass
class V1AutoTriageIssuesConfig:
    """Configuration for auto triage of issues."""

    enabled: bool
    triaged_label: str
    with_terms: List[V1AutoTriageRule]


@dataclass
class V1AutoTriagePullsConfig:
    """Configuration for auto triage of pull requests."""

    enabled: bool
    triaged_label: str
    with_terms: List[V1AutoTriageRule]


@dataclass
class V1AutoTriageConfig:
    """Configuration for the auto_triage_v1 plugin."""

    issues: V1AutoTriageIssuesConfig
    pulls: V1AutoTriagePullsConfig


@dataclass
class V1StaleConfigBase:
    """Base configuration for stale issues or pull requests."""

    enabled: bool
    days_until_stale: int
    days_until_close: int
    stale_label: str
    mark_comment: str
    close_comment: str
    exempt_labels: List[str]


@dataclass
class V1StaleConfig:
    """Configuration for the stale_v1 plugin."""

    issues: V1StaleConfigBase
    pulls: V1StaleConfigBase


@dataclass
class V1AutoClosePRMergeConflictConfig:
    """Configuration for closing PRs due to merge conflicts."""

    enabled: bool
    comment: str
    exempt_labels: List[str]


@dataclass
class V1AutoClosePRLabelsConfig:
    """Configuration for closing PRs based on labels."""

    enabled: bool
    close_labels: List[str]
    exempt_labels: List[str]


@dataclass
class V1AutoClosePRConfig:
    """Configuration for the auto_close_pr_v1 plugin."""

    merge_conflict: V1AutoClosePRMergeConflictConfig
    labels: V1AutoClosePRLabelsConfig
