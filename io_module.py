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
    ns_time: int

    price_hour: str
    time_hour: tuple
    ns_time_hour: int

    price_day: str
    time_day: tuple
    ns_time_day: int

def write_data(data: OneRequestStorage):

    directory = DATA / f'user_{data.id}'
    Path(directory).mkdir(exist_ok=True)
    file_path = directory / f'{data.coin}_DATA.xlsx'

    if not file_path.is_file():
        df = pd.DataFrame(columns=[
            "price",
            "time",
            "date",
            "ns"
            ])
        
    else:
        df = pd.read_excel(file_path)

    new_row = pd.DataFrame({
        "price": [data.price_day, data.price_hour, data.price],
        "time": [data.time_day[1], data.time_hour[1], data.time[1]],
        "date": [data.time_day[0], data.time_hour[0], data.time[0]],
        "ns": [data.ns_time_day, data.ns_time_hour, data.ns_time]
        })

    df = pd.concat([df, new_row], ignore_index=True)

    df.to_excel(file_path, index=False)

def parse(files: list) -> list:
    df_list = [pd.read_excel(f) for f in files]
    df_list = [df.sort_values(by="ns") for df in df_list]
    df_list = [df.loc[:, :"date"] for df in df_list]
    result = []
    for df, file in zip(df_list, files):
        path = Path(file).parent.resolve() / f"{file.name[:-5]}_USER.xlsx"
        df.to_excel(path, index=False)
        result.append(path)
    return result
    
