
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt
import numpy as np
import random
from datetime import datetime, timedelta


def run_strategy_crypto(files):
    data = pd.DataFrame()
    for file in files:
        data = pd.read_csv(file)
        window_size = 100  # Adjust the window size as needed
        # haven't included bid size
        data['bid_px_sma'] = data['bid_px_00'].rolling(window=window_size).mean() 
        data['ask_px_sma'] = data['ask_px_00'].rolling(window=window_size).mean()

        data['spread'] = data['bid_px_sma'] - data['ask_px_sma']

        # Create a new column 'deltaValues' initialized with 0
        data['deltaValues'] = 0

        # Define the number of zeros to add at the beginning
        num_zeros_to_add = window_size

        # Add the specified number of zeros at the beginning
        data['deltaValues'] = pd.concat([pd.Series([0] * num_zeros_to_add), data['deltaValues']], ignore_index=True)

        # Reset the index of the DataFrame
        data = data.reset_index(drop=True)

        # Use pandas' shift() method to compare spread values and update 'deltaValues'
        mask1 = (data['spread'].shift(1) > 0) & (data['spread'] < 0)
        mask2 = (data['spread'].shift(1) < 0) & (data['spread'] > 0)

        # Update 'deltaValues' using np.where
        data['deltaValues'] = np.where(mask1, -1, np.where(mask2, 1, 0))

        data['position'] = [0] * len(data['deltaValues'])

        for i in range(1, len(data['deltaValues'])):
            print(data['deltaValues'][i-1])
            if data['deltaValues'][i-1] > 0 and data['deltaValues'][i] < 0:
                data.at[i, 'position'] = 1
            elif data['deltaValues'][i-1] < 0 and data['deltaValues'][i] > 0:
                data.at[i, 'position'] = -1

    positions = pd.DataFrame({
        "DATETIME": data['ts_event'], 
        "POSITION": data['position']
    })
    return positions
    
