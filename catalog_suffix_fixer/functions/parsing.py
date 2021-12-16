import pandas as pd
from typing import Union, Tuple
import re
import string
import os


def import_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, header=[1])
    return df


def verify_format(df: pd.DataFrame) -> bool:
    critical_columns = ["Accession Number", "Date of Entry", "Catalog Suffix"]
    check = all(
        map(lambda v: v in list(df.columns.values), critical_columns)
    )  # column must be exact match
    # check = all(
    #     map(
    #         lambda v: any([re.search(v, x) for x in list(df.columns.values)]),
    #         critical_columns,
    #     )
    # )  # column name contains match
    return check


def drop_columns(
    df: pd.DataFrame, cols: int = 0
) -> pd.DataFrame:  # this may not be required
    df_out = df.drop(df.columns[list(range(0, cols))], axis=1)
    return df_out


def move_columns(df: pd.DataFrame) -> pd.DataFrame:
    targets = ["Date of Entry", "Catalog Suffix", "Accession Number"]
    columns = [x for x in list(df.columns.values) if x not in targets]
    df_out = df[targets + columns]
    return df_out


def sort_df(df: pd.DataFrame) -> pd.DataFrame:
    df_out = df.sort_values(["Accession Number", "Date of Entry"], ignore_index=True)
    return df_out


def remove_empty_rows(df: pd.DataFrame, column_names: list[str] = None) -> pd.DataFrame:
    if not column_names:
        column_names = ["Accession Number"]
    df_out = df.replace(r"^s*$", float("NaN"), regex=True).dropna(subset=column_names)
    df_out = df_out.fillna("")
    return df_out


def number_processed(df: pd.DataFrame) -> int:
    return len(df.index)


def cat_suffix_range(
    cat_suf: Tuple[Union[int, str], Union[int, str]]
) -> list[Union[int, str]]:
    list_out = []
    if type(cat_suf[1]) == str:
        for n in range(1, len(cat_suf[1]) + 1):
            list_out = list_out + [n * x for x in string.ascii_lowercase]
        list_out = list_out[list_out.index(cat_suf[0]) : list_out.index(cat_suf[1]) + 1]
    else:
        list_out = list(range(cat_suf[0], cat_suf[1] + 1))
    return list_out


def parse_catalog_suffix(suffix: str) -> Tuple[Union[int, str], Union[int, str]]:
    suffix = suffix.replace(" ", "")
    str_test = re.search(r"[A-z]+-[A-z]+", suffix)
    int_test = re.search(r"[0-9]+-[0-9]+|[0-9]+to[0-9]+", suffix)
    if str_test:  # a-b
        suffix_start = str_test.group().split("-")[0].lower()
        suffix_end = str_test.group().split("-")[1].lower()
    elif int_test:  # 8 to 9 OR 8-9
        suffix_start = int(re.split(r"-|to", int_test.group())[0])
        suffix_end = int(re.split(r"-|to", int_test.group())[1])
    else:  # unsupported
        suffix_start = ""
        suffix_end = ""
    return suffix_start, suffix_end


def generate_new_records(df: pd.DataFrame) -> pd.DataFrame:
    df_temp = df.copy()
    for idx, row in df_temp.iterrows():
        cat_suf = row[["Catalog Suffix"]][0]
        if cat_suf != "":
            cat_suf = parse_catalog_suffix(cat_suf)
            if "" in cat_suf:
                print("PROBLEM PARSING CATALOG SUFFIX")  # log statement, details
            else:
                # determine the new range of characters/integers to generate
                cat_suf_range = cat_suffix_range(cat_suf)
                df_temp["Catalog Suffix"].at[idx] = cat_suf_range
    df = df_temp.explode("Catalog Suffix", ignore_index=True)
    return df


def save_df(df: pd.DataFrame, path: str) -> None:
    os.makedirs("/".join(path.split("/")[0:-1]), exist_ok=True)
    df.to_csv(path)


def number_generated(df: pd.DataFrame, offset: int = 0) -> int:
    return len(df.index) - offset
