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


class Summarize:
    """A class for summarizing text using a language model."""

    @staticmethod
    def summarize(
        openai_api_key, text, model_name="gpt-4o-mini", temperature=0, callbacks=[]
    ):
        """
        Summarizes the given text using a specified language model.

        Args:
            openai_api_key (str): API key for accessing OpenAI services.
            text (str): The text to be summarized.
            model_name (str): The name of the model to use for summarization (default is "gpt-4o-mini").
            temperature (float): Sampling temperature for the model (default is 0).
            callbacks (list): A list of callback functions to be executed during processing (default is empty).

        Returns:
            str: The summarized version of the input text.

        Raises:
            Exception: If there is an error during the summarization process.
        """
        chain = LangchainClient.create_chat_chain(
            openai_api_key,
            model_name,
            temperature,
            [
                ("system", "You are a helpful assistant that summarizes text."),
                ("user", f"Summarize the following text:\n{text}"),
            ],
            callbacks,
        )

        return chain.invoke({"text": text})
