---
layout: post
title: "Configuring The Nginx Proxy In An Elastic Beanstalk Linux Environment"
date: 2021-04-29 14:45:39 +0100
tags: aws fixes-&amp;-tricks
---

# Configuring the nginx proxy in an Elastic Beanstalk Linux environment

![person holding a green plant]({{ "images/pexels-photo-1072824.jpeg" | relative_url }})

How to resolve the error "upstream sent too big header while reading response header from upstream" by extending the nginx config in Elastic Beanstalk.

### Bad Gateways & Big Headers

I was recently using Elastic Beanstalk to set up a dev/test environment for a Blazor web app, running .NET 5 on Amazon Linux. Without authentication, the app was working fine. But when authentication (via Azure AD) was enabled, the site gave a "502 - Bad Gateway" error.

Elastic Beanstalk lets you easily look at the logs of the underlying EC2 instances, and I soon found the issue in the logs for the nginx proxy:

```upstream sent too big header while reading response header from upstream
```

Sure enough, the headers were rather large.

### You're gonna need a bigger buffer

Turns out it's [not unusual](https://andrewlock.net/fixing-nginx-upstream-sent-too-big-header-error-when-running-an-ingress-controller-in-kubernetes/) for nginx to choke on large headers, and the solution is to change the nginx configuration to increase the buffer size. All your `nginx.conf` file needs is something like the following:

```
proxy_buffers         8 16k;
proxy_buffer_size     16k;   
large_client_header_buffers 4 32k;
```

### Extending the nginx configuration in Elastic Beanstalk

At the time of writing this is a single instance environment, so it would be pretty easy to SSH onto the EC2 instance and append the above to nginx.conf. Not a very satisfactory solution, however, it's much more desirable to have the necessary config extension baked into the app source, so that if Elastic Beanstalk creates a new instance, the nginx proxy will be properly configured from the get-go.

As documented [here](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/platforms-linux-extend.html), this is very achievable. Simply ensure that when your application is built, the bundle will contain a folder called `.platform/nginx/conf.d/` containing any .conf files that you wish to append to the default `nginx.conf`. Elastic Beanstalk will pick these up automatically and include them in `nginx.conf`.

If you don't want to extend the nginx config, but instead overwrite it with your own version, make your own `nginx.conf` file and include it in the `.platform/nginx/` folder of your app bundle.

### Using AWS CodeBuild

This application was being built by AWS CodeBuild, so I added a command to the `buildspec.yml` to copy a file called `proxy.conf` to the appropriate folder. `proxy.conf` just contains the above text which I wanted to add to the nginx config.

The snippet below shows that the app will be published to a folder imaginatively named publish, hence copying `proxy.conf` from the root of the working directory (which is a copy of the source repo) to the folder `publish/.platform/nginx/conf.d/`

```yaml
post_build:
   commands:
     - mkdir -p publish/.platform/nginx/conf.d/ && cp proxy.conf publish/.platform/nginx/conf.d/proxy.conf
     - dotnet publish -c Release -f net5.0 -r linux-x64 -o ./publish MySubFolder/MyApp.csproj
      
artifacts:
  files:
    - ./**/*
  base-directory: publish
```
