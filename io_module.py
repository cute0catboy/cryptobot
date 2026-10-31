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
            "id",
            "price",
            "time",
            "date",
            "price_hour",
            "time_hour",
            "date_hour",
            "price_day",
            "time_day",
            "date_day",
            ])
        
    else:
        df = pd.read_excel(file_path)

    new_row = pd.DataFrame([{
        "coin": f"{data.coin}",
        "id": f"{data.id}",
        "price": f"{data.price}",
        "time": f"{data.time[1]}",
        "date": f"{data.time[0]}",
        "price_hour": f"{data.price_hour}",
        "time_hour": f"{data.time_hour[1]}",
        "date_hour": f"{data.time_hour[0]}",
        "price_day": f"{data.price_day}",
        "time_day": f"{data.time_day[1]}",
        "date_day": f"{data.time_day[0]}",
        }])

    df = pd.concat([df, new_row], ignore_index=True)

    df.to_excel(file_path, index=False)

def read_data(id: int) -> tuple:
    file_path = DATA / f"{id}.xlsx"
    if not file_path.is_file():
        return (0, "You have no story yet :(", None)
    else:
        df = pd.read_excel(file_path)
        return (1, "Here's all your story", df)

    
