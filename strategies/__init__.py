# strategies/__init__.py
"""Dynamiczne ładowanie strategii (bazowych + wygenerowanych przez LLM).

* pomija base.py
* przyjmuje klasy dziedziczące po Strategy **lub** dowolne z metodą
  decide(self_history, opp_history) i atrybutem name
* waliduje, że decide() zwraca dokładnie "C" lub "D"
"""

from importlib import import_module
from pathlib import Path
from types import ModuleType
import sys, traceback

from .base import Strategy as _BaseStrategy

# -----------------------------------------------------------------------------
STRATEGY_REGISTRY: dict[str, _BaseStrategy] = {}

# -----------------------------------------------------------------------------
def _discover(path: Path):
    """Zwróć listę plików *.py do załadowania."""
    return [
        p for p in path.glob("*.py")
        if p.name not in {"__init__.py", "base.py"}
    ]

def _make_module_name(file: Path) -> str:
    """Zbuduj pełną nazwę modułu, uwzględniając podpakiet generated/."""
    if file.parent.name == "generated":
        return f"{__package__}.generated.{file.stem}"
    return f"{__package__}.{file.stem}"

def _is_strategy_class(obj) -> bool:
    """Warunek przyjęcia klasy do rejestru."""
    if not isinstance(obj, type):
        return False
    if obj is _BaseStrategy:             # pomijamy abstrakcyjną bazę
        return False
    if issubclass(obj, _BaseStrategy):   # jawny subclass → OK
        return True
    # duck‑typing: metoda decide + atrybut name
    return callable(getattr(obj, "decide", None)) and isinstance(
        getattr(obj, "name", None), str
    )

# -----------------------------------------------------------------------------
def load_strategies() -> None:
    pkg_path = Path(__file__).parent
    files = _discover(pkg_path) + _discover(pkg_path / "generated")

    for file in files:
        try:
            mod: ModuleType = import_module(_make_module_name(file))
        except Exception as exc:            # noqa: BLE001
            print(f"[strategies] ❌ Import {file.name} nieudany: {exc}",
                  file=sys.stderr)
            traceback.print_exc()
            continue

        found_any = False
        for obj in mod.__dict__.values():
            if not _is_strategy_class(obj):
                continue
            # utwórz instancję
            try:
                inst = obj()
            except Exception as exc:        # noqa: BLE001
                print(f"[strategies] ❌ {file.name}: nie tworzę instancji "
                      f"{obj.__name__}: {exc}", file=sys.stderr)
                traceback.print_exc()
                continue
            # walidacja zwrotu
            try:
                sample = inst.decide([], [])
                if sample not in {"C", "D"}:
                    raise ValueError(f"decide() zwraca '{sample}'")
            except Exception as exc:        # noqa: BLE001
                print(f"[strategies] {file.name}: walidacja decide() "
                      f"nie powiodła się: {exc}", file=sys.stderr)
                traceback.print_exc()
                continue

            if inst.name in STRATEGY_REGISTRY:
                # duplikat → dopisz sufiks
                suffix = 1
                new_name = f"{inst.name}_{suffix}"
                while new_name in STRATEGY_REGISTRY:
                    suffix += 1
                    new_name = f"{inst.name}_{suffix}"
                inst.name = new_name
            STRATEGY_REGISTRY[inst.name] = inst
            found_any = True

        if not found_any:
            print(f"[strategies] ⚠️ {file.name} pominięto "
                  "(brak prawidłowych klas strategii)",
                  file=sys.stderr)

# -----------------------------------------------------------------------------
load_strategies()

__all__ = ["STRATEGY_REGISTRY"]
