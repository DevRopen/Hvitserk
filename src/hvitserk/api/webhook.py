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

import hmac
import hashlib


class Webhook:
    """Webhook Validates Github Webhook Payload"""

    def sign_request(self, webhook_secret, data):
        """Generate Payload Signature"""

        message = bytes(data, "utf-8")
        secret = bytes(webhook_secret, "utf-8")

        hash = hmac.new(secret, message, hashlib.sha1)

        return hash.hexdigest()

    def validate_request(self, webhook_secret, data, signature):
        """Validate Payload Signature"""

        sha_name, signature = signature.split("=")

        if sha_name != "sha1":
            return False

        return hmac.compare_digest(self.sign_request(webhook_secret, data), signature)
