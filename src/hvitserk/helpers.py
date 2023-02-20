# MIT License
#
# Copyright (c) 2022 Clivern
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

import logging
import sys

from hvitserk.api import App
from hvitserk.plugins import *
from hvitserk.api import Client
from hvitserk.config import ConfigParser
from hvitserk.config import LocalConfigReader
from hvitserk.config import RemoteConfigReader


def get_sys_logger():
    """
    Initializes and returns a system logger with the specified configuration.

    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def get_app(app_id, installation_id, private_key_path):
    """
    Retrieves and initializes an App instance using the provided credentials.
    """
    client = Client()

    result = client.fetch_access_token(
        private_key_path, int(app_id), int(installation_id)
    )

    app = App(
        int(app_id), private_key_path, int(installation_id), result["permissions"]
    )

    app.init()

    return app


def get_remote_parsed_configs(app, repo_name, config_path=".github/ropen.yml"):
    """
    Retrieves, parses, and returns the remote configuration files.
    """
    rc = RemoteConfigReader(app, repo_name, config_path)
    result = rc.get_configs()
    cp = ConfigParser(result["configs"])

    return {
        "unparsed": result["configs"],
        "parsed": cp.parse(),
        "checksum": result["checksum"],
    }


def get_local_parsed_configs(file_path):
    """
    Retrieves, parses, and returns the local configuration files.
    """
    lc = LocalConfigReader(file_path)
    result = lc.get_configs()
    cp = ConfigParser(result["configs"])

    return {
        "unparsed": result["configs"],
        "parsed": cp.parse(),
        "checksum": result["checksum"],
    }


def run_labels_v1_plugin(app, repo_name, plugin_rules, logger):
    """
    Runs the Labels V1 Plugin with the provided configurations and logger.
    """
    plugin = V1LabelsPlugin(app, repo_name, plugin_rules, logger)

    return plugin.run()


def run_auto_triage_v1_plugin(app, repo_name, plugin_rules, logger):
    """
    Run the Auto Triage V1 Plugin to label issues based on predefined rules.
    """
    plugin = V1AutoTriagePlugin(app, repo_name, plugin_rules, logger)

    return plugin.run()


def run_stale_v1_plugin(app, repo_name, plugin_rules, logger):
    """
    Run the Stale V1 Plugin for a given repository.
    """
    plugin = V1StalePlugin(app, repo_name, plugin_rules, logger)

    return plugin.run()


def run_auto_close_pull_request_v1_plugin(app, repo_name, plugin_rules, logger):
    """
    Run the Auto Close PR V1 Plugin for a given repository.
    """
    plugin = V1AutoClosePullRequestPlugin(app, repo_name, plugin_rules, logger)

    return plugin.run()
