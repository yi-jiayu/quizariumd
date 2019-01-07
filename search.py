import re
import requests
from bs4 import BeautifulSoup, Comment
from collections import Counter

ddg_query_base = 'https://duckduckgo.com/html/?q='
whitespace_regexp = re.compile(r'\s+')

with open('stopwords.txt') as f:
    stopwords = set(f.read().strip().split('\n'))


def get_search_results(question):
    resp = requests.get(ddg_query_base + question)
    soup = BeautifulSoup(resp.text, features='html.parser')

    # remove comments
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    page_text = soup.findAll(text=True)
    not_whitespace = (t for t in page_text if whitespace_regexp.fullmatch(t) is None)
    stripped = [t.strip() for t in not_whitespace]
    return stripped


def build_hint_matcher(hint):
    hint = ' '.join([h.replace(' ', '').replace('_', r'\w') for h in hint.split('   ')])
    hint = fr'(?:^|[^\w])({hint})(?:$|[^\w])'
    return re.compile(hint)


def generate_candidate_answers(search_results, hint, question='', use_stopwords=True, additional_stopwords=None):
    matcher = build_hint_matcher(hint)
    for t in search_results:
        matches = matcher.findall(t)
        for m in matches:
            m = m.lower()
            # todo: stem both question and match
            if m in question.lower():
                continue
            if use_stopwords and m in stopwords:
                continue
            if additional_stopwords and m in additional_stopwords:
                continue
            yield m


def evaluate_candidate_answers(search_results, hint, question='', use_stopwords=True, additional_stopwords=None):
    candidate_answers = list(
        generate_candidate_answers(search_results, hint, question, use_stopwords, additional_stopwords))
    if candidate_answers:
        return Counter(candidate_answers)


def get_best_match(candidate_answers, simple_majority_threshold=0.5, plurality_threshold=1.75):
    if candidate_answers:
        # check for simple majority
        most_common = candidate_answers.most_common(1)
        top_result, count = most_common[0]
        if count / sum(candidate_answers.values()) > simple_majority_threshold:
            return top_result

        # check if most common candidate is at least twice as common as second most common
        if len(candidate_answers) > 1:
            most_common, second_most_common = candidate_answers.most_common(2)
            top_result, count = most_common
            _, second_best_result_count = second_most_common
            if count >= plurality_threshold * second_best_result_count:
                return top_result
