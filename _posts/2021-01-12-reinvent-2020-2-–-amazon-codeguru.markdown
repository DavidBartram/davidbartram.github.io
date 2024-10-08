---
layout: post
title: "Reinvent 2020 2 Amazon Codeguru"
date: 2021-01-12 14:45:39 +0100
tags: automation aws aws-reinvent cloud coding
---

# Re:Invent 2020 2 – Amazon CodeGuru

![14796090251_5d6467a59b_b]({{ "images/14796090251_5d6467a59b_b.jpg" | relative_url }})

[Re:Invent](https://reinvent.awsevents.com/) is AWS's annual learning conference, and this is the first one I've been able to attend (virtually of course!). I'm going to write up my thoughts on some of the talks that I enjoyed and got value out of, though there has been a lot of other great stuff at the conference.

### "Continuous Improvement of Code Quality with Amazon CodeGuru"

This [talk](https://virtual.awsevents.com/media/1_yssmnql1) was given by [Nikunj](https://www.linkedin.com/in/nikunj-vaidya-a15a471/) [Vaidya](https://www.linkedin.com/in/nikunj-vaidya-a15a471/). It was my first introduction to CodeGuru, a product which was announced at Re:Invent 2019. It's a machine-learning based service for automated code review and application profiling.

#### CodeGuru Reviewer

Amazon CodeGuru Reviewer currently supports Java and Python (available in preview) code stored in GitHub, GitHub Enterprise, Bitbucket and AWS CodeCommit repositories.

One point that Vaidya was keen to stress is that CodeGuru Reviewer does not replace human code reviews, it augments them. Where human code reviews will tend to focus on the business logic of the application, CodeGuru can support by detecting issues related to functional correctness. It can help to catch "hard to spot" code defects - [race conditions](https://stackoverflow.com/questions/34510/what-is-a-race-condition), data corruption, [thread concurrency](https://blogs.grammatech.com/fun-with-concurrency-problems), [resource leaks](https://stackify.com/memory-leaks-java/) - using a machine learning system trained on many thousands of code reviews.

The output of Reviewer is actionable recommendations, like the ones below, where we can see that CodeGuru has flagged a possible resource leak, a suggestion to use a batch API operation for efficiency, and a pagination issue.

![]({{ "images/image.png" | relative_url }})

#### CodeGuru Profiler

Helps you understand your application structure in runtime, for example by producing a [flame graph](http://www.brendangregg.com/flamegraphs.html) representation of CPU or latency data, with each block representing a function. This can let you examine cascading function calls and identify issues with high CPU usage or latency, and their cause. Profiler also provides automatic recommendations.

![]({{ "images/image-1.png" | relative_url }})

#### Takeaway

This was a good introduction to the CodeGuru tool, and has left me with questions to ponder. I'm interested to find out how CodeGuru Reviewer compares to similar tools on the market (for example [SonarQube](https://www.sonarqube.org/)), and also delve a bit more into why the flame graph representation is particularly useful.
