---
tags:
  - GDPR
  - analytics
  - reverse proxy
  - terraform
date: 2024-12-30
published: true
---

# Caddy as a reverse proxy in a podman rootless setup

I host my own server on a cloud. I pay attention to the softwares I run and to their security.

Also, I recently begun rewriting my personal website (to spare a little on my web hosting and to experiment with recent frameworks). I was totally unsatisfied with analytics: on one side you have privacy invasive solutions, requiring an extra consent on your site; on the other, the requirements to host a open source, GDPR compliant solution were too high/expensive.

So I wrote a GDPR compliant, open source, lightweight, web analytics software.

# GDPR compliant

The EU says you need consent to collect your users data. This is a privacy directive, and several others exist across the globe. My bet is that they will become ubiquitous over time, so better be prepared.

My website does not want to collect an individual data. I just want to know ho wmuch it is popular and who's browsing it. I'm not interested in IP addresses neither, or knowing which other sites you are visiting before mine. No fingerprinting, no advertising.

In this scenario, I could have chosen plausible analytics. But it's expensive and it has quite heavy requirements in terms of infrastructure (the UI, and all those dashboards require a fair amount of resources). Let's be honest: given my habits, I don't need a UI.

## Infrastructure

[https://link.excalidraw.com/readonly/IY7zsvJkRomHQlPXUZFE](https://link.excalidraw.com/readonly/IY7zsvJkRomHQlPXUZFE)

## A service in my podman host

So, in the days of ChatGPT and Copilot, an MVP was ready in the matter of hours. But not everything was working as expected, since the proxy was replacing the client IP address with the podman daemon IP address (10.89.x.y). Also, I was computing the wrong schema for the realtive URIs: http instead of https.

In my intended infrastructure, a single reverse proxy serves multiple services (say CDN, analytics, other). The reverse proxy choice was made several months in the past, and I was satisfied with it. Long story short, after having tried traefik and discarded the option to move to a rootful podman, I went the "caddy beta"route.

Caddy supports these features in rootless podman thanks to socket activation (a systemd feature) but version 2.9.0 is required (still a beta at the time of writing).

## Caddy configuration

Erik Sjolund did a great work documenting [Caddy setup with socket activation](https://github.com/eriksjolund/podman-caddy-socket-activation). But this was incomplete: there was no hint about the versions used (systemd, podman). And systemd is still relatively new to me, so it was not clear how to create a `service`.

The trial and error took a couple of days, but at last I had a working configuration (I'll spare you the details, but essentially on some podman/systemd versions/configurations, the caddy container was unable to solve the acme challenge or reach the analytics container, and the analytics container was unable to resolve DNS names after a restart of the caddy socket).

# GitHub repository - hands on

The [nillebco/analytics](https://github.com/nillebco/analytics) service provides a sample configuration. This is not perfect, in the sense that you still have some manual operation beyond the `./cli deploy`, but I'll be polishing this.
