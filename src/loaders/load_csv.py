import pandas as pd


def load_csv(filepath: str = "../data/processed/thelasttake_clean.csv", **kwargs) -> pd.DataFrame:
    """
    Charge le dataset TheLastTake en DataFrame.
    """
    df = pd.read_csv(filepath, encoding="utf-8-sig", **kwargs)
    return df