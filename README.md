[![Build Status](https://dev.azure.com/yijiayu/quizariumd/_apis/build/status/yi-jiayu.quizariumd?branchName=master)](https://dev.azure.com/yijiayu/quizariumd/_build/latest?definitionId=1?branchName=master)
[![Build Status](https://travis-ci.com/yi-jiayu/quizariumd.svg?branch=master)](https://travis-ci.com/yi-jiayu/quizariumd)
[![codecov](https://codecov.io/gh/yi-jiayu/quizariumd/branch/master/graph/badge.svg)](https://codecov.io/gh/yi-jiayu/quizariumd)

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

## Sample output
```shell
$ ./quizariumd 
INFO:telethon.network.mtprotosender:Connecting to 91.108.56.150:443/TcpFull...
INFO:telethon.network.mtprotosender:Connection to 91.108.56.150:443/TcpFull complete!
INFO:root:CHAT_ID=365638834 getting search results for question: Which dog is named for the German word for muzzle
INFO:root:CHAT_ID=365638834 got hint: _ _ _ _ _ _ _ _ _
INFO:root:CHAT_ID=365638834 got candidate answers: Counter({'harnesses': 7, 'questions': 4, 'wordhippo': 4, 'wikipedia': 4, 'agitation': 2, 'thoughtco': 2, 'equipment': 2, 'following': 1, 'larapedia': 1, 'schnauzer': 1, 'muzziness': 1, 'direction': 1, 'otherwise': 1, 'deutscher': 1, 'sometimes': 1, 'indicates': 1, 'intricate': 1, 'frequency': 1, 'available': 1, 'dog_names': 1, 'recipient': 1, 'resulting': 1, 'varieties': 1, 'retriever': 1, 'malleable': 1, 'cesarsway': 1, 'purposely': 1, 'intensity': 1, 'elongated': 1, 'universal': 1, 'miniature': 1, 'developed': 1, 'inscribed': 1, 'shortened': 1})
INFO:root:CHAT_ID=365638834 replying with answer: harnesses
INFO:root:CHAT_ID=365638834 got hint: _ c _ _ _ _ _ _ _
INFO:root:CHAT_ID=365638834 got candidate answers: Counter({'schnauzer': 1})
INFO:root:CHAT_ID=365638834 replying with answer: schnauzer
INFO:root:CHAT_ID=365638834 getting search results for question: What color flower should never be sent to newlyweds in Hong Kong?
INFO:root:CHAT_ID=365638834 got hint: _ _ _ _ _
INFO:root:CHAT_ID=365638834 got candidate answers: Counter({'china': 7, 'every': 7, 'white': 6, 'aveda': 5, 'xhtml': 4, 'gifts': 4, 'email': 4, 'bring': 4, 'paper': 4, 'bride': 4, 'class': 3, 'xmlns': 3, 'hands': 3, 'style': 3, 'poppy': 3, 'often': 2, 'avoid': 2, 'gives': 2, 'house': 2, 'coins': 2, 'guide': 2, 'crème': 2, 'ideas': 2, 'world': 2, 'parts': 2, 'rover': 2, 'malva': 2, 'leave': 2, 'seeds': 2, 'great': 1, 'facts': 1, 'asian': 1, 'debby': 1, 'getty': 1, 'quite': 1, 'blood': 1, 'ce_hk': 1, 'night': 1, 'works': 1, 'black': 1, 'learn': 1, 'allow': 1, 'place': 1, 'roses': 1, 'known': 1, 'spray': 1, 'drive': 1, 'photo': 1, 'condé': 1, 'weeds': 1, 'deane': 1, 'ruins': 1, 'begin': 1, 'notes': 1, 'proof': 1, 'carry': 1, 'taste': 1, 'image': 1, 'along': 1, 'sites': 1, 'finds': 1, 'dress': 1, 'aisle': 1, 'girls': 1, 'three': 1, 'ivory': 1, 'groom': 1, 'light': 1, 'means': 1, 'since': 1, 'women': 1, '53470': 1, '10001': 1, 'https': 1, '16783': 1, 'coast': 1, 'soups': 1, 'meals': 1, 'mixed': 1, 'sweet': 1, 'japan': 1, 'prior': 1, 'party': 1, 'thank': 1, 'aroma': 1, 'heart': 1, 'plant': 1, 'quick': 1, 'fresh': 1, 'fight': 1, 'water': 1, 'reset': 1, 'funds': 1, 'share': 1, 'items': 1, 'boxes': 1, 'might': 1, 'large': 1, 'local': 1, 'links': 1})
INFO:root:CHAT_ID=365638834 got hint: _ h _ _ _
INFO:root:CHAT_ID=365638834 got candidate answers: Counter({'china': 7, 'white': 6, 'xhtml': 3, 'photo': 1, 'three': 1, 'thank': 1, 'share': 1})
INFO:root:CHAT_ID=365638834 got hint: W h _ t _
INFO:root:CHAT_ID=365638834 got candidate answers: Counter({'white': 2})
INFO:root:CHAT_ID=365638834 replying with answer: white
```
