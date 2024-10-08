---
layout: post
title: "Reflections On The Aws Solutions Architect Associate Certification 2021"
date: 2021-06-03 14:45:39 +0100
tags: aws
---

# Reflections on the AWS Solutions Architect Associate certification (2021)

![person holding black pen]({{ "images/pexels-photo-1109541.jpeg" | relative_url }})

Last week I sat and passed the AWS Solutions Architect Associate exam (SAA-C02), and I'm here to share a few thoughts on preparation and the experience of the exam itself.

Preparation
-----------

### [A Cloud Guru SAA-C02 Course](https://acloudguru.com/course/aws-certified-solutions-architect-associate-saa-c02)

One key to my preparation strategy was the [A Cloud Guru SAA-C02 course](https://acloudguru.com/course/aws-certified-solutions-architect-associate-saa-c02). Like many people, I'm coming into A Cloud Guru content via my Linux Academy subscription, now that the two have merged.

In my experience the ACG courses are a little less detailed and it does annoy me that they focus explicitly on the exam rather than the skills and knowledge themselves. Obviously you don't want to get dragged down massive tangents that cover material beyond the cert you're preparing for, but it's nice to think of the cert in terms of a knowledge base rather than just cramming for a test.

That said, the course was a great backbone for study and the hands-on labs are really useful for practicing without using your own AWS account.

### [Whizlabs Practice Tests](https://www.whizlabs.com/aws-solutions-architect-associate/)

You may be wondering how I can criticise ACG for being too test-focused, and then recommend a pack of practice exams. I used to be a maths teacher, and one of the most interesting and useful things I learned was how to integrate assessment into the learning process. A test can measure your learning, yes, but it can also guide your learning.

It's important to save some practice tests for near the exam, when you're ready to start drilling and aiming to get a good score. But first, before I've even completed an end-to-end study of a certification's topics, I'll take a couple of practice tests and fail them miserably. This provides a random-access dip into the course material, and you'll start to see recurring keywords and concepts. This is my stimulus to go and watch some videos, read some docs, and try some stuff in a hands-on lab or in my own AWS account. Personally I find this much more motivating than studying sequentially. Ploughing through Section 5 - AWS Database Solutions is all well and good, but if I've been asked a couple of questions about DynamoDB, then I really want to find out about that.

### Make your own glossary

A certification like this is mostly about breadth and not depth. You will get the occasional question that probes deeply, most likely on a favourite topic like CloudFront or how to architect a 3-tier web app, but a lot of questions will test your understanding of the purpose, pros/cons, and basic configuration of what seems like a million AWS services. Athena is not Aurora. SQS and SNS are completely different. AWS Shield, that's something which protects your application, right? OK, so in that case what's a Web Application Firewall?

It's all in the docs, of course, and in countless study guides you can find online. But for me the best approach is to start building up your own glossary. I used an Excel worksheet so I would be easily able to filter my entries by category etc. You might want to use flashcards, or anything else really. The point is to record the information yourself, express things in your own words.

This helps embed the learning. It also gives you something to do when you have a light-bulb moment - go and get it written down in your glossary. When you get a handle on Route 53 routing policies or the difference between a standard and FIFO queue in SQS, you go and write it down. You update any related references in your glossary, make sure the document as a whole reflects that new piece of knowledge. Otherwise, if you're anything like me, you'll be revisiting the same topic again 48 hours later, feeling like you're back where you started.

The Exam
--------

It would be inappropriate to talk in any real detail about the questions I got on my exam, and in any case, there's a large question bank and any given person's experience may be different. So all I'm going to do is highlight some general themes and things that might be a stumbling block.

### Don't panic!

Staying calm is important. If you're anything like me, you will find the real exam more challenging than your practice tests, and the exam is under no obligation to "warm you up" with nice question or two. Press on, flag lots of questions for review if you need to. You will find there's a big chunk of the exam that you can answer comfortably, but it won't feel like it because your mind will obsess on the questions that baffle you at first.

### Don't be surprised if you need to do some calculations.

You may need to do the IT equivalent of converting inches per minute to furlongs per fortnight.

The correct solution to choose may depend on a specific number that you have to calculate out of the question - whether that's an execution time or a throughput figure or a volume of data. Again, don't panic - your testing software will probably provide a whiteboard and/or comment box for each question. If you need to math it out, take a deep breath and write down each step.

Questions like these are a good candidate to leave and come back to. You don't want to lose time going down a numerical rabbit hole if there are still low-hanging fruit elsewhere on the exam.

### Aurora

_Personally_ I wished I'd had a deeper understanding of Aurora when I went in to the exam. This may just be the luck of the draw in terms of questions, or just a gap in my own personal preparation. But there it is!

### Read and re-read: answers can hinge on a single word or phrase

If you're a relatively fast reader like me, you might want to look at every question twice. Because sometimes the dilemma between two plausible options is solved by one fact hidden in a dense paragraph about the customer's requirements. I revisited every question on the test at least once to look at it with a fresh pair of eyes, and I changed quite a few of my initial anwers.

### Understand costs, but maybe don't obsess on figures

You will definitely be asked to choose the most cost-effective option out of a set of possible solutions. You might be able to rule out one or two of the answers as not being viable solutions to the problem, but then you'll have to tie-break the remaining ones based on which is cheapest.

In my experience of the exam, this will rarely be about requiring to memorise the exact costs of various services (these vary by region anyway). It's more about being able to rank options from cheap to expensive, and understanding what the trade-offs are. Spot EC2 instances are very cheap, but they're not going to be viable for every use case.

Understand the metrics that affect the cost of a service, again, not necessarily the figures, but which factors affect the price and which do not.

Conclusion
----------

This is a fun exam to study for, and a great way to get a bird's eye view of a wide variety of different AWS services and what they do. This might be valuable if your practical AWS experience so far has been limited to using a small number of services, and you want a better idea of what's out there.

Personally I see Solution Architect Associate less as a stepping stone to Solution Architect Professional (though it certainly can be). I see it as a serious upgrade to the Cloud Practitioner certification in terms of giving you a broad-based grounding in AWS, allowing you to understand more about the tools at your disposal to solve problems using AWS.
