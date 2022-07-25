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

from .langchain import Client as LangchainClient


class Labeler:
    """A class for labeling GitHub issues based on their content."""

    @staticmethod
    def label(
        openai_api_key,
        title,
        body,
        labels=[],
        model_name="gpt-4o-mini",
        temperature=0,
        callbacks=[],
    ):
        """
        Labels a GitHub issue based on its title and body.

        Args:
            openai_api_key (str): API key for accessing OpenAI services.
            title (str): The title of the GitHub issue.
            body (str): The body content of the GitHub issue.
            labels (list): A list of possible labels to assign (default is empty).
            model_name (str): The name of the model to use for labeling (default is "gpt-4o-mini").
            temperature (float): Controls the randomness of the model's output (default is 0).
            callbacks (list): A list of callback functions to execute during processing (default is empty).

        Returns:
            list: A list of labels that best fit the issue, stripped of whitespace.

        Raises:
            ValueError: If no valid labels are provided or if an error occurs during processing.
        """
        prompt = f"""
        Given the following GitHub issue, assign the most appropriate label(s) from this list:
        {', '.join(labels)}

        Issue Title: {title}
        Issue Body: {body}

        Return only the label(s) that best fit the issue, separated by commas if multiple labels apply.
        """

        chain = LangchainClient.create_chat_chain(
            openai_api_key,
            model_name,
            temperature,
            [
                (
                    "system",
                    "You are an AI assistant that labels GitHub issues accurately.",
                ),
                ("user", prompt),
            ],
            callbacks,
        )

        response = chain.invoke({"title": title, "body": body})

        return [label.strip() for label in response.split(",")]
