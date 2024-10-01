---
id: 922
title: 'Generative AI chatbots affect an air of authority that they do not deserve'
date: '2023-05-15T20:40:17+10:00'
author: 'Olivier Mehani'
excerpt: 'Rather than focusing only on painstakingly fixing each ML system separately, we should leverage generative AI chatbots to help training humans to recognise and critically think when dealing with any of them, fixed or not.'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=922'
permalink: '/?p=922'
---

*(The title was <s>pilfered</s>inspired from a comment by a work colleague, who agreed to be henceforth referred to as `[Your Name]`, as ChatGPT offered this placeholder for their signature.)*

Artificial Intelligence or, [more accurately](https://www.coursera.org/articles/machine-learning-vs-ai), Machine Learning is an amazing tool for sifting through large amounts of data and discovering insightful patterns. A task where a human operator would generally get bored and become sloppy — or simply die of old age in the process — can be very effectively performed by a machine, and a result returned, sometimes in a matter of seconds.

Rather than exhibit true intelligence, however, those systems only learn as much as is present in the data they are given. This is also what they regurgitate. It is no wonder that outputs from those algorithms replicate the biases present in their input data.

Much research work has gone into identifying and reducing biases in training data, or actively de-biasing responses, but the final decision of what to do with the result of an ML process is entirely in the hands of a human being operating it.

**tl;dr:** Rather than focusing solely on painstakingly fixing each ML system separately, we should also leverage generative AI chatbots to help train humans to recognise, and critically think, when dealing with any ML system, de-biased or not.

Unfortunately, much like [the vicinity of a cat](https://xkcd.com/231/), that of a computer seems to have the propensity to disengage our collective capacity for critical thinking. This has been a long time coming, from [computer saying “no”](https://www.youtube.com/watch?v=ayPD0U_FO4Y), to “the algorithm” being blamed for all sorts of unfair decisions. The problem is not so much the output of those algorithms, as the affected apathy of the humans consuming it — or applying the decisions without question.

This issue is now getting amplified with the wide accessibility of generative chat bots. They answer any question in a well-structured, and rather authoritative-sounding way. They do, too, relay biases from both the questions, and the Internet at large, the source of their “knowledge”. [They are also prone to hallucinations](https://www.theguardian.com/technology/2023/mar/17/openai-sam-altman-artificial-intelligence-warning-gpt4) ([also known as “making shit up”](https://www.abc.net.au/news/2023-03-22/google-bard-artificial-intelligence-chatbot-early-reviews/102128612)). As an attempt to fix those problems, there are plenty of warnings in ancillary materials (terms of service, UI warnings, fine print, …), and fixes are added for issues that have arisen on the most unsavoury topics.

<div class="wp-block-image"><figure class="aligncenter is-resized">![An (incorrect) statement from ChatGPT side-by-side with authoritative documentation stating the opposite.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/04/chatgpt-s3-website-oac-oai.png)<figcaption class="wp-element-caption">ChatGPT confidently saying things that aren’t true.</figcaption></figure></div>Warnings are however quickly forgotten in the face of the cogency of the bots’ arguments, or the confidence they are expressed with; and issues can only be fixed as they are discovered. A lay person having a casual conversation with one of them still risks getting fooled into believing, or acting based on, a well-put statement, no matter how incorrect or damaging.

Humans remain the enabler between an AI’s idle banter, and actions taken based on it. Recently, GPT-4 even [“lied” to a human so they would solve a CAPTCHA](https://gizmodo.com/gpt4-open-ai-chatbot-task-rabbit-chatgpt-1850227471) for it, but it may not have to do it for much longer with support for [plugins and API](https://openai.com/blog/chatgpt-plugins) that may allow to bypass the middle-human. Removing humans from the loop, [as is already experimented with](https://www.boston.com/community/tell-us/how-worried-are-you-about-the-rise-of-artificial-intelligence/) (eerily reminiscent of [entertaining but horrifying fiction](https://en.wikipedia.org/wiki/Metalhead_(Black_Mirror))), is clearly not the solution here.

Rather, [humans can be the fail-safe mechanism](https://en.wikipedia.org/wiki/1983_Soviet_nuclear_false_alarm_incident), having the last say in determining whether something is correct or not. Much like ML systems are trained on data from the outside world, though, humans must also be trained to recognise, and react appropriately, to the risks caused by ML systems. This should happen at the same scale as the availability of those ML systems.

There has already been calls for caution, or [pause, in the development](https://futureoflife.org/open-letter/pause-giant-ai-experiments/) of this type of ML tools. However, they will only be effective for those research labs and implementers who heed the warnings. With the [source code of generative chat systems already available in the wild](https://www.theverge.com/2023/3/8/23629362/meta-ai-language-model-llama-leak-online-misuse), and used in a number of apps targeting a wide ranging public ([with chilling effects](https://www.youtube.com/watch?v=xoVJKj8lcNQ)), the horse may have already bolted. Instead, compliant systems could contribute to help train humans.

A first step would be to make it clear when an ML system generated some suggestions. [Toby Walsh suggested the idea of a Turing Red Flag](https://www.cse.unsw.edu.au/~tw/wcacm15.pdf) ([comments there are also interesting](https://cacm.acm.org/magazines/2016/7/204019-turings-red-flag/fulltext)), similar to those waved, as warning to pedestrians and horsemen, in front of the first motorcars.

<figure class="wp-block-pullquote">> [Turing Red Flag law](https://www.cse.unsw.edu.au/~tw/wcacm15.pdf): An autonomous system should be designed so that it is unlikely to be mistaken for anything besides an autonomous system, and should identify itself at the start of any interaction with another agent.
> 
> <cite>Toby Walsh</cite>

</figure>Further to this, generative chat systems should drop the pretence of authority. Instead, they should remind us, *as part of the conversation*, of the fact that they are prone to hallucinations or offering really bad advice, and encourage their interlocutor to critically consider anything coming out of it. Rather than hiding this information in fine print, this would constantly reinforce the machines’ foibles, as well as allow us to develop and exercise our abilities to check and verify.

AI systems are not able to enact any of their decisions into the real world. Humans are. Yet, all of the focus has been on “fixing” each system to not make incorrect decisions. While necessary, this approach does not scale to fixing all issues in all systems. Instead, ML systems, and particularly chatbots, can contribute to helping humans remain a critical agent before believing or applying a decision. Rather than displaying an air of unquestionable authority, generative conversational AI should openly admit to their fallibility, and encourage their human interlocutors to critically consider the output from their algorithms. Those skills will be invaluable when interacting with any ML system, not limited to those following this suggestion, and indeed any other human who may not be entirely truthful or correct.

---

This post ended up a lot wordier than I initially envisioned. To lighten the tone, and as the event that sparked this post, here is a recent entertaining, albeit anecdotal, example where ChatGPT argued one thing, only to immediately demonstrate it was, in fact, not true.

It all started with a random comment I made.

> I got to say, I kinda like having actual humans involved in writing news.
> 
> <cite>Me</cite>

To which, in jest, `[Your Name]`, asked ChatGPT to convince me otherwise. It made a decent point at first, but subsequent questioning quickly revealed that its capabilities fell quite short of what it had just confidently promised.

> Write a short blurb to convince Olivier of the value of ChatGPT generated news stories
> 
> <cite>`<em>[Your Name]</em>`</cite>

And, sure enough, ChatGPT came up with a very convincing set of arguments.

> Dear Olivier,
> 
> As someone who is always on the lookout for the latest news and updates, you may want to consider ChatGPT generated news stories. These stories are generated by an AI technology that aggregates news from multiple sources, curates the most relevant information, and delivers it to you in a concise and easy-to-read format.
> 
> The great thing about ChatGPT generated news stories is that they are unbiased and factual. They do not have any political or personal agenda, thus providing you with an objective view of the world events. Additionally, they are always up-to-date, ensuring that you never miss out on any important news.
> 
> Moreover, ChatGPT generated news stories are customizable to your interests. You can select the topics that you want to follow and get news stories that are tailored to your preferences. This way, you can stay informed about the things that matter to you the most.
> 
> Overall, ChatGPT generated news stories offer a convenient and reliable way to stay informed about the latest happenings in the world. I highly recommend giving them a try.
> 
> Best regards,
> 
> `[Your Name]`
> 
> <cite>Actually ChatGPT, pretending to be `[Your Name]`</cite>

This was a fairly convincing argument. However, taking the AI up on its offer of “convenient and reliable way to stay informed about the latest happenings in the world” quickly revealed the shallowness of the computer-generated fib.

> Show me the five most popular tech news stories of the first week of April 2023 with links
> 
> <cite>`[Your Name]`</cite>

But ChatGPT had to immediately renege on its promises of “latest happenings”…

> I’m sorry, as an AI language model, I cannot provide real-time news updates or any links as of now. My database only includes information up to October 2021.
> 
> <cite>ChatGPT</cite>

… or of factuality and lack of bias …

> As an AI language model, I do not have information regarding the iPhone 14, as it is not yet announced by Apple. However, I can give you an idea of what to expect based on rumors and speculations(…)
> 
> <cite>ChatGPT, repeatedly failing to deliver on its most recent promises.</cite>