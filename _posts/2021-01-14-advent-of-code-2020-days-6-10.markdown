---
layout: post
title: "Advent Of Code 2020 Days 6-10"
date: 2021-01-14 14:45:39 +0100
tags: advent-of-code aoc coding python
---

# Advent of Code 2020 Days 6-10

![advent architecture blur business]({{ "images/pexels-photo-195030.jpeg" | relative_url }})

Continuing my series of posts as I work through [Advent of Code 2020](http://adventofcode.com/2020/) at my own pace. Here are some of my thoughts and solutions.

These posts will be quite brief, just a few thoughts on each puzzle and the Python 3 code I used to solve it. All code on Github [here](https://git.io/JmAvJ). The code below is for Part 2 of each day, which often incorporates Part 1 in some way.

Day 6 - [Custom Customs](https://adventofcode.com/2020/day/6)
-------------------------------------------------------------

### Thoughts

Stripped of context, the input is a text file with groups of lines separated by blank lines. In each group, you need to find how many characters appear in _every_ line of the group. I did this by first putting all the characters in the group into a set, and then taking the intersection with the set of characters on each line.

### Python Code
```python
import sys

with open(sys.argv[1]) as file:
    groups = file.read().split('\n\n')

output = []

for group in groups:
    x = set(group)
    for line in group.split('\n'):
        x = x.intersection(set(line))
    
    output.append(len(x))
        
print(sum(output))
```

Day 7 - [Handy Haversacks](https://adventofcode.com/2020/day/7)
---------------------------------------------------------------

### Thoughts

The goal here was to process a set of rules similar to the below (but much longer), and find out how many bags in total are contained in a shiny gold bag.

shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.

My solution below is...fairly unpleasant, to say the least. It's a naïve recursion approach. It's not fast, it's not pretty. The recursion in lines 18-20 below was the first way I found which worked, though it's a truly nasty bit of code which I'm sure is calling the function more times than is necessary.

If you want to see a better solution, take a look at [this solution by sophiebits](https://github.com/sophiebits/adventofcode/blob/main/2020/day07.py) which, much more sensibly, starts by processing the rules into two dictionaries - one where you can look up what bags _are contained_ in a given bag, and one where you can look up what bags _contain_ a given bag.

### Python Code
```python
import sys
import re


with open(sys.argv[1]) as file:
    rules = [line.rstrip('\n') for line in file]

count = 0

def bagcount(colour):
    nextcolour = ''
    global count
    for rule in rules:
        if rule.startswith(colour):
            for x in re.findall(r'\d+ \w+ \w+',rule):
                num = int(x.split()[0])
                nextcolour = ' '.join(x.split()[1:3])
                for i in range(num):
                        count += 1
                        bagcount(nextcolour)
            
            

bagcount('shiny gold')

print(count)
```

Day 8 - [Handheld Halting](https://adventofcode.com/2020/day/8)
---------------------------------------------------------------

### Thoughts

Here we have a simple version of a halting problem.

*   The function `run` below will execute a program as defined in the puzzle.
    *   The program **terminates** if it attempts to execute an instruction immediately after the last instruction in the program, handled on lines 13-15. In this case `run` will return `terminates: True` as part of its output.
    *   The program **enters an infinite loop** if it visits an instruction for the second time. Rather than execute the infinite loop, the `run` function actually terminates as soon as this happens. In this case `run` will return `terminates: False` as part of its output.
*   The function `findswap` is where the puzzle is actually solved - this involves searching the given program for a line where exchanging the `nop` and `jmp` commands would make the code terminate properly.

### Python Code
```python
def run(code):
    
    visited = set()

    i=0
    acc = 0

    terminates = False

    while i not in visited:
        visited.add(i)

        if i == len(code):
            terminates = True
            break
        
        else:
            op,arg = code[i].split()
            arg = int(arg)

            if op == "nop":
                i += 1
            elif op == "acc":
                acc += arg
                i += 1
            elif op == "jmp":
                i += arg

    return {'lastline': i, 'acc': acc, 'terminates': terminates }


def findswap(filename):

    with open(filename) as file:
        code = [line.rstrip('\n') for line in file]

    for i in range(0,len(code)):
        
        code2 = code[:]
        
        
        if code2[i].startswith("nop"):
            code2[i] = code2[i].replace("nop", "jmp")
            

        if code2[i].startswith("jmp"):
            code2[i] = code2[i].replace("jmp", "nop")
            

        result = run(code2)
        terminates = result["terminates"]

        if terminates == True:
            acc = result["acc"]
            print("Swapping line", i, "makes the code terminate with acc =", acc)
            break
    

findswap("bootcode.txt")
```
Day 9 - [Encoding Error](https://adventofcode.com/2020/day/9)
-------------------------------------------------------------

### Thoughts

Dealing with sublists. The input is a list of integer values. In part 1 we're looking for the first value which equals the sum of two distinct elements from the previous 25 values. In part 2 we're seeking a consecutive sublist of any length which sums to the answer to part 1.

The solution below doesn't look particularly "Pythonic" - there's a whole lot of indexing going on.

### Python Code
```python
import sys

with open(sys.argv[1]) as file:
    l = [int(line) for line in file]


#Part 1 
k=25

# Set up a list of tuples, the first element of each tuple is a value from the list,
# the second element is the set of the k previous values
m = [(l[i+k], set(l[i:i+k])) for i in range(len(l)-k)]

#for each tuple, determine if the second element (the set) contains two values which sum to the first element (the value)
for (x,y) in m:
    haspair=False
    for val in y:
        goal = x - val
        if goal in y:
          haspair=True
          
    if haspair==False:
        s = x
        break

print(s)

#Part 2
#Find a sublist of any length which sums to the answer from Part 1

def findsub():
    for k in range(2,len(l)):
        sublists = [l[i:i+k] for i in range(len(l)-k+1)]
        for x in sublists:
            if sum(x) == s:
                return min(x)+max(x)

print(findsub())
```

Day 10 - [Adapter Array](https://adventofcode.com/2020/day/10)
--------------------------------------------------------------

### Thoughts

This was _extremely satisfying_ to write.

The puzzle is a classic [Dynamic Programming](https://skerritt.blog/dynamic-programming/) problem. Given a power outlet of 0 "jolts" and a set of adapters with various distinct integer "joltage" ratings, how many ways are there to connect the outlet to your highest-rated adapter? Any adapter can be plugged into another one as long as the next adapter is rated 1-3 "jolts" higher than the previous one.

A simple recursive algorithm will work, but in order to make it more efficient in time I've used [memoization](https://chialunwu.medium.com/wtf-is-memoization-a2979594fb2a). This is a fancy word for caching the results of your function calls so you don't have to make the same function call twice. The dictionary `memo` stores all previously made function calls, to avoid needless repetition of the recursive function `cost`.

The answer for my puzzle input was that there were 97 trillion ways to plug in the adapters, and on my machine the code below runs in about 5 milliseconds. What if I removed the memoization? Well . . . [some redditors](https://www.reddit.com/r/adventofcode/comments/kasqdq/2020_day_10_part_2_i_calculated_how_long_it_would/) have estimated it as taking somewhere between a few hours and a month depending on implementation.

### Python Code
```python
import sys


with open(sys.argv[1]) as file:
    ratings = [int(line) for line in file]

memo = {}

def cost(x):

    if x in memo:
        return memo[x]
    
    ways = 0

    if x == max(ratings):
        ways = 1
    if x+1 in ratings:
        ways += cost(x+1)
    if x+2 in ratings:
        ways += cost(x+2)
    if x+3 in ratings:
        ways += cost(x+3)

    memo[x] = ways
    return ways
    

print(cost(0))
```
