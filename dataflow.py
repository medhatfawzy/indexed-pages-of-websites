import pandas as pd


class File():
    def __init__(self, path):
        self.data = pd.read_excel(path)

    def get_domains(self):
        return self.data["domains"]

    def save_results(self, results, path="results.xlsx"):
        self.data["results"] = pd.Series(results)
        self.data.to_excel(path, index=False)