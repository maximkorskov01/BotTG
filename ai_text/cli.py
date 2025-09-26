import argparse
import json
import os
import sys
from typing import Optional

from .pipeline import TextProcessingPipeline


def _read_text_from_source(file_path: Optional[str]) -> str:
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    if sys.stdin and not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("No input provided. Pass --file or pipe text via stdin.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="AI-style text processing CLI (summarize, sentiment)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    summarize_parser = subparsers.add_parser("summarize", help="Summarize text")
    summarize_parser.add_argument(
        "--file",
        type=str,
        help="Path to input text file. If omitted, reads from stdin.",
    )
    summarize_parser.add_argument(
        "--max-sentences",
        type=int,
        default=3,
        help="Maximum number of sentences in summary (default: 3)",
    )
    summarize_parser.add_argument(
        "--min-chars",
        type=int,
        default=30,
        help="Minimum characters per sentence to include (default: 30)",
    )

    sentiment_parser = subparsers.add_parser("sentiment", help="Sentiment analysis")
    sentiment_parser.add_argument(
        "--file",
        type=str,
        help="Path to input text file. If omitted, reads from stdin.",
    )

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    pipeline = TextProcessingPipeline(
        min_sentence_characters=getattr(args, "min_chars", 30),
        max_summary_sentences=getattr(args, "max_sentences", 3),
    )

    if args.command == "summarize":
        text = _read_text_from_source(getattr(args, "file", None))
        summary = pipeline.summarize(text)
        print(summary)
        return 0

    if args.command == "sentiment":
        text = _read_text_from_source(getattr(args, "file", None))
        result = pipeline.sentiment(text)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

