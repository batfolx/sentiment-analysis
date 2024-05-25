# PySentia (Sentiment Analysis)


<div align="center">
  <img src="images/PySentia.png" alt="PySentia" width="600"/>
</div>



This bot aims to pull/scrape data from news articles regarding
stocks and then analyzes the sentiment of the article to determine
whether to buy a particular stock of a company. Our broker of choice will be RobinHood.
Our news source(s) are currently Yahoo Finance and Benzinga.

ChatGPT 3.5 Turbo is actually quite amazing at what it does. We can just use that for sentiment analysis
and to pick out the companies in an article.


*DEPRECATED*

~~This is done using a variety of open source models and natural language processing tools.~~

~~The sentiment analysis will be done with the [DistilRoberta model that is based on the financial_phrasebank dataset.](https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis)~~

~~The NER (Named Entity Recognition) will be done with the [Bert Large NER](https://huggingface.co/dslim/bert-large-NER) to extract
company names.~~


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
- RH_TOKEN
  - The RobinHood API token. If this is not set, then the program will prompt you for username/password
- RH_ACCOUNT_NUMBER (optional)
  - Your account number. You can view this in the RobinHood Web in Settings -> Personal Information -> See account numbers
- OPENAI_API_KEY
  - The OpenAI API key to use

You will also need a MongoDB instance running on your local machine. You can download
MongoDB or just use Docker.


Then, you can simply run the program with a simple

```commandline
python main.py
```

## Some articles to test with

Discover being acquired by Capital One
- https://finance.yahoo.com/video/capital-one-acquire-discover-35-144002283.html



