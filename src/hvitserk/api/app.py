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

from github import Auth
from github import Github
from hvitserk.util import Logger
from hvitserk.util import FileSystem
from hvitserk.api.client import Client


class App(Client):
    """
    The `App` class is responsible for initializing a GitHub client using
    GitHub App authentication.
    """

    def __init__(
        self,
        app_id,
        private_key_path,
        installation_id,
        token_permission,
        file_system=None,
        logger=None,
    ):
        """
        Initializes the App class with the given parameters.
        """
        super().__init__(file_system, logger)
        self._app_id = app_id
        self._private_key_path = private_key_path
        self._installation_id = installation_id
        self._token_permission = token_permission
        self._logger = Logger().get_logger(__name__) if logger is None else logger
        self._file_system = FileSystem() if file_system is None else file_system

    def init(self):
        """
        Initializes the GitHub client using the GitHub App authentication.
        Reads the private key from the specified file path and creates an
        authenticated GitHub client.
        """
        private_key = self._file_system.read_file(self._private_key_path)

        self._logger.info(
            "Create a new client for app with id {} and installation with id {}".format(
                self._app_id, self._installation_id
            )
        )

        auth = Auth.AppAuth(self._app_id, private_key).get_installation_auth(
            self._installation_id, self._token_permission
        )

        self._client = Github(auth=auth)

    def get_client(self):
        """
        Returns the initialized GitHub client.
        """
        return self._client

    def get_logger(self):
        """
        Returns the logger instance.
        """
        return self._logger
