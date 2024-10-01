---
id: 741
title: 'The ultimate bash(1) startup logic'
date: '2022-11-27T15:52:59+11:00'
author: 'Olivier Mehani'
excerpt: "It's always a bit confusing to reason about which startup files `bash` is going to run in a given situation.\nSo I made a chart."
layout: revision
guid: 'https://blog.narf.ssji.net/?p=741'
permalink: '/?p=741'
---

It’s always a bit confusing to reason about which startup files `bash` is going to run in a given situation. [It is documented, but the logic is not trivial](https://www.gnu.org/software/bash/manual/bash.html#Bash-Startup-Files).

  
So I made a chart ([using PlantUML](http://www.plantuml.com/plantuml/uml/nLD1Jp8n4BttLpIJxm07Fkvu43KOJOm7JJnXDiiw2mtTpgRjWiReRvVMx12RGa8ys0Ebsvath-_DJ9qlhUyQBU8V8LGj1yfiQ5rwHKQQii6Xz2iqSW2mADqAO2Ya_0xpQClAgmsUzp5lwC9r2DZ5ZqOjEVKAa5o7DG7uzpwxV_e0E8kVK3iCQPgMoZ2WeJvX3sh8LbdCk9odbiyHbL4I75lLIYD0fXPpd7-E_uTdswhdoSkGnuaijIEv3VdAj9sNjQLcRWpwBTcrhCWOh8AKdCka01wkhc_lPW1fsVucAOdcHTKYEJ9U8eGk5wXbe5v4HJCgjfPOWDEbPAvZzDMOiNum3csorx3WeBHVyfeNEL1k54Rc9nx7JQCpg8TR8CyaEY1JHpYrSsYbG-SKcMTnW0XrFg9oUaAbjojopbgr94-fqUbhuhHTNZpU53noNB3VHT-MfmnvEgt7nplRet_QeNb_4pT_OynHMvX-wWHlOhhxwHhz1G00)!). You’re welcome.

<figure class="wp-block-image size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2022/11/bash_startup_files_logic-1-1024x501.png)<figcaption class="wp-element-caption">Graphical representation of `bash`‘s startup logic.</figcaption></figure>