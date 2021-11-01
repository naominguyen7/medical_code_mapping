import os
import re

import pandas as pd
from bs4 import BeautifulSoup


def get_code_from_page(fname: str) -> pd.DataFrame:
    """Get code and description from a DIMDI's HTML file (https://www.dimdi.de/dynamic/de/klassifikationen/icd/icd-10-gm/)

    Args:
        fname (str): file name with code and description

    Returns:
        pd.DataFrame: a dataframe with descriptions for code with format "^[A-Z][0-9][0-9]$"
    """
    with open(r"Klassifikationsdateien/" + fname, "r") as f:
        html_doc = f.read()
        soup = BeautifulSoup(html_doc, "html.parser")
        code_tags = soup.find_all(
            "a", {"class": "code", "id": re.compile("^[A-Z][0-9][0-9]")}
        )
        description_tags = [code_tag.find_next_sibling() for code_tag in code_tags]
        codes = [code_tag["id"] for code_tag in code_tags]
        descriptions = [description_tag.text for description_tag in description_tags]
    return pd.DataFrame(
        {
            "description": descriptions,
            "code": codes,
        }
    )


def main():
    dfs = []
    for file_name in os.listdir("Klassifikationsdateien/"):  # folder downloaded
        if "block" in file_name:  # HTML files with codes and descriptions
            dfs.append(get_code_from_page(file_name))

    code_description_df = pd.concat(dfs)
    code_description_df.to_csv("./processed_data/code_description.csv", index=False)


if __name__ == "__main__":
    main()
