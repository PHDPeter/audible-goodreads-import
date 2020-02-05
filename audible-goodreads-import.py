# So this is a somewhat manual but not nearly as manual as it could be process.
# First, follow the instructions here: https://www.themodernnomad.com/audible-statistics-extractor/
# Depending on how many pages, copy and paste the results into Excel 
# (it will auto format, though you will need to remove the header)


import audible

# example for US accounts
auth = audible.LoginAuthenticator(
    "EMAIL",
    "PASSWORD",
    locale="us"
)

# to specify another API version
library, _ = client.get(
    path="library/books",
    api_version="0.0",
    params={
        "purchaseAfterDate": "01/01/1970",
        "sortInAscendingOrder": "true"
    }
)

# Before running
# Install the required libraries: pandas and isbntools
# Modify the read_excel argument to point at your file.
# Then point the to_csv argument to wherever you want to export to.

# Go to https://www.goodreads.com/review/import, add the CSV file, and sit back and enjoy

import pandas as pd
from isbntools.app import *

df = pd.read_excel(r'/path/to/the/saved/excel.xlsx')

# Fetch ISBN from title and author using isbn tools
df['isbn'] = df.apply(lambda x : isbn_from_words(str(x.Title) + " " + str(x.Author)), axis=1 )
# Convert Dates
df["Buy Date"] = pd.to_datetime(df["Buy Date"], format="%m-%d-%y", exact=False).dt.strftime('%Y-%m-%d')
#df["Buy Date"] = df["Buy Date"]
# Add to audible
df["Bookshelves"] = "audible"
# Map the Date Read to the Buy Date as a loose proxy
df["Date Read"] = df.apply(lambda x: x["Buy Date"] if x["Time Left"] < 30 else None, axis=1)
# This doesn't actually register, but the export that Goodreads provides is Exclusive Shelf for the read status
df["Exclusive Shelf"] = df.apply(lambda x: "read" if x["Time Left"] < 30 else "currently-reading" if x["Time Left"]/x["Minutes"] < .8 else "to-read", axis=1)
# So I fix it by just appending the status to Bookshelves depending on read status. i.e. if less than 30min left, it's read. If you've listened to more than 20% of it, it's Currently Reading
df["Bookshelves"] = df.apply(lambda x: x["Bookshelves"] + " " + "read" if x["Time Left"] < 30 else x["Bookshelves"] + " " + "currently-reading" if x["Time Left"]/x["Minutes"] < .8 else x["Bookshelves"] + " " + "to-read", axis=1)
# Rename Buy Date to Date Added
df.rename(columns={"Buy Date" : "Date Added"},inplace = True)
 
df.to_csv(r'/path/to/export/audible-goodreads-import.csv')  
print ("Done")
