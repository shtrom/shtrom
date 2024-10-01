---
id: 984
title: 'Shell work history'
date: '2023-09-12T00:11:27+10:00'
author: 'Olivier Mehani'
excerpt: ' I was wondering what my most-used shell commands are. It''s an easy few commands to pipe:  `history | sed ''s/^ *//;s/ \+/ /g'' | cut -d'' '' -f 2 | sort | uniq -c | sort -n | tail -n 20`'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=984'
permalink: '/?p=984'
---

As idle musing, and a way to show off my mastery of shell pipelines, I was wondering what my most-used shell commands are. It’s an easy few commands to pipe.

```
history | sed 's/^ *//;s/ \+/ /g' | cut -d' ' -f 2 | sort | uniq -c | sort -n | tail -n 20
```

The outcome is rather expected. I feel validated (by my shell) in my own self-perception!

<figure class="wp-block-image size-full">![Screenshot of a terminal showing oft-used commands](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/09/Screenshot-from-2023-09-11-23-54-20.png)</figure>As for a less cryptic unpicking,

```
history             # get the shell's history, as lines of the form '  <nnn>  <command> <arguments>'
  | sed 's/^ *//;   # trim leading spaces
         s/ \+/ /g' # replace multiple spaces with a single one, for all occurrences
  | cut -d' ' -f 2  # cut the line at every single space, and retain the second field (the <command>)
  | sort            # sort the output, as needed by uniq
  | uniq -c         # remove duplicates, but retain a count, as line of the form '<count> <string>'
  | sort -n         # sort the output 
  | tail -n 20      # keep the last 20 lines
```

Notes:

- Due to the lack of line continuations, this commented command is not functional as is.
- This works with the [GNU coreutils](https://www.gnu.org/software/coreutils/coreutils.html) on Linux. Other Unices may exhibit slightly different behaviours and/or require the use of `g`-prefixes commands (e.g., `gsed`) to use the Coreutils implementation (if installed).