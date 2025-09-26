from __future__ import annotations

import json
import math
import re
import sys
from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple


try:
    # Lightweight sentiment library (no model downloads required)
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
except Exception as import_error:  # pragma: no cover - defensive import
    SentimentIntensityAnalyzer = None  # type: ignore


SMALL_DEFAULT_STOPWORDS: frozenset[str] = frozenset(
    {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "by",
        "for",
        "from",
        "has",
        "he",
        "in",
        "is",
        "it",
        "its",
        "of",
        "on",
        "that",
        "the",
        "to",
        "was",
        "were",
        "will",
        "with",
    }
)


def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences using a simple regex-based approach.

    This avoids heavy dependencies and works reasonably for many cases.
    """
    if not text:
        return []
    # Normalize whitespace
    normalized = re.sub(r"\s+", " ", text).strip()
    # Split on period, exclamation, question mark followed by space or end
    candidate_sentences = re.split(r"(?<=[.!?])\s+", normalized)
    # Keep non-empty sentences
    return [s.strip() for s in candidate_sentences if s.strip()]


def tokenize(text: str) -> List[str]:
    """Tokenize into lowercase word tokens (alphabetic only)."""
    return re.findall(r"[A-Za-zА-Яа-яЁё]+", text.lower())


def build_word_frequencies(tokens: Iterable[str], stopwords: Iterable[str]) -> Dict[str, float]:
    frequency: Dict[str, int] = {}
    stopword_set = set(stopwords)
    for token in tokens:
        if token in stopword_set:
            continue
        frequency[token] = frequency.get(token, 0) + 1

    if not frequency:
        return {}

    max_frequency = max(frequency.values())
    # Normalize to [0,1]
    return {word: count / max_frequency for word, count in frequency.items()}


def score_sentences(sentences: List[str], word_frequencies: Dict[str, float]) -> List[Tuple[int, float]]:
    scores: List[Tuple[int, float]] = []
    if not sentences or not word_frequencies:
        return scores

    for index, sentence in enumerate(sentences):
        sentence_tokens = tokenize(sentence)
        if not sentence_tokens:
            continue
        score = sum(word_frequencies.get(token, 0.0) for token in sentence_tokens)
        # Length normalization to avoid bias for long sentences
        score /= math.log(len(sentence_tokens) + 1.5)
        scores.append((index, score))
    return scores


def select_top_sentences(
    sentences: List[str],
    scored: List[Tuple[int, float]],
    max_sentences: int,
    min_sentence_characters: int,
) -> List[str]:
    if not scored:
        return []
    # Sort by score descending and select top N indices
    top_indices = [idx for idx, _ in sorted(scored, key=lambda t: t[1], reverse=True)]
    selected: List[int] = []
    for idx in top_indices:
        if len(selected) >= max_sentences:
            break
        if len(sentences[idx]) < min_sentence_characters:
            continue
        selected.append(idx)

    # Preserve original order for readability
    selected.sort()
    return [sentences[i] for i in selected]


def summarize_text(
    text: str,
    max_sentences: int = 3,
    min_sentence_characters: int = 30,
    stopwords: Iterable[str] = SMALL_DEFAULT_STOPWORDS,
) -> str:
    """Create a simple extractive summary by scoring sentences.

    This is a lightweight heuristic summarizer suitable as a fast baseline.
    """
    sentences = split_into_sentences(text)
    if not sentences:
        return ""
    word_frequencies = build_word_frequencies(tokenize(text), stopwords)
    scores = score_sentences(sentences, word_frequencies)
    top_sentences = select_top_sentences(
        sentences=sentences,
        scored=scores,
        max_sentences=max_sentences,
        min_sentence_characters=min_sentence_characters,
    )
    if not top_sentences:
        # Fallback: take the first sentence if all are too short
        return sentences[0]
    return " ".join(top_sentences)


def _ensure_vader() -> "SentimentIntensityAnalyzer":
    if SentimentIntensityAnalyzer is None:
        raise RuntimeError(
            "vaderSentiment is not installed. Please `pip install vaderSentiment`."
        )
    return SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> Dict[str, object]:
    """Analyze sentiment using VADER and return a compact JSON-like dict.

    Returns keys: compound (float in [-1,1]), label (negative/neutral/positive)
    """
    analyzer = _ensure_vader()
    scores = analyzer.polarity_scores(text or "")
    compound = scores.get("compound", 0.0)
    if compound >= 0.05:
        label = "positive"
    elif compound <= -0.05:
        label = "negative"
    else:
        label = "neutral"
    return {"compound": compound, "label": label, "scores": scores}


@dataclass
class TextProcessingPipeline:
    """High-level facade exposing common text processing tasks."""

    min_sentence_characters: int = 30
    max_summary_sentences: int = 3

    def summarize(self, text: str) -> str:
        return summarize_text(
            text=text,
            max_sentences=self.max_summary_sentences,
            min_sentence_characters=self.min_sentence_characters,
        )

    def sentiment(self, text: str) -> Dict[str, object]:
        return analyze_sentiment(text)


def _read_stdin_text_if_any() -> str:
    if sys.stdin and not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def _as_json(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)

