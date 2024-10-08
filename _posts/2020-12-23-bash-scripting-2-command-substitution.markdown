---
layout: post
title: "Bash Scripting 2 Command Substitution"
date: 2020-12-23 14:45:39 +0100
tags: bash-scripting coding
---

# Bash Scripting 2 - Command Substitution

![backticks-vs-dollarsign]({{ "images/backticks-vs-dollarsign-big-3.png" | relative_url }})

Let's ask a very simple question - how do I make a Bash command which will print the current date?

Naturally you're going to want to turn to the `date` command, and maybe a formatting option if you don't want the full date and time. For example, `date +%F` if you want your output in DDDD/MM/DD.

What you need is **command substitution** - in this case you want to call a command in the middle of the string you want to print, have the command evaluate, and then put the output in the proper part of the string.

Backticks `...`
---------------

For a long time while learning Bash, I thought there was only one way to do command substitution, namely using the backtick character `` ` `` to enclose the command.
```bash
$ echo "The date is `date +%F` at the time of writing"
```
```
The date is 2020-12-23 at the time of writing
```

The output is as desired. Lovely, right? Well...we'll see about that.

Dollar Brackets $(...)
----------------------

However, it turns out this is a legacy Bourne shell syntax, and has some limitations (see below). These days the [POSIX](https://opensource.com/article/19/7/what-posix-richard-stallman-explains) standard is to enclose the command in `$( )` - this convention is even respected by modern Bourne shells, though they will accept the backtick syntax as well.

```bash
$ echo "The date is $(date +%F) at the time of writing"
```
```
The date is 2021-12-23 at the time of writing
```

So far, seems much the same. But there are some differences when you look deeper.

Dollar Brackets vs Backticks
----------------------------

So - if both versions will work (assuming a suitable shell), then why do we care? Why am I taking the trouble to un-learn command substitution with backticks and start doing it with dollar brackets?

Largely, it's because backticks are difficult to read and have some unexpected behaviour

### Backtick is an annoying character

The backtick `` ` `` is easily confused with the single quote `'` - if I had my druthers, backticks wouldn't be used in coding AT ALL, for that reason alone. They're also easily missed when near to double quotes.

### Backslashes and quotes behave unexpectedly with `...`

A double backslash is treated rather strangely by backticks:

Consider wanting to print `\x` for some reason.
```bash
$ echo \\x
```
```
﻿\x
```

The first backslash is there as an escape character, so that the second backslash appears in the output. I'm sure nothing will go wrong when I use this in a command substitution...

```bash
echo `echo \\x`
```
```
x
```

I beg your pardon?

```bash
echo $(echo \\x)
```
```
\x
```

Much better, thank you `$(...)`. A similar behaviour crops up with single quotes, which can easily lead to very messy commands using the backtick syntax.

### Nesting with backticks is messy

```bash
echo "Next year will be 20`expr `date +%y` + 1`." 
```
```
Next year will be 20date +%y.
```

....that doesn't look right. Do I have to escape the inner backticks?

```bash
echo "Next year will be 20`expr \`date +%y\` + 1`." 
```
```
Next year will be 2022.
```

It's functional, but it's not pretty compared to:

```bash
echo "Next year will be 20$(expr $(date +%y) + 1)." 
```
```
Next year will be 2022.
```

Conclusion
----------

Use `$(...)` for command substitution if your shell supports it. It's really as simple as that, as far as I can see. Comment if you have a different perspective!

To find out more, take a look at:

*   [https://pubs.opengroup.org/onlinepubs/9699919799/xrat/V4_xcu_chap02.html#tag_23_02_06_03](https://pubs.opengroup.org/onlinepubs/9699919799/xrat/V4_xcu_chap02.html#tag_23_02_06_03)
*   [http://mywiki.wooledge.org/BashFAQ/082](http://mywiki.wooledge.org/BashFAQ/082)
