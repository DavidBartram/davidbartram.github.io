---
layout: post
title: "Advent Of Code 2021 Days 1-5"
date: 2021-12-17 14:45:39 +0100
tags: Advent of Code, Coding, Python
---

# Advent of Code 2021 Days 1-5

![christmas tree decorated with baubles and garland]({{ "images/pexels-photo-6211095.jpeg" | relative_url }})

This year I'm a bit more timely with [Advent of Code 2021](http://adventofcode.com/2021/)! Really enjoying it so far! Here are my thoughts and solutions for the first 5 days of coding Christmas!

These posts will be quite brief, just a few thoughts on each puzzle and the Python 3 code I used to solve it. All code on Github [here](https://git.io/JmAvJ). The code below is for Part 2 of each day, which often incorporates Part 1 in some way.

Day 1 - [Sonar Sweep](https://adventofcode.com/2021/day/1)
----------------------------------------------------------

### Thoughts

A bit of data manipulation here. Starting with a list of integers, consider a sliding window of three values at a time. Calculate the sum of the values in each window, and compare it to the previous sum.

The goal is to output the number of sums which are larger than the previous sum.

The method below is fairly straightforward, calculating a list of all the sums first. I then offer two ways of calculating the required output.

The first way uses indexing, while the second way uses the [zip](https://www.w3schools.com/python/ref_func_zip.asp) function.

Zip is one of my favourite python functions - it produces a "zip object", an iterator of tuples, pairing up the elements from each input iterator. So if `list1` is [`a,b,c,d,e]` and `list2` is `[1, 2, 3]` then `zip(list1,list2)` will contain the tuples `(a,1)`, `(b,2)` and `(c,3)`. The length of the output is determined by the shorter of the two inputs.

zip(list,list[1:]) will produce a list of tuples of consecutive elements in the list, for example:

`list = [1,2,3,5,8,13]`

then `list[1:] == [2,3,5,8,13]`

and `zip(list,list[1:])` contains `(1,2) , (2,3) , (3,5), (5,8)` and `(8,13)`

Given that, hopefully the list comprehension below makes sense. Remember that when summing a list of booleans, True will be treated as 1 and False will be treated as 0.

### Python Code
```python
import sys


with open(sys.argv[1]) as f:
    depths = [int(l.rstrip('\n')) for l in f]

#calculate sums of windows of 3 depths each
sums = []

window_size = 3

for i in range(len(depths)-window_size+1):
    sums.append(sum(depths[i:i+window_size]))

#non-pythonic way with indexing
count = 0

for i in range(1,len(sums)):
    if sums[i] > sums[i-1]:
        count += 1

print(count)


#more pythonic way with list comprehension

increase = [x<y for x,y in zip(sums,sums[1:])]

print(sum(increase))
```

Day 2 - [Dive!](https://adventofcode.com/2021/day/2)
----------------------------------------------------

### Thoughts

Now we are keeping track of the movements of the elves' Christmas submarine.

We get a set of instructions something like the following.

We need to keep track of the sub's horizontal position `x` and depth `y`, and also its current `aim` value, which tells you the direction the sub is currently pointing in, and thus how it will move when told to go "forward".

Our input is a text file with instructions like forward 3, "down 7", "up 2" etc, obeying the following rubric:

*   `down X` _increases_ your `aim` by `X` units.
*   `up X` _decreases_ your `aim` by `X` units.
*   `forward X` does two things:
    *   It increases your horizontal position by `X` units.
    *   It increases your depth by your aim _multiplied by_ `X`.

The required output is the product of `x` and `y` after all the instructions in the input file have been followed. The code below pretty much follows the rubric above line by line. :-)

### Python Code
```python
import sys

with open(sys.argv[1]) as file:
    moves = [line.rstrip('\n') for line in file]

(x,y, aim) = (0,0,0)

for move in moves:
    dir, value = move.split()

    value = int(value)
    
    if dir == 'forward':
        x += value
        y += aim*value
    
    elif dir == 'up':
        aim -= value
    
    elif dir == 'down':
        aim += value

print(x*y)
```

Day 3 - [Binary Diagnostic](https://adventofcode.com/2021/day/3)
----------------------------------------------------------------

### Thoughts

We are given a list of binary numbers. We need to filter this list down to two values called the "**oxygen generator rating**" and the "**CO2 scrubber rating**".

Apply the following procedure to filter the list to a single value:

*   Start with the full list of binary numbers and consider the first bit of each number
*   Discard all numbers which do not match the relevant _bit criteri_on
*   If you only have one number left, stop; this is the rating value for which you are searching.
*   Otherwise, repeat the process, considering the next bit to the right.

The _bit criterion_ varies depending upon which rating you want to find:

*   To find **oxygen generator rating**, determine the _most common_ value (`0` or `1`) in the current bit position, and keep only numbers with that bit in that position. If `0` and `1` are equally common, keep values with a `_1_` in the position being considered.
*   To find **CO2 scrubber rating**, determine the _least common_ value (`0` or `1`) in the current bit position, and keep only numbers with that bit in that position. If `0` and `1` are equally common, keep values with a `_0_` in the position being considered.

In the code below, the rating is found via the `get_rating` function, which has a Boolean argument `co2` which should be set to `True` to calculate **CO2 scrubber rating**, or `False` to calculate **oxygen generator rating**. The puzzle requires calculating both ratings, multiplying them, and returning the value in decimal notation.

The function is recursive, moving on to the next bit and filtering the list further until it reaches the base case, when the list has only 1 element.

### Python Code
```python
import sys
from math import ceil

with open(sys.argv[1]) as file:
    values = file.read().splitlines()

def get_rating(nums, i, co2):
        if len(nums) == 1:
            return nums[0]
        
        else:
            ones = sum([num[i]=='1' for num in nums]) #number of ones in the column being considered
            
            comparator = '0'

            if (co2==True and ones < ceil(len(nums)/2)) or (co2==False and ones >= ceil(len(nums)/2)) :
                comparator = '1'

            nums = [num for num in nums if num[i]==comparator] #filter the list

            return get_rating(nums,i+1,co2)


o2 = get_rating(values,0, co2=False)
co2 = get_rating(values,0, co2=True)

print(int(o2,2)*int(co2,2))
```

Day 4 - [Giant Squid](https://adventofcode.com/2021/day/4)
----------------------------------------------------------

### Thoughts

The giant squid loves bingo, apparently. Each time a number is drawn, cross off all matching numbers on all the bingo cards.

Given a list of bingo cards and a list of numbers to be drawn, the goal is to find the **score** of the _last_ card to win, and multiply it by the last number drawn. The score of a card is the sum of all the numbers on the card which have not been crossed off.

Each bingo card is a 5x5 grid of integers, and a card wins when a full row or column has been crossed off. Diagonals do not count (thankfully!).

My approach below does not involve "marking" the cards - I don't keep track of whether any given number on a card has been marked. Instead I repeatedly add the next number to the list of numbers drawn so far, and then iterate over the cards, using simple set operations to determine if the card wins.

This is probably inefficient compared to keeping a record of which numbers have been marked, but its the approach that occurred to me and it runs in reasonable time on my machine. I try not to let the perfect be the enemy of the good when doing these puzzles - which is handy as my code is far from perfect!

One trick that I didn't initially realise, is the fact that the columns of each bingo card can be appended to the card as extra rows. When I initially solved the puzzle, I made a transposed version of each bingo card and checked the whole set.

The Python one-liner:

```python
grids = [grid + [[row[i] for row in grid] for i in range(len(grid))] for grid in grids]
```

is pretty ugly-looking, but it appends the columns to each bingo card as new rows, as required.

Really there's nothing too clever below. There's a list called `nums_so_far` of numbers drawn so far, and a list of `remaining_cards` to keep track of which indices of the `card`s list represent cards that are still in play. Iteratively we append a new number to `nums_so_far`, then check all the cards, remove the indices of any winners from `remaining_cards`, and repeat until only one card survives.

### Python Code
```python
import sys

with open(sys.argv[1]) as file:
    data = file.read().split('\n\n')

    win_nums = data[0].split(',')

    grids = [x.split('\n') for x in data[1:]]

    grids = [[x.strip().replace('  ', ' ').split(' ') for x in grid] for grid in grids]

    grids[-1].remove([''])

#append columns to each grid as if they were additional rows
grids = [grid + [[row[i] for row in grid] for i in range(len(grid))] for grid in grids] 

def check(card,nums):
    for row in card:
        if set(row).issubset(set(nums)):
            return True

def score(card,nums):
    nums_on_card = set([val for row in card for val in row])
    scores = nums_on_card - set(nums)
    total = sum([int(score) for score in scores])
    return total

def part2_play(cards,nums):

    nums_so_far = []

    #list of indices of cards still in play
    # e.g. if cards[3] is still in play, then 3 will be in remaining_cards
    remaining_cards = list(range(len(cards)))

    for num in nums:
        nums_so_far.append(num)

        for i in remaining_cards:
            
            if check(cards[i],nums_so_far) == True:
                remaining_cards.remove(i)

                if len(remaining_cards) ==0:
                    final_card = cards[i]
                    return score(final_card,nums_so_far)*int(num)                

print(part2_play(grids,win_nums))
```

Day 5 - [Hydrothermal Venture](https://adventofcode.com/2021/day/5)
-------------------------------------------------------------------

### Thoughts

Here we are given a set of lines. They are specified by the coordinates of their end points. The lines are either horizontal, vertical or at exactly 45 degrees. Our goal to determine the number of points with integer coordinates where two or more lines intersect.

Putting aside vertical lines, the horizontal and diagonal lines will all have integer gradients (in fact all the gradients are either 0, +1 or -1). This means to find the integer coordinates a line passes through, we just need to step through from the start to the end, changing x by 1 and y by the gradient for each step. Each step will produce a new point on the grid that the line passes through, so we should increment the count of intersecting lines at that point by one. We stop when we reach the end point.

Vertical lines have infinite gradient but are easy to step through in a similar way, changing y by 1 each step and leaving x alone.

There is no distinction between the "start" and "end" points of a line, and so the code sometimes swaps them so that they can be stepped through by _increasing_ x by 1 per step (for non-vertical lines) or by _increasing_ y by 1 per step (for vertical lines). This is just for convenience.

### Python Code
```python
import sys
from collections import defaultdict

with open(sys.argv[1]) as file:
    data = file.read().splitlines()

end_points = []

#Process each line to produce a list of lists of endpoints
#e.g. end_points = [ [(3,2),(4,2)], [(1,1), (5,5)], ....]

for line in data:
    coords = line.replace(' -> ', ',').split(',')
    end_points.append([(int(coords[0]),int(coords[1])),(int(coords[2]),int(coords[3]))])

#dictionary from coordinate tuples (x,y) to number of overlapping lines at that point
overlap_count = defaultdict(lambda: 0)

dx,dy = 0,0

for pair in end_points:
    start = pair[0]
    end = pair[1]

    #vertical lines need special treatment as their gradient is undefined
    if start[0] == end[0]:

        #for convenience the point with lower y-value will be used as the start
        if start[1] > end[1]:
            start,end = end,start
        
        
        dx,dy = 0,1
        #an integer step along a vertical line adds +0 to x and +1 to y

    #horizontal and diagonal lines
    else:
        #for convenience the point with lower x-value will be used as the start
        if start[0] > end[0]:
            start,end = end,start
        
        dx = 1
        dy = int((end[1]-start[1])/(end[0]-start[0])) #gradient

        #an integer step along the line adds +1 to x and +(gradient) to y
    
    overlap_count[start] += 1
    (x,y) = start

    #keep taking integer steps along the line
    #until we reach the end point
    while (x,y) != end:
        x,y = x+dx,y+dy
        overlap_count[(x,y)] +=1 #increment the count of lines crossing that point


count = sum([value>1 for value in overlap_count.values()])

print(count)
```