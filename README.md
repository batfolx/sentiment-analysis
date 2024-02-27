# Sentiment Analysis

This bot aims to pull/scrape data from news articles regarding
stocks and then analyzes the sentiment of the article to determine
whether to buy a particular stock of a company. Our broker of choice will be RobinHood.
Our news source(s) are currently Yahoo Finance and Benzinga.

This is done using a variety of open source
models and natural language processing tools.

The sentiment analysis will be done with the [DistilRoberta model that is based on the financial_phrasebank dataset.](https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis)

The NER (Named Entity Recognition) will be done with the [Bert Large NER](https://huggingface.co/dslim/bert-large-NER) to extract
company names.


## Setup


Install dependencies with `pip`

```commandline
pip install -r requirements.txt
```


## RobinHood Unofficial API docs

https://github.com/sanko/Robinhood


## How to run

You will need to set some environment variables

- BENZINGA_API_KEY
  - the API key given by Benzinga to grab articles from
- RH_USERNAME
  - RobinHood username
- RH_PASSWORD
  - RobinHood password



## Some articles I want to test with

Discover being acquired by Capital One
- https://finance.yahoo.com/video/capital-one-acquire-discover-35-144002283.html



