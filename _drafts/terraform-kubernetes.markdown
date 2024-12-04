---
layout: post
tipue_search_active: true
title: "Terraform & Kubernetes - a simple project"
date: 2024-10-14 15:04:44 +0100
tags: coding iac terraform
---

# Terraform & Kubernetes - a simple project

I took a couple of days to work with Terraform recently. I decided that a simple project to deploy an AWS EKS cluster with a Kubernetes service that would run a simple web app over HTTPS would be a good way to learn some Terraform fundamentals.

The project can be found here [Terraform-k8s on GitHub](https://github.com/DavidBartram/terraform-k8s)

This is set up to host any simple single-container web app, for example the [nginx image on DockerHub](https://hub.docker.com/_/nginx) can be used to display a simple welcome page.

I wanted some amount of interactivity, so I hosted my [Godbound Dice Roller](https://github.com/DavidBartram/godbound-dice-roller) app, a very simple Flask app I made to make it easier to roll for damage in an obscure tabletop RPG.

## Basic Experiments

## Project Structure

### Providers

### eks-cluster module

### kubernetes module

## Key Challenges

### Managing Kubernetes cluster with the Terraform kubernetes provider

### HTTPS (without an Ingress)

### Dependencies

## Final Thoughts
