"""ai_text package: lightweight AI-style text processing utilities.

Exposes a small, dependency-light toolkit for text summarization and
sentiment analysis that can run without heavyweight ML frameworks.

Public API:
- TextProcessingPipeline: High-level facade with summarize and sentiment
- summarize_text: Extractive summarization using frequency-based scoring
- analyze_sentiment: VADER-based sentiment analysis with simple labels
"""

from .pipeline import (
    TextProcessingPipeline,
    summarize_text,
    analyze_sentiment,
)

__all__ = [
    "TextProcessingPipeline",
    "summarize_text",
    "analyze_sentiment",
]

__version__ = "0.1.0"

