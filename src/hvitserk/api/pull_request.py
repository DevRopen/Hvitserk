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


class PullRequest:
    """
    The PullRequest class provides methods to interact with GitHub repositories,
    specifically for operations related to branches and pull requests.
    """

    def __init__(self, app):
        """
        Initializes the PullRequest class with the given application instance.
        """
        self._app = app

    def get_default_branch(self, repo):
        """
        Retrieves the default branch of a specified repository.
        """
        return self._get_repo(repo).default_branch

    def create_branch(self, repo, source_branch, new_branch):
        """
        Creates a new branch in the specified repository.
        """
        source_obj = self._get_repo(repo).get_branch(source_branch)
        return self._get_repo(repo).create_git_ref(
            ref=f"refs/heads/{new_branch}", sha=source_obj.commit.sha
        )

    def delete_branch(self, repo, branch_name):
        """
        Deletes a branch in the specified repository.
        """
        ref = self._get_repo(repo).get_git_ref(f"heads/{branch_name}")
        ref.delete()

    def create_commit(self, repo, branch, file_path, file_content, commit_message):
        """
        Creates a new commit in the specified repository and branch.
        """
        return self._get_repo(repo).create_file(
            path=file_path, message=commit_message, content=file_content, branch=branch
        )

    def open_pr(self, repo, title, body, base_branch, head_branch):
        """
        Opens a new pull request in the specified repository.
        """
        return self._get_repo(repo).create_pull(
            title=title, body=body, head=head_branch, base=base_branch
        )

    def _get_repo(self, repo):
        """
        Helper method to get a repository object from the GitHub client.
        """
        return self._app.get_client().get_repo(repo)
