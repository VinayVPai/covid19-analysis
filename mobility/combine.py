import sys
from pathlib import Path
import pandas as pd

DATA_PATH = Path('../dist/static/mobility')
DATES = ['2020-03-29', '2020-04-05']

def load_reports(dates, data_path, us=False):
    dfs = []
    for date in dates:
        filename =  f'{date}_world.csv.gz' if not us else f'{date}_us.csv.gz'
        df = (pd.read_csv(data_path / filename, 
                        na_values=[''])
            .assign(report_date=date))
        dfs.append(df)
    df = pd.concat(dfs)
    return df

def take_mean(df, us=False):
    if not us:
        to_group = ['country_geoid', 'country', 'region', 'category', 'page', 'date']
    else:
        to_group = ['state', 'county', 'category', 'page', 'date']
    mean_df = df.groupby(to_group).agg({'change': 'last', 'value': 'mean'}).reset_index()
    return mean_df


if __name__ == "__main__":
    us = len(sys.argv) > 1 and sys.argv[1].lower() == 'us'
    df = load_reports(DATES, DATA_PATH, us=us)
    combined = take_mean(df, us)
    filename = 'world' if not us else 'us'
    combined.to_csv(DATA_PATH / f'{filename}.csv.gz', index=False)
    combined.to_json(DATA_PATH / f'{filename}.json.gz', orient='records', indent=2)
