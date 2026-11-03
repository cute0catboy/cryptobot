from dataclasses import dataclass
from pathlib import Path
import pandas as pd

DATA = Path(__file__).parent.resolve() / "data"

@dataclass
class OneRequestStorage:
    coin: str
    id: int

    price: list #[100.5, 151.3, 157.2, ...]
    time: list #[time_module.Time, time_module.Time, time_module.Time,...]

    def __post_init__(self):
        self.time_hours = []
        self.time_days = []
        self.time_nanosec = []
        for t in self.time:
            self.time_days.append(t.date)
            self.time_hours.append(t.time)
            self.time_nanosec.append(t.nanoseconds)
 
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
        "price": data.price,
        "time": data.time_hours,
        "date": data.time_days,
        "ns": data.time_nanosec
        })

    df = pd.concat([df, new_row], ignore_index=True)

    df.to_excel(file_path, index=False)

def parse(files: list) -> list:
    df_list = [pd.read_excel(f) for f in files]
    df_list = [df.sort_values(by="ns") for df in df_list]
    df_list = [df.loc[:, :"date"] for df in df_list] #тут короче говоря просто сортирует по наносекундам и отрезает столбик с ними для юзера (а еще я научился делать это короткие циклы ну в [])
    result = []
    for df, file in zip(df_list, files):
        path = Path(file).parent.resolve() / f"{file.name[:-5]}_USER.xlsx"
        df.to_excel(path, index=False)
        result.append(path)
    return result
    
