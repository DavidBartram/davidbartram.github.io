---
layout: post
title: "Sql Server Queries Task Duration Inserting Defaults"
date: 2021-10-05 14:45:39 +0100
tags: Coding, Fixes &amp; Tricks, SQL
---

# SQL Server Queries - Task Duration &amp; Inserting Defaults

![stock exchange board]({{ "images/pexels-photo-210607.jpeg" | relative_url }})

The title says it all really - two SQL (T-SQL) snippets designed for running against a Microsoft SQL Server database. They'll most likely work in whichever flavour of SQL you prefer, with a little tweaking.

The uses cases and solutions here have been simplified (to the point of absurdity!) to explain what each query does.

Task Duration
-------------

Here we have a status log of some tasks being worked on by Alice, Bob and Clare. The first status a task enters is Start, and the last status is Completed. There may be other statuses in between, such as Blocked.

| Task ID | Worker | Date       | Status    |
| ------- | ------ | ---------- | --------- |
| Task 1  | Alice  | 2021-11-19 | Start     |
| Task 2  | Bob    | 2021-11-23 | Start     |
| Task 3  | Clare  | 2021-11-23 | Start     |
| Task 3  | Clare  | 2021-11-25 | Blocked   |
| Task 3  | Clare  | 2021-11-27 | Completed |
| Task 4  | Clare  | 2021-11-28 | Start     |
| Task 1  | Alice  | 2021-12-02 | Completed |
| Task 4  | Clare  | 2021-12-07 | Completed |

Completed

You are asked to provide a list of completed tasks, their start and finish dates, and the number of days taken to complete each task.

### Query

This snippet will populate a `datatable` like the above. It then uses an INNER LEFT JOIN query, a self-join of the original table, to produce the desired output.

```sql
with datatable as (
        select 'Task 1' as 'Task ID', 'Alice' as "Worker", CAST('20211119' as date) as "Date", 'Start' as "Status"
  union select 'Task 2' as 'Task ID', 'Bob' as "Worker", CAST('20211123' as date) as "Date", 'Start' as "Status"
  union select 'Task 3' as 'Task ID', 'Clare' as "Worker", CAST('20211123' as date) as "Date", 'Start' as "Status"
  union select 'Task 3' as 'Task ID', 'Clare' as "Worker", CAST('20211125' as date) as "Date", 'Blocked' as "Status"
  union select 'Task 1' as 'Task ID', 'Alice' as "Worker", CAST('20211202' as date) as "Date", 'Completed' as "Status"
  union select 'Task 3' as 'Task ID', 'Clare' as "Worker", CAST('20211127' as date) as "Date", 'Completed' as "Status"
  union select 'Task 4' as 'Task ID', 'Clare' as "Worker", CAST('20211128' as date) as "Date", 'Start' as "Status"
  union select 'Task 4' as 'Task ID', 'Clare' as "Worker", CAST('20211207' as date) as "Date", 'Completed' as "Status"
)

SELECT initialData."Task ID", 
       initialData."Date" as "StartDate", 
       completedData."Date" as "EndDate",
       DATEDIFF(day,initialData."Date", completedData."Date") as "Duration (days)"
FROM datatable as initialData INNER JOIN datatable as completedData
  on  initialData."Task ID" = completedData."Task ID"
  and initialData."Status" = 'Start'
  and completedData."Status" = 'Completed';
```

### Output

| Task ID | StartDate  | EndDate    | Duration (days) |
| ------- | ---------- | ---------- | --------------- |
| Task 1  | 2021-11-19 | 2021-12-02 | 13              |
| Task 3  | 2021-11-23 | 2021-11-27 | 4               |
| Task 4  | 2021-11-28 | 2021-12-07 | 9               |

Inserting Default Values
------------------------

Consider a table like the below:

| Day | Value |
| --- | ----- |
| 1   | 254   |
| 3   | 665   |
| 4   | 3     |

We seem to have data for days 1, 3 and 4, but no other data. Maybe this came from an external data source didn't provide data for any other days. After talking to a domain expert, they would like a table showing days 1-5, and any day without a value should show a default value of zero.

### Query

This snippet will populate a `datatable` like the above, plus a table of `defaults`. It then uses a UNION query to produce the desired output.

```sql
with datatable as (
        select 1 as "day", 254 as "Value"
  union select 3 as "day", 665 as "Value"
  union select 4 as "day", 3 as "Value"
),

defaults as (
		select 1 as "day", 0 as "Value"
	union select 2 as "day", 0 as "Value"
	union select 3 as "day", 0 as "Value"
	union select 4 as "day", 0 as "Value"
	union select 5 as "day", 0 as "Value"
)

SELECT day, Value
FROM datatable
UNION 
SELECT day, Value
FROM defaults
WHERE defaults.day NOT IN (SELECT distinct day from datatable)
```

### Output

| Day | Value |
| --- | ----- |
| 1   | 254   |
| 2   | 0     |
| 3   | 665   |
| 4   | 3     |
| 5   | 0     |

With this technique you can easily insert nulls, zeros, or other default values into a table. You can even maintain a `defaults` table if, for some reason, the default value to be inserted is likely to vary.