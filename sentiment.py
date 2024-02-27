import typing
from transformers import pipeline, set_seed, AutoTokenizer, TFAutoModelForTokenClassification, Pipeline

set_seed(42)


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
