---
layout: post
title: "Understanding A Python 3 8 Quine"
date: 2021-09-02 14:45:39 +0100
tags: coding python
---

# Understanding a Python 3.8 Quine

![a primate examines themselves in the mirror]({{ "images/pexels-photo-1207875.jpeg" | relative_url }})

What is a quine?
----------------

Per the font of all human knowledge, Wikipedia, "a quine is a computer program which takes no input and produces a copy of its own source code as its only output".

Quines are named after the logician Willard Quine, and are quite interesting from a theoretical point of view and fun to think about. I thought I'd pick a Python quine and analyse how it works, and what syntactical tricks it exploits to replicate itself in the output.

Python 3.8 quine (from Stackoverflow)
-------------------------------------

Rather arbitrarily, I've picked this quine (tested in Python 3.8) from [StackOverflow](https://stackoverflow.com/questions/6223285/shortest-python-quine), in the response by user [hallo](https://stackoverflow.com/users/4698348/hallo).

```python
print((lambda x:f"{x}{x,})")('print((lambda x:f"{x}{x,})")',))
```

I just thought the syntax of it looked fun, and I wanted to understand it and hopefully share that understanding with you.

Note that Python 3.8 will usually interpret a value followed by a comma `x,` as a one-element tuple whose string representation is `(x,)`. This will be important later for keeping track of brackets!

Ingredients of the quine
------------------------

### The print statement

This line of code has only one print statement, on the outside. The second time the word print appears, it is inside a string and won't actually cause anything to be printed.

The print statement on the outside does what you'd expect, so there's not much to say about this ingredient.

### f-strings in Python

A more significant element in this quine is the use of f-strings. New in Python 3, f-strings are "formatted string literals", they allow you to insert variables or other Python expressions into a string.

To do this you simply prefix the string with an `f` or `F` before the opening single or triple quote, and contain the Python expression you want to insert in braces `{}`.

Example:
```python
name = 'Boba Fett'
age = 19
pronoun = 'he'
max_value = 10

message = f'When {name} was {age} years old, {pronoun} learned to count to {max_value}: {list(range(1,max_value+1))}'

print(message)
```
Output:
```
When Boba Fett was 19 years old, he learned to count to 10: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

### Lambda functions in Python

This quine uses lambda notation to define a function. This is a useful notation to define a function in a single line by specifying the output that results from a given input.

Let's look at an example:

```python
func = lambda x:x*5
```

Here we have defined a function `func` which takes an input `x` and returns an output `x*5`.

Having defined `func` , we can apply it to a few different inputs:

```python
print(func(3))
print(func('jiminy'))
print(func(300.5))
```

which will yield, predictably:

```
15
jiminyjiminyjiminyjiminyjiminy
1502.5
```

### The function `lambda x:f"{x}{x,})"`

The workhorse of this quine is the function `lambda` `x:f"{x}{x,})"`

Let's try and break it down - this takes an input `x` and returns an output `f"{x}{x,})"`

The output is an f-string which substitutes first the value of x, followed by the one-element tuple `(x,)`, then appends the character `)`. So we expect this function to return the input, followed by a tuple containing the input, then the `)` character.

Let's try it a couple of times:

```python
y = lambda  x:f"{x}{(x,)})"

print(y('banana'))
print(y(5))
print(y((1,3,5)))
```

**Output:**
```
banana('banana',))  
5(5,))  
(1, 3, 5)((1, 3, 5),))
```

So this function yields a string output consisting of the string representation of the three parts below, concatenated together:

1.  The input
2.  A tuple containing only the input
3.  A closing parenthesis character `)`

However something interesting happens if we feed this function an expression like `'chimp',`

Normally we expect Python to recognise this as a tuple and treat it the same way as the single-item tuple `('chimp',).` In that case we would expect the output `('chimp',)(('chimp',) ,))`

But test it, and you'll see a different behaviour:

```python
y = lambda  x:f"{x}{(x,)})"

print(y('chimp',))
```
**Output:**
```
chimp('chimp',))
```

What??? That looks nothing like what happened when we used the tuple `(1, 3, 5)` as an input.

Something curious is going on. To understand what, consider what happens if you try to evaluate `y('chimp','apple','grape')`. You'll get an error - the function y is expecting one positional argument, not three!

See, Python regards `` `y('chimp','apple','grape')` `` not as an instruction to take the tuple `('chimp','apple','grape')` and pass it into the function `y`, but rather as an instruction to take the strings `'chimp'`, `'apple'` and `'grape'` and pass them to the function as positional arguments.

Likewise, when we evaluate `` `y('chimp',)` `` , Python will see `'chimp',` not as a tuple argument, but as a tuple of positional arguments that happens to contain just one argument.

`y('chimp',) == y('chimp') == chimp('chimp',))`

This trick is crucial to this particular quine!

Reading the quine
-----------------

Let's take a look at the whole quine:

```python
print((lambda x:f"{x}{x,})")('print((lambda x:f"{x}{x,})")',))
```

So let's work through and see what this does. Ignoring the print statement for a moment:

```python
(lambda x:f"{x}{x,})")('print((lambda x:f"{x}{x,})")',)
```

So we take our beloved function from the previous section, and give it the input `'print((lambda x:f"{x}{x,})")',`

Per the `'chimp'`, example above, we know this output will be identical to:

```
(lambda x:f"{x}{x,})")('print((lambda x:f"{x}{x,})")')
```

Now we expect:

1.  The input == `print((lambda x:f"{x}{x,})")`
2.  A tuple containing only the input == (`'print((lambda x:f"{x}{x,})")'`,)
3.  A closing parenthesis == `)`

Concatenate the string representations of the above, and get:

```
print((lambda x:f"{x}{x,})")('print((lambda x:f"{x}{x,})")',))
```

This is the code of the quine itself, which will be wrapped in the print function we ignored earlier. Therefore, the quine will output its own code to the console. So it is a quine!

The "tricks" - parentheses and commas
-------------------------------------

This particular quine exploits two main quirks of Python.

Firstly, the fact that parentheses `()` are used in two different ways. They can be used to delimit a tuple `(a,b)` or to pass argument(s) to a function `func(a,b,c...)`. One could argue about how different the two uses are, since the arguments passed to a function do constitute a tuple...leaving that quibble aside, these can be thought of as distinct uses for parentheses.

The parentheses in this quine are, at various points, characters in a string, tuple delimiters, and delimiters of the argument(s) passed to a function.

The second quirk is that for any function `func` and argument `x`, we have the following: `func(x,) == func(x)`.

By exploiting these quirks, this quine manages to print itself. Fun!
