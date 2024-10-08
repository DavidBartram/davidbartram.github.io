---
layout: post
title: "How To Solve Ssl Error Unable To Get Local Issuer Certificate For Python On Windows"
date: 2021-04-13 14:45:39 +0100
tags: coding fixes-&amp;-tricks python
---

# How to solve SSL Error "unable to get local issuer certificate" for Python on Windows

![man people art sign]({{ "images/pexels-photo-4439425.jpeg" | relative_url }})

I ran into an issue where any https request from Python would fail on my Win 10 laptop, anything based on the `requests` library, which includes the humble `pip install`!

At the same time my browser had no issue making https requests.

I noticed that when I connected to my employer's corporate VPN, the issue disappeared.

In the end, the solution was to use [https://pypi.org/project/python-certifi-win32/](https://pypi.org/project/python-certifi-win32/) , which patches `certifi` (the part of requests that deals with certifications). The effect is that `requests` will recognise certifications from the Windows Certification Store, so you can verify tls/ssl connections to any server whose certificate authority is trusted by your Windows install.

The fix is as simple as:

1.  Connect to the VPN
2.  `pip install python-certifi-win32`
3.  Disconnect from the VPN

If you're using a bunch of Python virtual environments like I am, you might want to include `python-certifi-win32` in your favourite requirements.txt file, so you don't forget it when you start up a new venv!
