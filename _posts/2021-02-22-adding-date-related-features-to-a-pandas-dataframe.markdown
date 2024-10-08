---
layout: post
title: "Adding Date Related Features To A Pandas Dataframe"
date: 2021-02-22 14:45:39 +0100
tags: coding data pandas python
---

# Adding Date-Related Features to a Pandas Dataframe

![calendar dates paper schedule]({{ "images/pexels-photo-273153.jpeg" | relative_url }})

This post captures a few examples of feature enrichment in Pandas. In particular, these examples focus on adding a few simple features related to the date.

### Simple Date-Related Features
```python
def add_date_features(df, date_column):
    """
    Add date related features to the input dataframe
    df = dataframe
    date_column = name of the column containing the date. date should be in Pandas datetime format.
    """

    #the year, e.g. 2017
    df['year'] = df[date_column].dt.isocalendar().year

    #the month number, e.g. January = 1
    df['month'] = df[date_column].dt.month

    #the calendar day, e.g. 13th May = 13
    df['day'] = df[date_column].dt.day

    #the calendar week, from 1 to 52
    df['week'] = df[date_column].dt.isocalendar().week

    #the day of the week as a number, Monday = 0, Tuesday = 1 ... Sunday = 6
    df['dayofweek_num'] = df[date_column].dt.dayofweek

    #the name of the day of the week as a string
    df['dayofweek_name'] = df[date_column].dt.day_name()
```

### Identifying Bank Holidays (England & Wales)

The UK government has a simple API for information about past and upcoming bank holidays, the function below returns a list of dates of England & Wales bank holidays.

```python
import requests

def get_bank_holidays():
    """
    Uses the gov.uk API bank holiday API. Returns a list of dates of bank holidays in yyyy-mm-dd format.
    """

    params = {
        "division":"england-and-wales"
    }

    response = requests.get("https://www.gov.uk/bank-holidays.json",params=params)

    response_dict = response.json()

    events = response_dict["england-and-wales"]["events"]

    dates = []

    for event in events:
        dates.append(event["date"])

    return dates
```

### Adding Bank Holiday-related Features

Depending upon your use case, it might be valuable not only to identify bank holidays, but also the next working day after a bank holiday.

```python
def add_bh_features(df, date_column):

   #get bank holiday dates and convert to Pandas dataframe containing Pandas datetimes
    bh_list = get_bank_holidays()
    bh = pd.DataFrame(bh_list, columns=['date'])
    bh['date'] = pd.to_datetime(bh['date'], format='%Y-%m-%d')

    df['is_BH']= 0

    df.loc[(df[date_column].isin(bh.date)),'is_BH']= 1

    #add feature for next working day after bank holiday
    bh['next_wd'] = bh['date'] + pd.tseries.offsets.BDay()
    
    #when the next business day is another bank holiday (e.g. Easter Monday is the next 
    #"business day" after Good Friday), that date should not be treated as a working day
    bh.loc[bh['next_wd'].isin(bh.date), 'next_wd'] = pd.NaT

    df['after_BH'] = 0

    df.loc[(df[date_column].isin(bh.next_wd)),'after_BH']= 1
```
