---
id: 535
title: 'Scaling in the time of COVID: How we run load tests at Learnosity'
date: '2021-05-11T10:13:15+10:00'
author: 'Olivier Mehani'
excerpt: "tl;dr: (1) We used Locust to create the load, and a custom application to verify correct behaviour.\n(2) We found a number of configuration-level issues, mainly around limits on file descriptors and open connections.\n(3) Stuff we learned along the way: record all parameters and their values, change one at a time; be conscious of system limits, particularly on the allowed number of open files and sockets"
layout: post
guid: 'https://blog.narf.ssji.net/?p=535'
permalink: /2021/05/11/scaling-in-the-time-of-covid-how-we-run-load-tests-at-learnosity/
iawp_total_views:
    - '1'
image: /wp-content/uploads/sites/3/2021/05/image11-1024x696-1.jpg
categories:
    - code
    - engineering
    - Learnosity
    - sysadmin
tags:
    - Linux
    - load-testing
    - Locust
    - nginx
    - systemd
---

*I wrote this article for the [Learnosity blog, where it originally appeared](https://learnosity.com/scaling-in-the-time-of-covid-how-we-run-load-tests-at-learnosity/). I repost it here, with permission, for archival*. *With thanks, again, to [Micheál Heffernan](https://learnosity.com/author/micheal-heffernan/) for countless editing passes.*

In this series, I look at how we load test our platform to ensure platform stability during periods of heavy user traffic. For Learnosity, that’s typically during the back-to-school period. The year was different though, as COVID caused a dramatic global pivot to online assessment in education. Here is what the result of that looked like in terms of traffic.

<div class="wp-block-image"><figure class="aligncenter size-large is-resized">[![Weekly Learnosity users comparison 2012--2020](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2021/05/Learnosity-BTS-2020-users-1024x633-1.jpg)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2021/05/Learnosity-BTS-2020-users-1024x633-1.jpg)</figure></div>We expect major growth every year but that kind of hockey stick curve is not something you can easily predict. *But,* because scalability is one of the cornerstones of our product offering, we were well-equipped to handle it.

This article series reveals how we prepared for that.

In [part one](https://blog.narf.ssji.net/2020/04/locust-to-load-test-system-performance-under-pressure/ "How we manipulated Locust to test system performance under pressure") (which was, incidentally, pre-COVID), I detailed how we actually created the load by writing a script using [Locust](https://locust.io). In this post, I’ll go through the process of running the load test. I’ll also look at some system bottlenecks it helped us find.

Let’s kick things off by looking at some important things a good load-testing method should do. Namely, it should

1. Apply a **realistic load**, starting from known-supported levels.
2. Determine whether the **behaviour under load matches the requirements**. 
    - If the **behaviour is not as desired**, you need to identify errors and fix them. These could be in 
        - the load-test code (not realistic enough)
        - the load-test environment (unable to generate enough load)
        - the system parameters
        - the application code
    - If the **behaviour is as desired**, then ramp up the load exponentially.

We used two separate tools for steps 1 above (as [described in the first part](https://blog.narf.ssji.net/2020/04/locust-to-load-test-system-performance-under-pressure/ "How we manipulated Locust to test system performance under pressure") of this series) and tracked the outcomes of step 2 in a spreadsheet.

### **TL;DR**

- We [used Locust to create the load](https://blog.narf.ssji.net/2020/04/locust-to-load-test-system-performance-under-pressure/ "How we manipulated Locust to test system performance under pressure"), and a custom application to verify correct behaviour.
- We found a number of configuration-level issues, mainly around limits on file descriptors and open connections.
- Stuff we learned along the way: 
    - Record all parameters and their values, change one at a time;
    - Be conscious of system limits, particularly on the allowed number of open files and sockets.

### **Running load tests and collecting data**

It’s crucially important to keep good records when corralling data from the thundering herd into useful information.

There are essentially two classes of data to keep track of here.

1. **static parameters**, which describe all the relevant configurations of the system under load and;
2. **dynamic behaviour**, which is any relevant metrics collected during the load test.

Those two sets tend to grow over the duration of the load-test campaign, as more relevant parameters, and more performance metrics are identified.

#### **Static parameters**

Static parameters are under our direct control and we can change them in different runs. Those include environment and instance sizes – which also includes a growing number of configuration options that are discovered through successive rounds of load tests. The numbers driving the load generation are also important here.

<figure class="wp-block-image size-large">[![Static parameters](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2021/05/Screen-Shot-2020-11-02-at-15.18.381-1024x544-1.jpg)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2021/05/Screen-Shot-2020-11-02-at-15.18.381-1024x544-1.jpg)</figure>#### Dynamic behaviour

The dynamic behaviour metrics are things we can observe as the load test runs.

This category covers both intrinsic performance metrics of the hosts, such as CPU load or memory used, as well as the actual target metrics that allow us to call whether a load test run was successful or not.

Colour-coding helps in making the data more legible. As I mentioned before, there can be different types of failure, either of the system under load or of the load-testing system itself. Since we have two different components in our load test, we have a number of different colours for failures of the different components. Observations made during the run are important too, as they are generally a good indicator of what to do next.

<figure class="wp-block-image size-large">[![Dynamic parameters](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2021/05/image51-1024x503-1.jpg)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2021/05/image51-1024x503-1.jpg)</figure>We also have some automatic data reporting in place for the correctness test application.

It generates a simple CSV output, which can easily be imported into the same spreadsheet for each run. This allows us to quickly get an idea of how well the system performed in terms of the target criteria (in this case, the end-to-end delay) by calculating and plotting some summary statistics.

<figure class="wp-block-image size-large">[![Target metrics](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2021/05/image11-1024x696-1.jpg)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2021/05/image11-1024x696-1.jpg)</figure>At this stage, load testing becomes a relatively simple process, driven by the data-collection spreadsheet:

1. Run a load test with the current parameters
2. If the outcome is: 
    - a failure: understand and fix the cause of failure, or
    - a success: increase the parameters defining the load.

When updating the parameters to generate more load. It’s generally better to change one parameter at a time so you can more easily track down issues and create a fuller matrix of the combination of parameters.

Unless you have a clear number available, it’s good practice to double the previous value as it lets you exponentially explore the space (and hit a bottleneck faster), even if you’ve started with reasonably low values.

### **Configuration bottlenecks**

The load-test setup described above helped us identify a number of bottlenecks in our environment. Those bottlenecks were also often present in the load-generating infrastructure, so we had to run most tests twice before we could increase the load and hit a new bottleneck.

We found that at every level of the stack, the defaults were too low. Sometimes, parameters that remained in our configuration management system from legacy deployments were set incorrectly.

It is interesting to note that there are quite a few parameters that control the number of connections that can be successfully established to the app. We decided to create a funnel so the kernel limits would be the lowest. Any connection that managed to make it through those would be virtually guaranteed to make it all the way to the application and be serviced.

#### **System-wide limits**

First, we disabled an ancient entry that set the [`fs.filemax`](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/fs.html?highlight=file-max#file-max-file-nr) sysctl to 20,480. This dated from age-old deployments where we were actually increasing the default limit. It is now automatically calculated based on the memory of the host, and our hard-coded value is now set lower to the automatic default value (in one random check I just did, it was at 395,576, one order of magnitude higher). This otherwise led to errors from various components of the system.

```
Too many open files in system
```

#### **Per-process limits**

Next was the configuration of nginx, which proxies public requests to our app. After a while, it complained that:

```
[alert] 3122#0: *1520270 2048 worker_connections are not enough while connecting to upstream, client: 192.2.0.2, server: eventbus.loadtest.learnosity.com, request: "POST /latest/publish HTTP/1.1", upstream: "http://127.0.0.1:9092/latest/publish", host: "eventbus.loadtest.learnosity.com"
```

This was simply fixed by adjusting this parameter in the `nginx.conf` file.

```
worker_connections 32000;
```

Which led to the obvious next error

```
[alert] 25367#0: *5200246 socket() failed (24: Too many open files), client: 192.2.0.2, server: eventbus.loadtest.learnosity.com, request: "POST /latest/publish HTTP/1.1", upstream: http://127.0.0.1:9092/latest/publish", host: "eventbus.loadtest.learnosity.com"
```

Our default systemd configuration sets the limit of the maximum number of files the process can have open to 2048. We installed a manual override in` /etc/systemd/system/nginx.service.d/nofile.conf`, so as not to manual change system files.

```
[Service]
LimitNOFILE=65536
```

Note that the number of allowed open files is around twice that of `worker_connections`. This is because each accepted connection will lead the worker to establish a second connection to the backend, which also needs to be accounted for.

Once nginx was happy, we hit the same problem one level deeper, from our [Golang http](https://golang.org/pkg/net/http/)-based app.

```
http: Accept error: accept tcp [::]:9092: accept4: too many open files; retrying in 5ms
```

The fix was the same, by adding a manual override to the systemd service for our Event bus.

```
[Service]
LimitNOFILE=32768
```

#### **Network tuning**

Along the way, we found a few other occasional errors. Most revolved around TCP connections not being cleared up fast enough. We already had some configuration in place (prior to the load test) to maximise the amount of allowed connections and limit their lingering after closure

```
net.core.somaxconn = 63536
net.ipv4.tcp_fin_timeout = 15
```

We tweaked a couple more to expand the range of ports that could be used for outgoing connections (from nginx to the app), as well as allow the reuse of existing TCP sockets in the `TIME_WAIT` state.

```
net.ipv4.ip_local_port_range = 1024 65535
net.ipv4.tcp_tw_reuse = 1
```

We also had to adjust some firewall settings. We had kernel connection tracking enabled by default. This created issues when the table got full, trying to keep track of too many connections.

```
nf_conntrack: table full, dropping packet
```

We first thought about tweaking timeouts (`net.netfilter.nf_conntrack_tcp_timeout_fin_wait` and `net.netfilter.nf_conntrack_tcp_timeout_time_wait`) so the table entries would clear faster. However, we realised that connection tracking made little sense on a worker node. Simply disabling it in firewalld (with `--notrack`) in rules for connections to the backend app fixed that issue.

With all these changes, our Event bus was finally constrained only by the performance of the machines! We ran some dimensioning experiments to evaluate the impact of vertical (instance size) and horizontal (instance number) scaling, so we could make informed decisions on this final bit of system configuration for production.

### Know thyself—understand your tech stack

We’re at a time when hundreds of clients are relying on our infrastructure to perform with total reliability as millions of learners make the switch to digital assessments.

Had we doubled—or even tripled—the maximum traffic load capacity of what we saw in 2019, we would have come unstuck because of the unforeseen impact of COVID. But we always aim to stretch out our capacity by way more than that.

Due to the publish/subscribe nature of the Event bus application, we had to write a more complex Locust script than usual, keeping some state between publishers and subscribers. We also had to write a separate application to measure the message-delivery times, which were our target pass/fail metric.

Thanks to careful bookkeeping of all the parameters and results, we identified weak points in our system and optimised them. Note that most of the issues came from misconfigurations of the system, and that we did not even get into the application code.

This is an important reminder that a successful load-testing campaign requires a good understanding of the entire tech stack under consideration.

After further load tests, we were confident that the event-passing system would be able to sustain at least seven times the maximum load we’d previously seen. That put our system in good stead to withstand the shock waves of even the most challenging circumstances.