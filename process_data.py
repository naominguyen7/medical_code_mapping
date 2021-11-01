from typing import Iterable, List
import pandas as pd, numpy as np
from nnsplit import NNSplit
import spacy


splitter = NNSplit.load("de")  # tool to split compound
nlp = spacy.load(
    "de_dep_news_trf", exclude=["transformer", "tagger", "morphologizer", "parser"]
)  # tool to lemmatize


def split_compound(compound: str) -> str:
    """Split a compound and treat uni-components and bi-components as tokens.
    Return a string of space-seperated components.
    Compound nouns should be capitalized.

    Args:
        compound (str): compound

    Returns:
        str: string of space-seperated components
    """
    components = [str(comp) for comp in splitter.split([compound])[0][0][0][0]]
    if len(components) > 2:
        component_bigrams = [
            "".join(components[i : (i + 2)]) for i in range(len(components) - 1)
        ]
        components += component_bigrams
    if compound.istitle():  # if the compound is a noun, the components are also nouns
        components = [comp.capitalize() for comp in components]
    return " ".join(components).strip()


def split_query(query: str) -> str:
    """Process a query with compounds into such query with components instead

    Args:
        query (str): original query

    Returns:
        str: query with compounds with space seperated components
    """
    return " ".join(
        [
            split_compound(word)
            for word in query.split()
            if word not in nlp.Defaults.stop_words
        ]
    )


def lemmatize_and_tokenize(query: str) -> List:
    """Lemmatize each token of query

    Args:
        query (str)

    Returns:
        List: List of tokens that have been lemmatized
    """
    return [token.lemma_ for token in nlp(query)]


def preprocess_query(query: str) -> List:
    """Process a query:
    - Split compounds and treat components as tokens
    - Tokenize and lemmatized

    Args:
        query (str)
    Returns:
        List: List of lemmatized tokens
    """
    return lemmatize_and_tokenize(split_query(query))


def jaccard_similarity(list1: Iterable, list2: Iterable) -> float:
    """Measure Jaccard similarity between 2 iterables

    Args:
        list1 (Iterable):
        list2 (Iterable):

    Returns:
        float: Jaccard similarity. Range 0-1. The higher, the more similar
    """
    s1 = set(list1)
    s2 = set(list2)
    return float(len(s1.intersection(s2)) / len(s1.union(s2)))


if __name__ == "__main__":
    code_description_df = pd.read_csv("./processed_data/code_description.csv")
    code_description_df["description"] = code_description_df.description.apply(
        preprocess_query
    )
    code_description_df.to_csv(
        "./processed_data/processed_description.csv", index=False
    )
