"""Reading workflows from CSV and testing how sensitive rankings are to the weights."""

from pathlib import Path
from typing import List, Optional, Sequence, Union

import numpy as np
import pandas as pd

from .model import DOMAINS, Assessment, Workflow


def read_workflows(path: Union[str, Path]) -> List[Workflow]:
    """Read workflows from a CSV with columns `name`, the six domain keys and,
    optionally, `notes`. One row per workflow."""
    table = pd.read_csv(path)
    return [Workflow.from_dict(row) for row in table.to_dict("records")]


def write_workflows(workflows: Sequence[Workflow], path: Union[str, Path]):
    """Write workflows to CSV in the format read_workflows expects."""
    pd.DataFrame([{"name": w.name, **w.scores, "notes": w.notes} for w in workflows]).to_csv(path, index=False)


def weight_sensitivity(workflows: Sequence[Workflow], n_samples: int = 2000, concentration: float = 5.0,
                       seed: Optional[int] = None) -> pd.DataFrame:
    """How stable is the ranking when the domain weights change?

    Draws `n_samples` random weightings from a symmetric Dirichlet distribution
    (larger `concentration` keeps them closer to equal weights), ranks the
    workflows under each, and reports for each workflow how often it ranks first,
    its median rank, and the range of its overall score.
    """
    rng = np.random.default_rng(seed)
    keys = list(DOMAINS)
    S = np.array([[w.scores[k] for k in keys] for w in workflows])
    W = rng.dirichlet(np.full(len(keys), concentration), size=n_samples)
    overall = W @ S.T                                   # samples x workflows
    ranks = (-overall).argsort(axis=1).argsort(axis=1) + 1
    return pd.DataFrame({
        "workflow": [w.name for w in workflows],
        "rank_equal_weights": pd.Series(S.mean(axis=1)).rank(ascending=False, method="min").astype(int),
        "share_ranked_first": (ranks == 1).mean(axis=0).round(3),
        "median_rank": np.median(ranks, axis=0),
        "score_min": overall.min(axis=0).round(2),
        "score_max": overall.max(axis=0).round(2),
    }).sort_values("rank_equal_weights", kind="stable").reset_index(drop=True)
