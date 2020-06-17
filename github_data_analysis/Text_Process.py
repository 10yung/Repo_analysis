import pandas as pd
import re

df = pd.read_csv('./Pending_Dataset/javascript_github_1.csv')
raw_html = df.to_csv(sep=' ', index=False, header=False)
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    exclusionList = ['#','\*','-', '👆','⚠',cleanr,'http[s]?://\S+']

    for a in range(0, len(exclusionList)):
        raw_html = re.sub(exclusionList[a], '',raw_html)

    # print(raw_html)

cleanhtml(raw_html)




