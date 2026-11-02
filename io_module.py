from dataclasses import dataclass
from pathlib import Path
import pandas as pd

DATA = Path(__file__).parent.resolve() / "data"

@dataclass
class OneRequestStorage:
    coin: str
    id: int

    price: str
    time: tuple

    price_hour: str
    time_hour: tuple

    price_day: str
    time_day: tuple

def write_data(data: OneRequestStorage):
    file_path = DATA / f"{data.id}.xlsx"
    if not file_path.is_file():
        df = pd.DataFrame(columns=[
            "coin",
            "price",
            "time",
            "date",
            ])
        
    else:
        df = pd.read_excel(file_path)

    new_row = pd.DataFrame({
        "coin": [f"{data.coin}", f"{data.coin}", f"{data.coin}"],
        "price": [f"{data.price}",  f"{data.price_hour}", f"{data.price_day}"],
        "time": [f"{data.time[1]}", f"{data.time_hour[1]}", f"{data.time_day[1]}"],
        "date": [f"{data.time[0]}", f"{data.time_hour[0]}", f"{data.time_day[0]}"],
        })

    df = pd.concat([df, new_row], ignore_index=True)

    df.to_excel(file_path, index=False)

def read_data(id: int) -> tuple:
    file_path = DATA / f"{id}.xlsx"
    if not file_path.is_file():
        return (0, "You have no story yet :(", None)
    else:
        df = pd.read_excel(file_path)
        return (1, "Here's all your story", df)

    
