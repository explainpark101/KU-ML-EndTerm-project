from typing import Iterable
import pandas as pd

def classify_features(dataFrame:pd.DataFrame, no_remove:Iterable=[], debug=False) -> tuple[list, list]:
    """kills columns with only unique value.

    Args:
        dataFrame (pd.DataFrame): Target Dataframe for processing
        no_remove (list, optional): List of columns that you don't want to remove even though it is only unique value column. Defaults to [].
        debug (bool, optional): print the removed columns. Defaults to False.

    Returns:
        tuple[list, list] : list of used columns, list of only unique value columns.
    """
    temp_cols = dataFrame.columns
    used = list(temp_cols[:])
    unused = []
    for col in dataFrame.columns:
        try:
            if dataFrame[col].unique().shape[0] <= 1 and col not in no_remove:
                if debug: print(f"{col} : unique value column")
                used.remove(col)
                unused.append(col)
                continue
        except: 
            used.remove(col)
            unused.append(col)
    return list(set(used)), list(set(unused))
