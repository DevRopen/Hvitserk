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

from github import GithubObject
from hvitserk.exception import NotFound


class Label:
    """
    The Label class provides methods to interact with GitHub labels.
    """

    def __init__(self, app):
        """
        Initializes the Label class with the given application instance.
        """
        self._app = app

    def get_labels(self, repo):
        """
        List all labels in the specified repository.
        """
        return self._get_repo(repo).get_labels()

    def get_label(self, repo, name):
        """
        Get a specific label by name.
        """
        try:
            return self._get_repo(repo).get_label(name)
        except Exception:
            return None

    def create_label(self, repo, name, color="eb4d4b", description=GithubObject.NotSet):
        """
        Create a new label in the specified repository.
        """
        return self._get_repo(repo).create_label(
            name=name, color=color, description=description
        )

    def update_label(
        self,
        repo,
        old_name,
        new_name,
        new_color="eb4d4b",
        new_description=GithubObject.NotSet,
    ):
        """
        Update an existing label.
        """
        label = self.get_label(repo, old_name)
        if label is not None:
            label.edit(name=new_name, color=new_color, description=new_description)
        else:
            raise NotFound(f"Label '{old_name}' not found in repository '{repo}'.")

    def delete_label(self, repo, name):
        """
        Delete a label from the specified repository.
        """
        label = self.get_label(repo, name)
        if label is not None:
            label.delete()
        else:
            raise NotFound(f"Label '{name}' not found in repository '{repo}'.")

    def _get_repo(self, repo):
        """
        Helper method to get a repository object from the GitHub client.
        """
        return self._app.get_client().get_repo(repo)
