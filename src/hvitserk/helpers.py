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
from hvitserk.api import Client
from hvitserk.api import App
from hvitserk.config import RemoteConfigReader
from hvitserk.config import LocalConfigReader
from hvitserk.config import ConfigParser
from hvitserk.plugins import LabelsV1Plugin
from hvitserk.plugins import AutoTriageV1Plugin
from hvitserk.plugins import StaleV1Plugin


def get_sys_logger():
    """
    Initializes and returns a system logger with the specified configuration.

    Returns:
        logging.Logger: A logger instance set to the DEBUG level with a console handler.
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

    Args:
        app_id (int): The ID of the application.
        installation_id (int): The ID of the installation.
        private_key_path (str): The path to the private key file.

    Returns:
        App: An initialized App instance.
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

    Args:
        app (App): The App instance.
        repo_name (str): The name of the repository.
        config_path (str, optional): The path to the configuration file. Defaults to ".github/ropen.yml".

    Returns:
        dict: A dictionary containing the unparsed configurations, parsed configurations, and the checksum.
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

    Args:
        file_path (str): The path to the local configuration file.

    Returns:
        dict: A dictionary containing the unparsed configurations, parsed configurations, and the checksum.
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
    Runs the LabelsV1Plugin with the provided configurations and logger.

    Args:
        app (App): The App instance.
        repo_name (str): The name of the repository.
        plugin_rules: Object containing labels rules.
        logger (logging.Logger): The logger instance.

    Returns:
        Any: The result of running the LabelsV1Plugin.
    """
    labels_v1_plugin = LabelsV1Plugin(app, repo_name, plugin_rules, logger)

    return labels_v1_plugin.run()


def run_auto_triage_v1_plugin(app, repo_name, plugin_rules, logger):
    """
    Run the Auto Triage V1 Plugin to label issues based on predefined rules.

    Args:
        app: Application object with configuration and API clients.
        repo_name (str): Name of the repository to triage.
        plugin_rules: Object containing auto-triage rules.
        logger: Logger object for operations and errors.

    Returns:
        bool: True if auto-triage completes successfully, False otherwise.
    """
    auto_triage_v1_plugin = AutoTriageV1Plugin(app, repo_name, plugin_rules, logger)

    return auto_triage_v1_plugin.run()


def run_stale_v1_plugin(app, repo_name, stale_rules, logger):
    """
    Run the Stale V1 Plugin for a given repository.

    Args:
        app (object): The application instance.
        repo_name (str): The name of the repository to run the plugin on.
        stale_rules (dict): A dictionary containing the stale rules configuration.
        logger (object): The logger object for logging messages.

    Returns:
        The result of running the Stale V1 Plugin.
    """
    stale_v1_plugin = StaleV1Plugin(app, repo_name, stale_rules, logger)

    return stale_v1_plugin.run()
