from ast import literal_eval
import pandas as pd
from fastapi import FastAPI
from process_data import jaccard_similarity, preprocess_query

app = FastAPI()
code_description_df = pd.read_csv(
    "./processed_data/processed_description.csv",
    converters={"description": literal_eval},
)


@app.get("/predict_icd/{query}")
async def predict(query: str) -> str:
    """Predict ICD code given request's input

    Args:
        query (str): disease description

    Returns:
        str: ICD code
    """
    res = code_description_df["description"].apply(
        jaccard_similarity, list2=preprocess_query(query)
    )
    return code_description_df.code.iloc[res.argmax()]
