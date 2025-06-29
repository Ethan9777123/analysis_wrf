
import os
from datetime import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.tools import generate_hourly_timestamps, download_gsmap




def get_gsmap_data(start_date, end_date):


    start = datetime.strptime(start_date, "%Y%m%d%H")
    end = datetime.strptime(end_date, "%Y%m%d%H")


    # 1時間ずつ増やして日時リストを作成
    dt_list = generate_hourly_timestamps(start, end)

    print(dt_list)

    for timestamp in dt_list:
        download_gsmap(timestamp)

        


if __name__ == "__main__":

    # yy mm dd hh
    start_date = sys.argv[1]
    end_date = sys.argv[2]

    get_gsmap_data(start_date, end_date)


