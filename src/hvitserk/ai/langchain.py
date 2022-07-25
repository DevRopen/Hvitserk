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

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class Client:
    """A class for creating chat chains with OpenAI models."""

    @staticmethod
    def create_chat_chain(
        openai_api_key,
        model_name="gpt-4o-mini",
        temperature=0,
        prompt_template=None,
        callbacks=[],
    ):
        """
        Creates a chat chain using the specified language model and parameters.

        Args:
            openai_api_key (str): API key for accessing OpenAI services.
            model_name (str): The name of the model to use (default is "gpt-4o-mini").
            temperature (float): Controls the randomness of the output (default is 0).
            prompt_template (list): A list of message tuples for the chat prompt (default is None).
            callbacks (list): A list of callback functions to be executed during processing (default is empty).

        Returns:
            Chain: A configured chat chain that processes user input and generates responses.

        Raises:
            ValueError: If the prompt template is invalid or cannot be processed.
        """
        prompt = ChatPromptTemplate.from_messages(prompt_template)

        llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name=model_name,
            temperature=temperature,
            callbacks=callbacks,
        )

        chain = prompt | llm | StrOutputParser()

        return chain
