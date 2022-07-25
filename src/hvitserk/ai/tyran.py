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

import requests
from hvitserk.util import Logger


class Tyran(object):
    """Tyran Client https://github.com/Clivern/Tyran"""

    def __init__(self, base_url, api_key, logger=None):
        self._base_url = base_url
        self._api_key = api_key
        self._logger = Logger().get_logger(__name__) if logger is None else logger

    def create_document(self, content, metadata):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": self._api_key,
        }

        data = {"content": content, "metadata": metadata}

        self._logger.info("Create a new document in tyran service API")

        return requests.post(
            f"{self._base_url}/api/v1/document", json=data, headers=headers
        )

    def get_document(self, uuid):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": self._api_key,
        }

        self._logger.info(f"Fetch document with id {uuid} from tyran service API")

        return requests.get(f"{self._base_url}/api/v1/document/{uuid}", headers=headers)

    def delete_document(self, uuid):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": self._api_key,
        }

        self._logger.info(f"Delete document with id {uuid} from tyran service API")

        return requests.delete(
            f"{self._base_url}/api/v1/document/{uuid}", headers=headers
        )

    def search_documents(self, text, metadata, limit):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-API-Key": self._api_key,
        }

        data = {"text": text, "limit": limit, "metadata": metadata}

        self._logger.info("Search documents in tyran service API")

        return requests.post(
            f"{self._base_url}/api/v1/document/search", json=data, headers=headers
        )
