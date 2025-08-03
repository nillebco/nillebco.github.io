---
tags:
  - containers
  - docker alternatives
date: 2025-01-02
published: true
---

# colima:  a lightweight docker replacement

[https://github.com/abiosoft/colima](https://github.com/abiosoft/colima)

I was unable to run a x86 container on my M1 with rancher desktop, so I decided to give a try to [colima](https://github.com/abiosoft/colima). Is this name somewhat related to the cold SIberian wind?

My needs:

- lightweight (an M1 in 2025 is not anymore "top of the market")
- execute x86 and arm containers
- build docker images for ARM
- (optional) kubernetes support
- good command line support (ie. show progress in the terminal, connect to the VM using a shell)
    - good docker compatibility (the majority of the documentation is oriented to Docker and often I encounter border-line incompatibility issues; great for experience, less for fun 🙂)

After a quick and seamless installation that took less than a minute

```shell
brew install colima
brew install docker
```

A first good surprise was that it listens on its own IP address:

```shell
❯ colima status
INFO[0000] colima is running using macOS Virtualization.Framework 
INFO[0000] arch: aarch64                                
INFO[0000] runtime: docker                              
INFO[0000] mountType: sshfs                             
INFO[0000] address: 192.168.64.14                       
INFO[0000] socket: unix:///Users/nilleb/.colima/default/docker.sock 

```

This clearly identifies the host running the docker images, so I kinda love it. If ever you'd like to reach the host from within a container, colima supports the `docker` standard `host.docker.internal`.

The command `docker build` is now deprecated, so it could be worth following the steps highlighted in the following discussion

https://github.com/abiosoft/colima/discussions/273#discussioncomment-4959736

Reported here for brevity

```shell
brew install docker-buildx
mkdir -p ~/.docker/cli-plugins
ln -sfn $(which docker-buildx) ~/.docker/cli-plugins/docker-buildx
docker buildx install 
```
