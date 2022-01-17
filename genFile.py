import pandas as pd
import glob
def genEngagement():
    path = r"./input/engagement_data"
    filenames = glob.glob(path+"/*.csv")

    engagement = pd.DataFrame()
    for file in filenames:
        b = pd.read_csv(file)
        b["district_id"] = int(file.split("/")[-1].split(".")[0])
        engagement = pd.concat([engagement,b])
        print(len(engagement))
    engagement.to_csv('input/csv/engagement.csv')
