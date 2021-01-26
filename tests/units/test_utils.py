from io import StringIO
from unittest.mock import mock_open, patch

import numpy as np
import pytest

import event_library
import event_library.utils as utils


def test_load_from_text():
    path = "foo/events.txt"
    txt_source = "100 0 0 1\n110 0 1 0"
    expected_result = np.array([[0, 0, 100, 1], [0, 1, 110, 0]])
    with patch("event_library.utils.load.open") as _file:
        _file.return_value = StringIO(txt_source)
        events = utils.load_from_file(path, 2)
        _file.assert_called_once_with(path, "r")
        assert type(events) == np.ndarray
        np.testing.assert_equal(events, expected_result)


def test_load_from_text_high_n():
    path = "foo/events.txt"
    txt_source = "100 0 0 1\n110 0 1 0"
    expected_result = np.array([[0, 0, 100, 1], [0, 1, 110, 0]])
    with patch("event_library.utils.load.open") as _file:
        _file.return_value = StringIO(txt_source)
        events = utils.load_from_file(path, 100)
        _file.assert_called_once_with(path, "r")
        assert type(events) == np.ndarray
        np.testing.assert_equal(events, expected_result)


def test_load_1_event_from_text():
    path = "foo/events.txt"
    txt_source = "100 0 0 1\n110 0 0 0"
    expected_result = np.array([[0, 0, 100, 1]])
    with patch("event_library.utils.load.open") as _file:
        _file.return_value = StringIO(txt_source)
        events = utils.load_from_file(path, 1)
        _file.assert_called_once_with(path, "r")
        assert type(events) == np.ndarray
        np.testing.assert_equal(events, expected_result)


def test_load_n_event_from_text():
    path = "foo/events.txt"
    txt_source = "100 0 0 1\n110 0 0 0\n100 0 0 1\n110 0 0 0"
    expected_result = np.array([[0, 0, 100, 1], [0, 0, 110, 0], [0, 0, 100, 1]])
    with patch("event_library.utils.load.open") as _file:
        _file.return_value = StringIO(txt_source)
        events = utils.load_from_file(path, 3)
        _file.assert_called_once_with(path, "r")
        assert type(events) == np.ndarray
        np.testing.assert_equal(events, expected_result)
