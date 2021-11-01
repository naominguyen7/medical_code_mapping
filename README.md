This project aims to predict ICD code given a description. 
The description is assumed to capitalize correctly for nouns.


# Mechanism:
- Get data from DIMI source
- Make a table of code and corresponding official description
- Split each description into lemmatized tokens, including splitting up compounds
- Since there is only one sample per class, the project uses a lookup table. The query will be measured against all existing ones for similarity scores and the returned code is the code with highest score

# Set up:
- Clone the repo
- Create a new virtual environment with python 3.7.3 and pip 21.3.1
- Run `pip install requirements.txt`


---

# Run the live server:
1. Run `uvicorn main:app --reload`
2. Follow the URL (example http://127.0.0.1:8000) to send request
Example: 

Request: GET /predict_icd “Karzinom des Zungengrundes”
Response: "C01"

---


# Generate data:
- Compile raw medical codes and descriptions from HTML files:
    + Go to https://www.dimdi.de/dynamic/.downloads/klassifikationen/icd-10-gm/version2022/icd10gm2022syst-html.zip
    + Accept conditions and download
    + Run `python get_data.py`
    -> Results stored in `processed_data/code_description.csv`

- Process code description into lemmatized split-up:
    + Run `python process_data.py`
    -> Results stored in `processed_data/processed_description.csv`

## License
[MIT](https://choosealicense.com/licenses/mit/)