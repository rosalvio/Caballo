import pandas as pd

test_row = {"Nombre":"Nombre","Fecha":"Fecha","1,5":1, "3":1, "6":1, "12":1, "18":1}
database = pd.DataFrame(columns = ["Nombre", "Fecha", "1,5", "3", "6", "12", "18"])
database = database.append(test_row, ignore_index = True)
database.to_csv("database.csv", index = False)