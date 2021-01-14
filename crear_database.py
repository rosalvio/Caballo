import pandas as pd
from datetime import datetime

test_row = {"Nombre":"Nombre", "Apellidos": "Apellidos", "Fecha":datetime.now().strftime('%Y-%m-%d'),"F1.5":1, "F3":1, "F6":1, "F12":1, "F18":1}
database = pd.DataFrame(columns = ["Nombre", "Apellidos", "Fecha", "F1.5", "F3", "F6", "F12", "F18"])
database = database.append(test_row, ignore_index = True)
database.to_csv("database.csv", index = False)