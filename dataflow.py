import pandas as pd


class File():
    def __init__(self, path):
        self.data = pd.read_excel(path)

    def get_domains(self):
        return self.data["domains"]
    
    @staticmethod
    def save_results(results, path="results.xlsx"):
        new_file = pd.DataFrame(list(results.items()))
        new_file.to_excel(path, index=False)