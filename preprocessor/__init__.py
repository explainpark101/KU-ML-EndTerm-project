import pandas as pd

def classify_features(dataFrame:pd.DataFrame, no_remove=[], exception=lambda column: False, debug=False):
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
            if exception(col):
                used.remove(col)
                unused.append(col)
    return list(set(used)), list(set(unused))