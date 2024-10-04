---
layout: post
title: "Reinvent 2020 Part 1 Aws Systems Manager"
date: 2021-01-04 14:45:39 +0100
tags: automation aws aws-reinvent cloud
---

# Re:Invent 2020 1 - AWS Systems Manager

![14796090251_5d6467a59b_b]({{ "images/14796090251_5d6467a59b_b.jpg" | relative_url }})

[Re:Invent](https://reinvent.awsevents.com/) is AWS's annual learning conference, and this is the first one I've been able to attend (virtually of course!). I'm going to write up my thoughts on some of the talks that I enjoyed and got value out of, though there has been a lot of other great stuff at the conference.

### "**Automate anything with [AWS Systems Manager](https://docs.aws.amazon.com/systems-manager/index.html)**"

This very engaging [talk and demo](https://virtual.awsevents.com/media/1_icyx69i0) by [Darko Meszaros](https://aws.amazon.com/developer/community/evangelists/darko-meszaros/) was focused on automating IT operations tasks with code. The talk mentioned patching, provisioning, package installation, AMI creation and remediation steps as processes ripe for automation with AWS Systems Manager.

#### Demo - automated Docker installation

The demo showed how to use Systems Manager Automation to create a runbook which installs Docker on an EC2 instance and tags the instance with a tag called `dockerinstall` with a value of `true`. This proceeds by creating two [SSM](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-ssm-docs.html) documents , one Command document and one Automation document (both in YAML format in the demo). Loosely speaking, the Command document contains the shell commands we want to run to install Docker. The automation document defines a runbook with 3 steps - check that the instance is running, run the Command document for installing docker, and tag the instance.

Once the runbook is defined, you can then run it from Systems Manager in the AWS console (or from the CLI), with the console giving a nice-looking output in terms of the steps defined in the two documents mentioned above.

#### New AWS Systems Manager features

The talk then wraps up discussing the latest features of AWS Systems Manager:

*   **[Fleet Manager](https://aws.amazon.com/blogs/aws/new-aws-systems-manager-fleet-manager/)**: for administering a fleet of servers running on AWS and on-premises, allowing you to manage VMs without RDP/SSH and perform common tasks from a single console
*   [**Application Manager**](https://docs.aws.amazon.com/systems-manager/latest/userguide/application-manager.html): discovers application resources across multiple AWS services and consolidates operational data in a single console.
*   **[Change Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/change-manager.html):** allows automated approval processes for operational changes, such as new automation runbooks. I found this particularly interesting because it ties into some of the downsides of automation - as Meszaros said during the talk, you don't really want a broken automation runbook being created and run on a Friday afternoon.

#### Takeaway

The key, as ever, to automation is the commitment to finding things to automate and automating them in a repeatable, predictable fashion - which usually means defining your automation as code. AWS Systems Manager offers one way to do that. The new features emphasize a more nuanced point, though - **you should be automating the right things, at the right time**. That's what the new tools are geared towards doing, either by improving observability with Fleet Manager and Application Manager or by improving governance with Change Manager.
