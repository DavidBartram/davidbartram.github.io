---
layout: post
tipue_search_active: true
title: "Terraform, Kubernetes, EKS - a simple project"
date: 2024-10-14 15:04:44 +0100
tags: coding iac terraform
---

# Terraform, Kubernetes, EKS - a simple project

I took some time recently to work with Terraform. I decided that a simple project to deploy an AWS EKS (Elastic Kubernetes Service) cluster with a Kubernetes service that would run a simple web app over HTTPS would be a good way to learn some Terraform fundamentals.

The project can be found here [Terraform-k8s on GitHub](https://github.com/DavidBartram/terraform-k8s)

This is set up to host any simple single-container web app, for example the [nginx image on DockerHub](https://hub.docker.com/_/nginx) can be used to display a simple welcome page.

I wanted some amount of interactivity, so I hosted my [Godbound Dice Roller](https://github.com/DavidBartram/godbound-dice-roller) app, a very simple Flask app I made to make it easier to roll for damage in an obscure tabletop RPG.

## Basic Experiments

In the `basic-experiments` directory I played with some features of Terraform, creating EC2 instances with random names and and create an EC2 using the latest Amazon Linux AMI.

## Project Structure

The main EKS Terraform project lives in the `k8s` directory, and here I structured the Terraform project into modules and used [`terraform-docs`](https://github.com/terraform-docs/terraform-docs) for automatic documentation.

The [project repo](https://github.com/DavidBartram/terraform-k8s) itself contains the most detailed guide, I will just summarise a few points here.

The main module takes a docker hub image ref for the web app you want to host on EKS, a Route53 domain name and hosted zone ID (for a hosted zone you've already set up separately), and a few other details. Given this, it will create an EKS cluster, deploy the app to the cluster, and serve the app at the given domain name. It will output the URL at which you can test the web app.


### Providers

#### AWS
Unsurprisingly this project uses the standard Terraform [`aws`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs) provider to deploy resources to an AWS account.

#### Kubernetes
Unsurprisingly this project uses the standard Terraform [`kubernetes`](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs) provider so that Terraform can interact with the Kubernetes cluster on EKS without needing to use `kubectl` commands.

```hcl
provider "kubernetes" {
  host                   = module.eks-cluster.cluster_endpoint
  cluster_ca_certificate = base64decode(module.eks-cluster.cluster_certificate_authority_data)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["--profile", var.profile, "eks", "get-token", "--cluster-name", module.eks-cluster.cluster_name]
  }
}
```

We can see that the provider uses an AWS CLI call to to the `aws eks get-token` API to obtain credentials for the EKS cluster.

This allows for some declarative interaction with the cluster, though a potential expansion would be to use [Helm charts](https://registry.terraform.io/providers/hashicorp/kubernetes/latest/docs) for this purpose.

### eks-cluster module

This module handles the AWS infrastructure needed for the kubernetes app to be deployed.

It sets up a VPC, an EKS cluster, and an Amazon Certificate Manager certificate to allow the web app to be served over HTTPS.

### kubernetes module

This module creates a Kubernetes deployment and service, along with a Route53 DNS record (an A record) to point to the deployed service. For this project I didn't want to add an ingress, so to simplify matters the service only listens on HTTPS on port 443 and does not have redirection of HTTP to HTTPS.

## Brief Comparison with CloudFormation

Having worked a great deal with AWS CloudFormation, Terraform is significantly different. The ease with which I can make and combine modules, and understand them by way of their inputs and outputs, is very impressive. It was also a welcome change to see `Terraform plan` determine the current state of the resources in AWS before deciding what to do - CloudFormation is notoriously reliant on the previously deployed template as a record of current state. Terraform instead queries AWS APIs to determine the current state, and thus can easily detect and remediate drift - a feature I enjoyed playing around with by manually adding unneccessary tags to resources and watching Terraform squash them.

## Final Thoughts

This was an enjoyable project to work with Terraform and Kubernetes, deploying a public-facing HTTPS web app entirely from declarative code. I was a little disappointed with cases where I needed an explicit `depends_on`, such as ensuring that the Route 53 records associated with the ACM certificate validation were deployed after the ACM certificate...I might naively have hoped that Terraform's AWS provider could determine the right order for those (given that the certificate resource's attributes are referenced in the Route 53 resource). Likewise I had to explicitly note that the Route53 A record pointing to the web app service should only be deployed after the web app service.