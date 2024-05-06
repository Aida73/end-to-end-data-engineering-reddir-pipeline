from utils.constants import *
from etls.reddit_etl import *
import pandas as pd

def reddit_pipeline(file_name: str, subreddit: str, time_filter='day', limit=None):
    #connecting to reddit instance
    instance = connect_reddit(CLIENT_ID, SECRET, 'Airschoalar Agent')
    #extraction
    posts = extract_posts(instance, subreddit, time_filter, limit)
    post_df = pd.DataFrame(posts)
    post_df = transform_data(post_df)
    #transforamtion
    post_df = transform_data(post_df)
    #loiading to csv
    file_path = f'{OUTPUT_PATH}/{file_name}.csv'
    load_data_to_csv(post_df,file_path )

    return file_path