"""
Thin wrapper around brainglobe_atlasapi + brainrender.
All imports are local inside functions to keep import-time light and tests easy.
"""

from __future__ import annotations
from typing import Iterable, Tuple, List

class AtlasLoadError(RuntimeError):
    pass

def load_atlas(name: str):
    try:
        from brainglobe_atlasapi import BrainGlobeAtlas
    except Exception as e:
        raise AtlasLoadError(f"brainglobe_atlasapi not available: {e}") from e
    try:
        return BrainGlobeAtlas(name)
    except Exception as e:
        raise AtlasLoadError(f"Cannot load atlas '{name}': {e}") from e

def get_structures(atlas):
    """
    Return a list of structure acronyms from a variety of atlas.structures shapes:
    - dict-like: keys are acronyms
    - pandas.DataFrame: column 'acronym'
    - list/tuple of dicts or objects with 'acronym'
    - fallback: atlas.lookup_df['acronym'] if available
    """
    s = getattr(atlas, "structures", None)

    # dict-like
    if isinstance(s, dict):
        return [str(k).strip() for k in s.keys()]

    # pandas.DataFrame
    try:
        import pandas as pd  # type: ignore
        if isinstance(s, pd.DataFrame):
            cols = [c.lower() for c in s.columns]
            if "acronym" in cols:
                colname = s.columns[cols.index("acronym")]
                return [str(a).strip() for a in s[colname].astype(str).tolist()]
    except Exception:
        pass

    # list/tuple of dicts or objects with 'acronym'
    if isinstance(s, (list, tuple)):
        acrs = []
        for item in s:
            if isinstance(item, dict) and "acronym" in item:
                acrs.append(str(item["acronym"]).strip())
            elif hasattr(item, "acronym"):
                acrs.append(str(getattr(item, "acronym")).strip())
        if acrs:
            return acrs

    # fallback: some versions expose a lookup dataframe
    lookup = getattr(atlas, "lookup_df", None)
    if lookup is not None:
        try:
            import pandas as pd  # type: ignore
            if isinstance(lookup, pd.DataFrame) and "acronym" in [c.lower() for c in lookup.columns]:
                cols = [c.lower() for c in lookup.columns]
                colname = lookup.columns[cols.index("acronym")]
                return [str(a).strip() for a in lookup[colname].astype(str).tolist()]
        except Exception:
            pass

    raise AtlasLoadError("Atlas does not expose a dict-like 'structures' table.")


def build_scene(atlas_name: str):
    try:
        from brainrender import Scene
    except Exception as e:
        raise AtlasLoadError(f"brainrender not available: {e}") from e
    try:
        return Scene(title=f"NeuroRender — {atlas_name}", inset=False)
    except Exception as e:
        raise AtlasLoadError(f"Cannot create Scene: {e}") from e

def add_regions(scene, acronyms: Iterable[str], colors: Iterable[str], alpha: float):
    for a, c in zip(acronyms, colors):
        # brainrender accepts list of regions but adding one-by-one is explicit
        scene.add_brain_region(a, alpha=float(alpha), color=c)

def render(scene):
    # In a GUI you’d probably call scene.render(interactive=True)
    scene.render()
