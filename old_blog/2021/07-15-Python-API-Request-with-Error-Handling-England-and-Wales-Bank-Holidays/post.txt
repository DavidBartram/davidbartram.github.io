---
layout: post
title: "Python Api Request With Error Handling England Wales Bank Holidays"
date: 2021-07-15 14:45:39 +0100
tags: Coding, Fixes &amp; Tricks, Python
---

# Python API Request with Error Handling: England &amp; Wales Bank Holidays

![woman writing on whiteboard]({{ "images/pexels-photo-3861943.jpeg" | relative_url }})

A brief example of using the requests library in Python to query an API, in this case the gov.uk Bank Holidays API.

The output of this function is a list of bank holiday dates, using a stored list if the API is not available (as it was during the [Fastly internet outage](https://www.bbc.co.uk/news/technology-57399628) in June 2021.

The goal here is to provide reasonable informative error messages printed to console.
```python
def get_bank_holidays():
    """
    Uses the gov.uk API bank holiday API. Returns a list of dates of England and Wales bank holidays in yyyy-mm-dd format.
    """

    default_dates = ['2016-01-01', '2016-03-25', '2016-03-28', '2016-05-02', '2016-05-30', '2016-08-29', '2016-12-26', '2016-12-27', '2017-01-02', '2017-04-14', '2017-04-17',
    '2017-05-01', '2017-05-29', '2017-08-28', '2017-12-25', '2017-12-26', '2018-01-01', '2018-03-30', '2018-04-02', '2018-05-07', '2018-05-28', '2018-08-27', '2018-12-25',
    '2018-12-26', '2019-01-01', '2019-04-19', '2019-04-22', '2019-05-06', '2019-05-27', '2019-08-26', '2019-12-25', '2019-12-26', '2020-01-01', '2020-04-10', '2020-04-13',
    '2020-05-08', '2020-05-25', '2020-08-31', '2020-12-25', '2020-12-28', '2021-01-01', '2021-04-02', '2021-04-05', '2021-05-03', '2021-05-31', '2021-08-30', '2021-12-27', 
    '2021-12-28', '2022-01-03', '2022-04-15', '2022-04-18', '2022-05-02', '2022-06-02', '2022-06-03', '2022-08-29', '2022-12-26', '2022-12-27']

    use_default_dates = False

    params = {
        "division":"england-and-wales"
    }

    try:
        response = requests.get("https://www.gov.uk/bank-holidays.json",params=params)

        if response.status_code != 200:
            print("USING STORED BANK HOLIDAY DATES")
            use_default_dates = True

    
    except requests.exceptions.SSLError as errssl:
        print("SSL Error:", errssl)
        print("USING STORED BANK HOLIDAY DATES")
        use_default_dates = True

    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        print("USING STORED BANK HOLIDAY DATES")
        use_default_dates = True
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        print("USING STORED BANK HOLIDAY DATES")
        use_default_dates = True
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        print("USING STORED BANK HOLIDAY DATES")
        use_default_dates = True
    except requests.exceptions.RequestException as err:
        print ("Error accessing Bank Holiday API",err)
        print("USING STORED BANK HOLIDAY DATES")
        use_default_dates = True

    if use_default_dates == False:
        response_dict = response.json()
        events = response_dict["england-and-wales"]["events"]
        dates = []

        for event in events:
            dates.append(event["date"])
    
    else:
        dates = default_dates

    return dates
```