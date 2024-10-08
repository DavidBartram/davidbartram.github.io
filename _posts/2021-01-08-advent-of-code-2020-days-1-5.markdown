---
layout: post
title: "Advent Of Code 2020 Days 1-5"
date: 2021-01-08 14:45:39 +0100
tags: advent-of-code aoc coding python
---

# Advent of Code 2020 Days 1-5

![advent architecture blur business]({{ "images/pexels-photo-195030.jpeg" | relative_url }})

Advent is long over, but I'm working through [Advent of Code 2020](http://adventofcode.com/2020/) at my own pace. Here are some of my thoughts and solutions.

These posts will be quite brief, just a few thoughts on each puzzle and the Python 3 code I used to solve it. All code on Github [here](https://git.io/JmAvJ). The code below is for Part 2 of each day, which often incorporates Part 1 in some way.

Day 1 - [Report Repair](https://adventofcode.com/2020/day/1)
------------------------------------------------------------

### Thoughts

With the simple goal of finding the product of the three numbers in a list that add up to 2020. My first solution was horribly over-engineered. The solution below is a bit neater, but I still set a few unnecessary personal goals:

*   The puzzle input I got from AoC had only one trio with a sum of 2020, and thus only one answer for the product. I wanted to check I could deal with a list of numbers where multiple trios added to 2020. So I used my own input for the below.
*   Given that I would find multiple trios, I had to decide how to display the output. I decided to build a dictionary where the key is the trio, and the value is the product of the trio's three elements.
    *   The advantage of a dictionary, I thought, is that it won't accept multiple values for the same key.
    *   If I store the key as a `set` of 3 integers, I thought, then when the code inevitably finds a duplicate set (compare `{2001,18,1}` and `{1,2001,18}`) , it will just harmlessly overwrite the product associated with that set with an equal value.
    *   Actually....Python sets are **mutable**, so they aren't hashable, so they can't be used as dictionary keys. That's why you'll see `frozenset` below, which is an **immutable** Python data type which otherwise behaves like a `set`.

### Python Code

```python
import sys

sum_ = 2020

with open(sys.argv[1]) as f:
    lines = [int(l.rstrip('\n')) for l in f]
    trios = {}

    for line in lines:

        for line2 in lines:
            x = sum_ - line - line2

            if x in lines and len({x, line, line2}) == 3:
                trios[frozenset({x, line, line2})] = x*line*line2

    for key, val in trios.items():
        print(key, ":", val)
```

### Example Output
```
frozenset({1856, 150, 14}) : 3897600
frozenset({1312, 694, 14}) : 12747392
frozenset({1674, 196, 150}) : 49215600
```

Day 2 - [Password Philosophy](https://adventofcode.com/2020/day/2)
------------------------------------------------------------------

### Thoughts

Not much excitement here, just counting up the number of valid passwords in a list, based on some rather eccentric password policies.

### Python Code
```python
import sys

with open(sys.argv[1]) as file:
    lines = list()
    for line in file:
        line = line.replace(":", "")
        line = line.replace("-", " ")
        lines = lines + [line.strip().split()]

validcount = 0
for line in lines:
    pos1 = int(line[0]) - 1
    pos2 = int(line[1]) - 1
    char = line[2]
    password = line[3]

    if password[pos1] == char:

        if password[pos2] != char:
            validcount += 1

    elif password[pos2] == char:
        validcount += 1

print(validcount)
```

Day 3 - [Toboggan Trajectory](https://adventofcode.com/2020/day/3)
------------------------------------------------------------------

### Thoughts

A puzzle about heading down a slope in a toboggan that can apparently survive colliding with a tree. Some posters on the [subreddit](https://www.reddit.com/r/adventofcode/) decided to go the extra mile with graphics, even 3D representations in Unity! My solution is rather less ambitious.

[Indexing from zero](https://en.wikipedia.org/wiki/Zero-based_numbering) (e.g. `list[0]` is the first item in `list`) is handy when doing [modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic).

e.g. in Python `x % len(list)` will convert any integer `x` into an index that's within the bounds of `list`.

Hypothetically, if `list[1]` were the first item in `list`, you'd get an off-by-one error. For example, in a list with 30 items, `30 % len(list)` is 0 and list[0] doesn't exist! You'd need `(x % len(list))+1` and nobody wants to deal with that.

### Python Code
```python
import sys

with open(sys.argv[1]) as file:
    map_ = file.read().splitlines()

def  trees(dx, dy):
    x = 0
    y = 0
    xmax = len(map_[0])
    ymax = len(map_)
    count = 0

    if map_[x][y] == "#":
        count = 1

    while y < ymax:
        x = (x+dx)%(xmax)
        y = (y+dy)

        if y  >= ymax:
            break
        
        if map_[y][x] != "." and map_[y][x] !="#":
            print("error at x=",x, "y=",y)
            break

        elif map_[y][x] == "#":
            count += 1

    return count


print("product", trees(1,1)*trees(3,1)*trees(5,1)*trees(7,1)*trees(1,2) )
```

Day 4 - [Passport Processing](https://adventofcode.com/2020/day/4)
------------------------------------------------------------------

### Thoughts

Who doesn't love a bit of Regex matching? Thank goodness for [https://regex101.com/](https://regex101.com/).

There was a salutary lesson here - while working on Part 2, I forgot to keep enforcing the requirements from Part 1 which were still relevant. Spent a fair while looking for a coding error which was actually an error understanding the requirements.

### Python Code
```python
import sys
import re

with open(sys.argv[1]) as file:
    ports = file.read().split('\n\n')

ports = [re.findall(r'\S*:\S*', port) for port in ports]

countvalid = 0

req = {'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'}

for port in ports:

    portvalid = True
    present = set()

    for field in port:
        valid = True
        present.add(field[:3])
        x = field.partition(':')[2]

        if field.startswith('byr'):
            valid = 1920 <= int(x) <= 2002

        elif field.startswith('iyr'):
            x = int(x)

            valid = 2010 <= int(x) <= 2020

        elif field.startswith('eyr'):
            valid = 2020 <= int(x) <= 2030

        elif field.startswith('hgt'):
            
            if field.endswith('cm'):
                x = x.replace('cm', '')
                valid = 150 <= int(x) <= 193
            
            elif field.endswith('in'):
                x = x.replace('in', '')
                valid = 59 <= int(x) <= 76
            
            else:
                valid = False

        elif field.startswith('hcl'):
            valid = bool(re.fullmatch(r'#[0-9a-f]{6}', x))

        elif field.startswith('ecl'):
            valid = bool(re.fullmatch(r'amb|blu|brn|gry|grn|hzl|oth', x))

        elif field.startswith('pid'):
            valid = bool(re.fullmatch(r'[0-9]{9}', x))

        portvalid = portvalid and valid
        #print(field, valid)

    present.discard('cid')
    if present != req:
        portvalid = False

    if portvalid:
        countvalid += 1

print(countvalid)
```

Day 5 - [Binary Boarding](https://adventofcode.com/2020/day/4)
--------------------------------------------------------------

### Thoughts

Nice quick one involving a very convenient plane with 128 rows and 8 columns of seats!

### Python Code
```python
import sys


with open(sys.argv[1]) as file:
    lines = [line.rstrip('\n') for line in file]

rows = []
cols = []
IDs = []

for line in lines:
    rows.append(line[:7])
    cols.append(line[-3:])

rows = [row.replace("F","0").replace("B","1") for row in rows]
rows = [int(row,2) for row in rows] #convert from binary to decimal

cols = [col.replace("L","0").replace("R","1") for col in cols]
cols = [int(col,2) for col in cols] #convert from binary to decimal


for i in range(len(rows)):
    IDs.append(rows[i]*8 + cols[i])

print(max(IDs))


IDs.sort()

for i in range(len(rows)):
    if IDs[i] + 1 != IDs[i+1]:
        print(IDs[i] + 1)
        break
```
