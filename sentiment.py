import common
import json
import openai.types.chat.chat_completion
import typing
import re

from openai import OpenAI


def parse_json_from_markdown(markdown_text: str) -> list:
    """
    Parses Markdown-like JSON from a given text
    :param markdown_text: The markdown-like text
    :return: A list of JSON objects
    """
    pattern = re.compile(r'```json(.*?)```', re.DOTALL)
    matches = pattern.findall(markdown_text)
    parsed_json_list = []
    for match in matches:
        try:
            parsed_json = json.loads(match)
            parsed_json_list.append(parsed_json)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")

    return parsed_json_list


def extract_company_names_openai(article_id: int, article_text: str) -> typing.Optional[dict]:
    """
    Extracts the company names with ChatGPT 3.5 turbo
    :param article_id:
    :param article_text: The article text to analyze
    :return: A dictionary
    """
    prompt = """
    Given an article and if there is any GOOD news of a company investing 
    in other companies or some GOOD news from this company has been announced, give me a JSON response with
    the company that is announcing the good news and give me the smaller companies that it is investing in, if any.
    Make the big company have the key of "parentCompany" and make the smaller companies a list of strings called 'subCompanies'.
    If there are any company tickers, include them in a separate key called 'parentCompanyTicker' and 'subCompanyTickers'.
    Include a field called sentiment called 'sentiment' if it is positive, neutral, or negative sentiment.
    """
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": prompt},
            {'role': 'system', 'content': article_text}
        ]
    )

    if not completion.choices:
        return None

    choice: openai.types.chat.chat_completion.Choice = completion.choices[0]
    content = choice.message.content
    try:
        return json.loads(content)
    except Exception as e:
        print(f'({common.get_formatted_time()}){common.get_calling_func_name()}: '
              f'Failed to parse JSON response from article ID {article_id}: {e} ')
        return None
