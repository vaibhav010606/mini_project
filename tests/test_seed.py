"""Tests for deterministic seeding."""

import random
import sys
import types

import numpy as np
import pytest

from logad.seed import set_seed


def test_same_seed_gives_same_python_and_numpy_draws() -> None:
    set_seed(7)
    first = (random.random(), float(np.random.rand()))
    set_seed(7)
    second = (random.random(), float(np.random.rand()))
    assert first == second


def test_different_seeds_give_different_draws() -> None:
    set_seed(1)
    a = random.random()
    set_seed(2)
    b = random.random()
    assert a != b


def test_negative_seed_is_rejected() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        set_seed(-1)


def test_seeds_torch_when_it_is_installed(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[tuple[str, int]] = []
    fake_torch = types.SimpleNamespace(
        manual_seed=lambda s: calls.append(("cpu", s)),
        cuda=types.SimpleNamespace(manual_seed_all=lambda s: calls.append(("cuda", s))),
    )
    monkeypatch.setitem(sys.modules, "torch", fake_torch)
    set_seed(3)
    assert calls == [("cpu", 3), ("cuda", 3)]


def test_works_without_torch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "torch", None)
    set_seed(5)  # must not raise when PyTorch is missing
