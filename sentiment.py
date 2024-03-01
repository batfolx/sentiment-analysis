import typing
import re
import json

import openai.types.chat.chat_completion
from openai import OpenAI
from transformers import pipeline, set_seed, AutoTokenizer, TFAutoModelForTokenClassification, Pipeline

import common

set_seed(42)


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


def get_ner_pipeline() -> Pipeline:
    """
    Gets the Named Entity Recognition pipeline needed to pull out
    :return: The NER pipeline
    """
    # 'NER' is Named Entity Recognition
    ner_tokenizer = AutoTokenizer.from_pretrained("dslim/bert-large-NER")
    ner_model = TFAutoModelForTokenClassification.from_pretrained("dslim/bert-large-NER")
    ner_pipeline: Pipeline = pipeline("ner", model=ner_model, tokenizer=ner_tokenizer)
    return ner_pipeline


def get_financial_classifier_pipeline() -> Pipeline:
    """
    Get the pipeline with the model that was trained on the financial workbank
    :return:
    """
    # to see if a news headline is positive or negative
    financial_classifier: Pipeline = pipeline(
        model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis",
        top_k=None
    )
    return financial_classifier


def get_gpt_pipeline() -> Pipeline:
    # might use this in the future idk
    openai_gpt2_pipeline: Pipeline = pipeline('text-generation', model='openai-community/gpt2-xl')
    return openai_gpt2_pipeline


def is_positive_sentiment(p: Pipeline, text: str):
    """
    Analyzes a piece of text for the sentiment
    :param p: the Pipeline to run the sentiment analysis on
    :param text: Text to analyze
    :return:
    """
    # >>> [[{'label': 'positive', 'score': 0.5302914977073669}, {'label': 'negative', 'score': 0.19330111145973206},
    # {'label': 'neutral', 'score': 0.276407390832901}]]
    answer = p(text)
    answer = answer[0]
    positive_score = 0
    negative_score = 0
    neutral_score = 0
    for sentiment in answer:
        sentiment: dict = sentiment
        label = sentiment.get('label')
        score = sentiment.get('score')
        if label == 'positive':
            positive_score = score
        elif label == 'negative':
            negative_score = score
        elif label == 'neutral':
            neutral_score = score

    return positive_score > negative_score and positive_score > neutral_score


def extract_company_names(p: Pipeline, text: str, threshold_score: float = 0.75) -> typing.List[str]:
    answers: typing.List[dict] = p(text)
    key_companies = [entity['word'] for entity in answers if
                     entity['entity'] == 'I-ORG' or entity['entity'] == 'B-ORG' and entity['score'] > threshold_score]
    return key_companies


def extract_company_names_gpt(p: Pipeline, text: str) -> list:
    prompt = 'Given this text, can you try to pick out the company names?'
    answer = p(f'{prompt}: {text}')
    return answer


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
