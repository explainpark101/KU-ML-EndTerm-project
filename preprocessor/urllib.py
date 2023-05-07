from urllib.parse import parse_qsl
import json
import pandas as pd

def strict_parse_qsl(qs, *args, strict_parsing=True, **kwargs):
    """makes the default urllib's parameter strict_parsing=True as default.

    Returns {"NaN":qs} is there is error while processing qsl.
    """
    if not qs: return dict()
    try:
        list_of_dicts = parse_qsl(qs, *args, strict_parsing=True,  **kwargs)
        for i,(key, val) in enumerate(list_of_dicts):
            if key and not val:
                key, val = val, key
                list_of_dicts[i] = (key, val)
        return dict(list_of_dicts)
    except:
        return dict([("NaN", qs)])
    
def query_params_to_dict(series:pd.Series, to_json=False):
    """makes the queryParameter Series into dict Series

    Args:
        series (pd.Series): Series of queryParameter
        to_json (bool, optional): returns to json string. Defaults to False.

    Returns:
        pd.Series: dict Series of processed queryParameter
    """
    return pd.Series([
        (
            json.dumps((strict_parse_qsl(_)), indent=2, ensure_ascii=True) 
            if to_json else
            strict_parse_qsl(_)
        )
            for _ in series
    ])