"""Tests du module sentiment avec mock de FinBERT."""

import os
import sys
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sentiment import SentimentResult, analyze, analyze_batch


@patch("sentiment.get_pipeline")
def test_analyze_positive(mock_pipe):
    mock_pipe.return_value = lambda text, **kwargs: [{"label": "positive", "score": 0.95}]
    result = analyze("Apple beats expectations")
    assert isinstance(result, SentimentResult)
    assert result.label == "positive"
    assert result.score == 0.95


@patch("sentiment.get_pipeline")
def test_analyze_negative(mock_pipe):
    mock_pipe.return_value = lambda text, **kwargs: [{"label": "negative", "score": 0.88}]
    result = analyze("Tesla missed Q3 earnings badly")
    assert result.label == "negative"
    assert result.score == 0.88


@patch("sentiment.get_pipeline")
def test_analyze_batch(mock_pipe):
    mock_pipe.return_value = lambda texts, batch_size=16: [
        {"label": "positive", "score": 0.9},
        {"label": "negative", "score": 0.8},
    ]
    results = analyze_batch(
        [
            "Apple stock soared",
            "Tesla missed estimates",
        ]
    )
    assert len(results) == 2
    assert results[0].label == "positive"
    assert results[1].label == "negative"


def test_analyze_empty_raises():
    with pytest.raises(ValueError):
        analyze("")


def test_analyze_batch_empty():
    results = analyze_batch([])
    assert results == []
