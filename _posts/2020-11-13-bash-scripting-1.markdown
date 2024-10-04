---
layout: post
title: "Bash Scripting 1 - the whole shebang"
date: 2020-11-13 14:45:39 +0100
tags: Bash, Bash Scripting, Coding, Linux, Scripting, Unix
---

# Bash Scripting 1 - the whole shebang

![shebang-big]({{ "images/shebang-big.png" | relative_url }})

I've spent some time over the last couple of weeks trying to learn some Bash scripting. I wanted to break out a bit of the Windows headspace and refresh my knowledge of Linux command line syntax. I'm going to document some of the key things I've learned on this blog - hopefully you find it useful.

### **Hey, what even is a Bash script?**

Without going into too much detail, Bash (the **B**ourne **A**gain **Sh**ell) is a Unix shell that interprets commands. If you're familiar with Unixland, you'll have spent a fair bit of time with commands like **`ls`** , **`grep`** and **`echo`.**

A Bash script is a text file containing a series of commands. When you execute the script, those commands are run by the Bash shell much as they would be at the command line. Bash scripting a great, simple form of automation - take a process that requires multiple command line inputs, write a script for it, and next time all you need to do is run the script. You can pass in arguments to the script, or prompt for user inputs, and all that good stuff.

### **Start with a shebang**

If you Google up some Bash scripts ([https://github.com/alexanderepstein/Bash-Snippets](https://github.com/alexanderepstein/Bash-Snippets) has some fun ones), you'll find they all have a first line that's something like `#!/bin/bash`.

The characters #! are called a "shebang", hence this post's title. But what is a line like `#!/bin/bash` doing for your script?

Well, in a very real sense, it's the shebang (or rather, what comes after) that makes your script a Bash script. `/bin/bash` is the path to the Bash interpreter. The line `#!/bin/bash` tells the machine that the file is a script, and that it should be interpreted with `bash`. If you wrote your script in Python, you should put the path to your Python interpreter here (e.g. `#!/usr/bin/python`) , and so on.

`#!/bin/bash` tells your script to be interpreted with `bash`, which is installed in the /`bin` folder. Which is where you would expect bash to be on most Linux machines.

### Which shebang to choose?

An alternative shebang line is `#!/usr/bin/env bash` . Instead of looking for `bash` in `/bin`, the script will search for `bash` in the user's `$PATH` variable, and start with the first one they can find. This approach has advantages and disadvantages, which are well explained here: [https://stackoverflow.com/questions/21612980/why-is-usr-bin-env-bash-superior-to-bin-bash](https://stackoverflow.com/questions/21612980/why-is-usr-bin-env-bash-superior-to-bin-bash)

So, you can run into controversy and confusion in the first line of your script!

Fortunately, at the moment I'm just learning the ropes, and on the Linux VM I've set up to practice, I know for sure that `#!/bin/bash` will work. So for now, that's the shebang for me.
