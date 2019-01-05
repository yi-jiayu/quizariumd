# Quizariumd
Automatically plays Quizarium for you using the Telegram API

## Background

[Quizarium](https://quizarium.com/) is a Telegram bot which asks trivia questions.

Quizariumd is a script which uses the Telegram API to automatically answer these questions for you, as if you sent them yourself.

## Algorithm

We use a simple heuristic to guess answers:

- First, search the [HTML version of DuckDuckGo](https://duckduckgo.com/html/) for the question
- Use BeautifulSoup to extract the text from the search results
- Look for strings in the search results that match the hints given by Quizarium

We also increase accuracy by filtering the results by eliminating stopwords and words that already occur in the question.

Instead of guessing wildly, we only guess when we are confident enough in one of the candidate answers based on the number of times it appeared in the search results.

## Performance

Because Quizariumd relies on hints to guess the answer, it will never score 5 points for any question (by answering before any hints appear).

Once the hints begin appearing, and especially after letters begin appearing, it is generally able to find the answer around 80% of the time (based on the number of questions answered in a round of 10 questions during testing).

When competing with other players, it will often be beaten to the answer, especially for easy questions. On the flip side, it is equally able to answer the more obscure questions.

## Getting started

Because Quizzariumd uses f-strings from [PEP-489](https://www.python.org/dev/peps/pep-0498/), it needs Python 3.7 and up to run.

1. Set up a virtual environment and install dependencies:
 
 ```shell
python3 -m venv venv
source venv/bin/activate  # venv/Scripts/Activate.ps1 in Powershell
pip install -r requirements.txt
 ```
 
2. Set the following environment variables: `TELEGRAM_USERNAME` (used for saving connection details), `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_PHONE`, `TELEGRAM_PASSWORD` (if set)
 
See [Creating your Telegram Application](https://core.telegram.org/api/obtaining_api_id) for details on how to get an API id and hash.
 
3. Run `telegram.py`:

```shell
./quizariumd
```

## Improvements

Besides trying to guess answers, it should also be possible to build a questions and answers database from chat history or based on questions encountered, and use it to answer questions immediately.
