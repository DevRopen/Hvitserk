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

import yaml
import hashlib


class RemoteConfigReader:
    """
    A class for loading configuration files from a remote repository.
    """

    def __init__(self, app, repo, file_path):
        """
        Initializes the RemoteConfigReader instance.
        """
        self._app = app
        self._repo = repo
        self._file_path = file_path

    def get_configs(self):
        """
        Retrieves the content of the specified configuration file from the remote repository.
        """
        repo = self._app.get_client().get_repo(self._repo)

        try:
            content = repo.get_contents(self._file_path)
        except Exception:
            return None

        return {
            "configs": yaml.safe_load(content.decoded_content.decode()),
            "checksum": hashlib.sha256(
                content.decoded_content.decode().encode()
            ).hexdigest(),
        }
