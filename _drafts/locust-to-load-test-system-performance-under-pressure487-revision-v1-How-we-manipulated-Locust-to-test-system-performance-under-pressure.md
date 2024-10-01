---
id: 678
title: 'How we manipulated Locust to test system performance under pressure'
date: '2022-10-28T13:21:33+11:00'
author: 'Jen Cuthbert'
layout: revision
guid: 'https://narf.jencuthbert.com/?p=678'
permalink: '/?p=678'
---

*I wrote this article for the [Learnosity blog, where it originally appeared](https://learnosity.com/how-we-manipulated-locust-to-test-system-performance-under-pressure/). I repost it here, with permission, for archival*. *With thanks to [Micheál Heffernan](https://learnosity.com/author/micheal-heffernan/) for countless editing passes.*

The dramatic increase in Learnosity users during the back-to-school period each year challenges our engineering teams to find new approaches to ensuring rock-solid reliability at all times.

Stability is a core part of Learnosity’s offering. Prior to back-to-school (known as “BTS” internally) we load-test our system to handle a 5x to 10x increase on current usage. That might sound excessive, but it accounts for the surge of first-time users that new customers bring to the fold as well as the additional users that existing customers bring.

Since the BTS traffic spike occurs from mid-August to mid-October, we start preparing in March. We test our infrastructure and apps to find and remove any bottlenecks.

<figure class="wp-block-image size-large">![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2020/04/bts2018vs2019_nonumbers-1024x201.jpg)</figure>Last year, a larger client ramped up their testing. This created a 3x usage increase of our [Events API](https://reference.learnosity.com/events-api/). In the process, several of our monitoring thresholds were breached and the [message delivery latency](https://www.sciencedirect.com/topics/computer-science/message-latency) increased to an unacceptable level.

As a result, we poured resources into testing and ensuring our system was stable even under exceptional stress. To detail the process, I’ve broken the post into two parts:

1. Creating the load with Locust (this piece)
2. Running the load test (in part two, coming soon).

## **TL;DR**

Here’s a snapshot of what I cover in this post:

- Our *target metrics*.
- How we wrote a [Locust](https://locust.io/) script to *generate load for a Publish/Subscribe system*.
- Our observations that:
    - The load test must reflect *real user behaviours and interactions*
    - Load testing alone *doesn’t validate system behaviour against target metrics*. It’s better to measure this separately while the system is under load.

## **A bit about our system and success metrics**

For context, our Events API relies on an internal message-passing system that receives Events from publishers and distributes them to subscribers. We call it the Event bus.

This API is at the core of our [Live Progress Report](https://reference.learnosity.com/reports-api/reporttypes#liveActivityStatusByUser), which enables proctors to follow and control test sessions for multiple learners at once. Clients (both proctors and learners) publish and subscribe to topics identified by IDs matched to the learners’ sessions.

There are two streams, one for messages in each direction:

1. Logging, from many learners to one proctor
2. Control, from one proctor to each learner

The Event bus terminates a subscriber’s connection whenever messages matching the subscription are delivered or after 25 seconds have passed. As soon as one connection is terminated, the client establishes a new one. Where there are backend errors, clients will wait before trying to reconnect so as not to create cascading failures.

Because proctors need to follow learners closely as they take a test, the event delivery has to be snappy. This informs our criteria for load test success or failure:

- We want to deliver 95% of messages in 2 seconds or less
- Messages should only be delivered once per subscriber
- Any messages that take over 15 seconds to deliver are considered lost

Keeping these targets in mind, here’s how we load tested our Event bus.

## **Loading the system**

*Note: The code below has been edited for brevity and is meant to illustrate the ideas of this post, not to run out of the box.*

### **Applying the load with Locust**

Locust is an open-source load testing tool that gauges the number of concurrent users a system can handle. Testers can write simple behaviours using Python before using Locust to simulate user “swarms”.

Locusts in the swarm have one or more behaviours (`TaskSets`) attached to them. They randomly choose one at a time, according to the different weights associated to each. For example, a login page might be given less weight than a popular forum thread due to the volume of visits they receive.

Though it works well for simple user-website loads, it doesn’t reflect the more sophisticated interactions between our Events API users and Event bus. Both user types, proctors and students, use the Events API but their publish and subscribe rates vary:

- Learners publish to a topic with their own session ID at short intervals and subscribe to the same topic for instructions from the proctor.
- Proctors subscribe to as many topics as monitored learners (their session ID), and occasionally publish one or more control messages to some students.

This highlights one of the big differences between Learnosity’s use case and a simple website test: we need publishers and subscribers interacting with the same topic at roughly the same time.

We also need our tasks to establish two connections in parallel: the long-running subscribe polls, and the short-lived publishes. Finally, we need to work out realistic values for the various time intervals.

### **Getting locusts to behave**

Given the state we needed to maintain during both learner and proctor sessions, we opted for single-task behaviours where a learner runs through a set number of [Items](https://help.learnosity.com/hc/en-us/articles/360000754838-Glossary-of-Learnosity-and-Industry-terms#lrn_i) before finishing their assessment while a proctor subscribes to a set number of learners and waits until they have finished before terminating.

Both our `StudentBehaviour` and `ProctorBehaviour` objects inherit from a `EventsApiBehaviour` class derived from locusts’ `TaskSet`. They are both defined and used in the same test script.

```
# We use this global as an easily-locatable place where we can configure this loadtest
SETTINGS = {}

class EventsApiBehaviour(Locust.TaskSet):
    '''Shared behaviour authenticating to Events API.'''
    def _publish(self, user_id, events, stream):
        '''Publish a list of events to stream as user_id'''
        pass

    def _subscribe(self, user_id, event_types, position, stream):
        '''Subscribe to a list of event_types as user_id from stream, starting at position; returns the next position and a list of events received'''
        pass

    def _post(self, endpoint, data):
        '''POST payload to the given URL, retrying on server errors'''
        retry = True
        while retry and not self.stop:
            res = self.client.post(endpoint, data=data)
            if res.status_code < 500:
               retry = False
        res.raise_for_status()
        return res

    def _make_event(self, payload):
        '''Build a full xAPI message for the payload'''
        pass

    # Request-signing and other security-related parameters omitted for brevity.
    ...


class StudentBehaviour(EventsApiBehaviour):
    '''The behaviour for a student publishing events.'''
    @Locust.Task()
    def do_assessment(self):
        '''For each item in the assessment, submit an event, then wait a random amount of time'''
        self.id = self.get_id()
        self._prepare()
        self.stop = False
        for i in range(0, SETTINGS['assessment']['num_items']):
            if self.stop:
                break
            events = [ self._make_event({'action': 'progressed'}) ]
            self._publish(self.id, events, 'logging')
            self._random_wait()

        # Send a finish event
        events = [ self._make_event({'action': 'submitted'}) ]
        self._publish(self.id, events)
        self._done()


class ProctorBehaviour(EventsApiBehaviour):
    '''The behaviour for a proctor subscribing to events.'''
    @Locust.Task()
    def subscribe_to_students(self):
        position = 0
        self.student_ids = self.get_student_ids()
        self.stop = False
        while not self.stop:
            event_types = [ { 'id': id, 'type': 'logging' for id in self.student_ids } ]
            position, events = self._subscribe(self.id, event_types, position, 'logging')
            for event in events:
                if event.action === 'submitted':
                    # It is easier to finish listening on the first submission, and other new Proctors will be spawned instead to continue loading
                    self.stop = True
                    break
```

This lets us give tasks different weights so that more locusts are created with the `StudentBehaviour` `TaskSet` than with the `ProctorBehaviour`.

```
class StudentUser(Locust.HttpLocust):
    host = SETTINGS['hosts']['eventbus']  # overridden by --host option
    weight = SETTINGS['users']['students_per_proctor']
    task_set = StudentBehaviour


class ProctorUser(Locust.HttpLocust):
    host = SETTINGS['hosts']['eventbus']
    weight = 1
    task_set = ProctorBehaviour
```

Though the script above creates a substantial load, it doesn’t reflect what we see from real clients.

- For one thing, the load test spirals out of control as soon as the system is overloaded: publications and subscriptions fail and retry immediately, which puts an unrealistic load on the system.
- Additionally, learners should also subscribe to control commands from proctors.
- Furthermore, stopping the load test doesn’t stop the locusts from continuing to load the system.

### **Modifying the load to match real-life use**

To meet the characteristics of real client traffic, we needed to find a way to replicate these behaviours. So we made a few refinements.

#### **Refinement #1: Retry with backoff on error**

When applying too much load, the naive retry mechanism in `EventsApiBehaviour._post` creates a thundering herd: connections are recreated immediately on failure and the server cannot recover from a transient overload.

This is a good example of the degree of realism that a load test needs to have. In this case, it’s just a matter of implementing the same backoff strategy the Events API already has.

```
class EventsApiBehaviour(Locust.TaskSet):
    ...
    def _post_with_backoff(self, endpoint, data):
        '''POST payload to the given URL, retrying on server errors, with exponential backoff'''
        for retry in range(self.RETRY_MAX):
            if self.stop:
                break
            res = self.client.post(endpoint, data=data)
            if res.status_code < 500:
                # successful request
                res.raise_for_status()
                return res
            
            # wait before retrying
            backoff = (2**retry * self.RETRY_TIME)  # an improvement would be to pick a random delay between 0 and this value
            gevent.sleep(backoff  / 1000.)

        # still failing after RETRY_MAX attempts, giving up
        res.raise_for_status()
        return res
```

#### **Refinement #2: Subscribe students to the control stream**

The loop for learners is pretty simple: send an event, then wait.

To reflect real-life use cases though, learners should also wait for commands from the proctor. This is important because it creates lots more connections to the system. Even though inactive, these connections still use server resources.

Fortunately, Locust plays well with [`gevent`](http://www.gevent.org/), which lets us run functions and handle the subscription in parallel with little fuss, while the main loop continues to publish new events.

```
import gevent
...
class StudentBehaviour(EventsApiBehaviour):
    ....
    def _subscribe_to_control(self):
        position = 0
        self.student_ids = self.get_student_ids()
        self.stop = False
        while not self.stop:
            event_type = [ { 'id': self.id, 'type': 'control' } ]
            position, events = self._subscribe(self.id, event_type, position, 'control')
     def _prepare(self):        '''Executed before starting the assessment loop'''
        self._subscribe_thread = gevent.spawn(self._subscribe_to_control)

    def _randow_wait(self):        '''Simulate a student's think time: wait a bit between sending events'''
        gevent.sleep(random.randint(
                SETTINGS['assessment']['think_time_min'],
                SETTINGS['assessment']['think_time_max']))

    def _cleanup(self):        '''Clean up resources at the end of an assessment''
        self._subscribe_thread.kill()
```

#### **Refinement #3: Terminate cleanly for clients**

One remaining issue was that terminating the load test from the Locust interface would result in clients running through the loop of their own `TaskSet`.

To avoid this we needed to inform the `TaskSet` to immediately terminate client loops, ignoring the rest of the assessment and cancelling retries. Fortunately, the loops discussed above are conditioned on `self.stop` not being `True`. Locust provides the missing piece in the form of the `on_stop` method, which it calls on all the running `TaskSets` when terminating.

```
class EventsApiBehaviour(Locust.TaskSet):
    ...
    def on_stop(self):
        self.stop = True
```

### **Behaviour checking**

What’s described above gives us a realistic load test that we can start and stop at will – but that’s just part of the job. The next step is verifying that the system performs as we want it to under this load.

<figure class="wp-block-image size-large">![](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2020/04/Screen-Shot-2019-08-07-at-16.07.28-1024x230.png)</figure>While Locust can provide some statistics about successful and failed connections, it doesn’t capture the data that’s most relevant to our targets such as lost and duplicate messages or long delivery delays between publishers and subscribers. To fix this we wrote a separate application that sends and receives messages to collect those metrics during load-testing.

An important additional task at this point is to keep an eye on the health of the underlying system. To make sure everything was operating smoothly we ran checks to see if the nodes running the Event bus were under too much stress (from CPU load, memory pressure, connection numbers, etc.). We also tracked logs from the system, web server, and Event bus to identify the root causes of any issues we spotted.

## **Flexibility is often a state of mind (and expertise)**

Locust is a powerful tool for single-user website load tests that also lends itself well to more complex load-testing scenarios – provided you bring in-depth knowledge of what system behaviours you’re looking to test and what kind of traffic your system receives.

To mimic the user behaviour patterns we experience at Learnosity, we had to go well beyond the basic script used in more straightforward load tests.

This isn’t a challenge anyone should take lightly.

Prior to running the load test for real, we went through multiple rounds of trial and error in developing a sufficiently realistic script. The code presented above represents only the end result; it doesn’t reflect the amount of time and effort it took to build it up – either for the basic behaviour or the subsequent refinements.

Our efforts in ensuring reliability at scale might not be glamorous, but they’re worth sharing. Reflecting on our process helps us refine it, while documenting the experience may help other engineering teams facing a similar challenge.

*In [part two of this series, I’ll look at the (slightly nerve-shredding) next step in the process: running the tests.](https://blog.narf.ssji.net/2021/05/scaling-in-the-time-of-covid-how-we-run-load-tests-at-learnosity/ "Scaling in the time of COVID: How we run load tests at Learnosity")*