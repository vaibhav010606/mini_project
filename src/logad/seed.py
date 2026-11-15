"""Deterministic seeding for reproducible experiments (NFR1)."""

import random

import numpy as np


def set_seed(seed: int) -> None:
    """Seed the Python, NumPy and (if installed) PyTorch random generators.

    GPU kernels can still be non-deterministic; document any residual
    run-to-run variation in the results analysis.
    """
    if seed < 0:
        raise ValueError("seed must be non-negative")
    random.seed(seed)
    np.random.seed(seed)
    try:
        import torch
    except ImportError:
        return
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
