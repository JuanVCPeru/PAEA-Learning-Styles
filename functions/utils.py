import pandas as pd

def get_type_result_from_user(user: str, df: pd.DataFrame):
    filtered_df = df[df['user'] == user]
    type_with_max_points = filtered_df.groupby('type')['points'].sum().idxmax()
    return type_with_max_points