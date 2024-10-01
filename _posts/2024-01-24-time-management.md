---
id: 1162
title: 'Time Management'
date: '2024-01-24T23:54:58+11:00'
author: 'Olivier Mehani'
excerpt: "I have evolved a system to plan my time, and schedule work days, based on task priority and importance.\n\nIt is a spreadsheet, where I classify task urgency and worth using an Eisenhower matrix;\nI then plan days and commit to tasks in 1-hour blocks (à la Deep Work)."
layout: post
guid: 'https://blog.narf.ssji.net/?p=1162'
permalink: /2024/01/24/time-management/
yarpp_meta:
    - 'a:1:{s:27:"yarpp_display_for_this_post";i:1;}'
iawp_total_views:
    - '6'
image: /wp-content/uploads/sites/3/2024/01/Screenshot-2024-01-05-at-11.45.49-scaled.png
categories:
    - engineering
    - tip
tags:
    - 'deep work'
    - 'eisenhower matrix'
    - 'time management'
---

As I progress in my career, I find my time to be more and more parcelled out due to many external requests, or internal whims. Over the last few years, I have cobbled together a system that allows me to plan time for tasks based on their priority and importance, and keep me honest applying my time where it matters.

At its core, it follows [Cal Newport’s Rule # 4 of Deep Work](https://calnewport.com/deep-work-rules-for-focused-success-in-a-distracted-world/).

> At the beginning of each workday, \[…\] Divide the hours of your workday into *blocks* and assign activities to the blocks. \[…\] When you’re done scheduling your day, every minute should be part of a block. You have, in effect, given every minute of your workday a job. Now as you go through your day, use this schedule to guide you.
> 
> <cite>Cal Newport, “Deep Work”, Rule # 4</cite>

tl;dr:

- It is simply based around a spreadsheet, where
- I classify sprintly task priorities and urgency using an [Eisenhower matrix](https://jamesclear.com/eisenhower-box),
- I plan a few days ahead by placing tasks in 1-hour blocks,
- I commit to the day’s plan in the morning, and record actual work; and
- Comparing commitment to actual work allows me to collect some metrics.

## Planning for the day

A few years back, when I was still in academia, a friend—we’ll call him Ralph, because that’s what his name is—introduced me to the ideas in [Cal Newport’s *Deep Work*](https://calnewport.com/deep-work-rules-for-focused-success-in-a-distracted-world/). He was using a simple approach based on a spreadsheet where he would simply plan the day ahead in one column, and record what he did against the plan throughout the day. Using a spreadsheet has the advantage of being quite frictionless, as editing a cell takes no time at all. This also makes the system quite flexible and extensible.

I have been reluctant, for years after being introduced to the idea, to do any fine planning of the day. I had been using [Bullet Journaling](https://www.lostbookofsales.com/why-to-do-lists-often-stink-and-how-do-the-truly-successful-people-maintain-their-productivity/) to loosely record objectives for, and actions of, the day, but I felt like anything more would be too constraining and prevent me from doing what I felt like doing. It took me a while to realise that preventing me from doing what I felt like was exactly the purpose of an effective planning system. As demands for my time became more numerous, I eventually decided to give the idea a go. I finally read Cal Newport’s book, and picked up where the conversation had left off: a spreadsheet with two columns.

<figure class="wp-block-image size-large">![A spreadsheet showing 8 days. There are two columns per day, and one row per hour. The cells are coloured: green when both cells match, orange when there is a partial match, or red when the cells are completely different. Meetings are highlighted in blue.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-2024-01-05-at-10.59.09-1024x419.png)</figure>
The left column gets filled before the start of the day. It’s the commitment. The right columns gets filled as the day goes. I recalled Ralph also mentioned some light colour-coding of the cells, so he could identify where he was sticking to his commitments, and where he was slipping. I thought this was a good idea, so I adopted and improved on the idea. Beyond simple string matching, that bestows a green tinge to the row (e.g., most of the “split-js” in this example), an unmatched commitment is coloured red (“TAMUC # 4” was not in favour on Monday # 1), while a partial match will be orange (“AWS step functions” on Thursday # 1), as will a delayed task (“reviews” on Thursday # 2). The blue colour was added later, to keep track of meetings. All this is achieved with conditional formatting, and a number of hidden formulas under the main table, providing TRUE/FALSE states for each of the cells.

## Numbers and metrics

Another advantage of the boolean state cells is that they can be counted. This doubles as a poor person’s proxy to metrics. As each row counts for an hour, and there are two columns per row, I arbitrarily count each cell as contributing half an of the block’s colour, that is, half an hour. Meetings are counted differently: only the actual meetings (right column) count as the whole. While not exactly precise, this counting method has the advantage of being simple, and sufficiently accurate to be useful. Moreover, beyond retrospective metrics, I can now gamify work!

<figure class="wp-block-gallery has-nested-images columns-default is-cropped wp-block-gallery-11 is-layout-flex wp-block-gallery-is-layout-flex"><figure class="wp-block-image size-large">![Barchart summaries of work time spent of 2023](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-2024-01-05-at-11.45.49-1024x570.png)</figure></figure>## Canvassing the next few days

The approach above is good for day-to-day planning. However, in the course of weeks, sprints, and months of work, different priorities compete, and tasks of different urgency need to be juggled. This is where the [Eisenhower matrix](https://jamesclear.com/eisenhower-box) comes into play.

Attributed to the 34th President of the USA, this method classifies tasks across two axes: priority and urgency. This creates four quadrants, each with a different handling rule:

- high importance / high urgency: do now
- high importance / low urgency: plan to do later
- low importance / high urgency: delegate
- low importance / low urgency: forget about it

I extended my spreadsheet with a makeshift matrix, with a few rows and columns in each quadrant. At first, I was just throwing tasks anywhere in the quadrant I thought they belonged in, but this felt very arbitrary, and subject to my human passions. As a way to address the issue, I labelled each row and column with more precise classes: importance from nice-to-haves to release-blockers, and urgency from years to hours.

<figure class="wp-block-image size-large">![An Eisenhower matrix implemented in a spreadsheet. Each quadrant is made of 10 rows and 3 columns. Rows are labelled by urgency: year, half-year, quarter, month, sprint, week, half-week, day, half-day and hour. Columns are labelled by importance: nice to have, code improvement, tool improvement, process improvement/education, people blocker, client/release blocker](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-2024-01-23-at-09.38.51-1024x764.png)</figure>Every sprint, I duplicate the previous sheet, clear the daily rows, and update the matrix according to how things have evolved. I often choose areas of focus at the start, and bold them as a reminder. Throughout the sprint, new tasks tend to pop up. They get weighed up with the matrix, and planned accordingly. I try to schedule important / urgent tasks in multi-hour blocks in the afternoons, while important but non-urgent tasks are fit in morning holes in the future days. I try as best as I can not to have unimportant tasks, but allow a few feel-good ones to sneak in occasionally. A release-day blocker, and other similar very top-left tasks coming in are allowed to disrupt the day, and override any commitment (but will still be colour-coded red).

## Does it work?

I started using this technique in the last 3–4 months of 2021, and it is now early 2024. I have a bit more than 2 years of metrics to look at. It’s not very clear cut, but there seems to be a trend towards more work done on schedule, mainly taking over out-of-schedule work, even if unscheduled work represents an apparently consistent 25% of my time.

<figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2024/01/Screenshot-2024-01-23-at-09.49.25-1024x631.png)</figure>
From a more qualitative perspective, though, I have found that I derive some validating satisfaction from doing what I had planned to do when I had planned to do it. The separation of planning—sometimes days or weeks earlier—, daily commitment, and actually doing the work provides an interesting reinforcement, particularly for the least appealing tasks. It’s easier to convince myself to do them, by remembering that I have already scheduled and committed to do them *now*. So it’s too late to backtrack. Conversely, it also provides the permission to stop working on something when the time block has elapsed, as well as the framework to decide when to pick up the task again, thus providing the reassurance that it is going to get worked on again.

All in all, I find it a beneficial approach, both qualitatively and quantitatively. Now, I need to continue improving my discipline to reduce the orange bars. The hardest will be reducing the red bars, as they tend to be caused by impromptu interruptions and meetings outside of my direct control.