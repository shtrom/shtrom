---
id: 1569
title: 'The ultimate bash startup logic'
date: '2024-05-21T17:13:34+10:00'
author: 'Olivier Mehani'
excerpt: "It's always a bit confusing to reason about which startup files `bash` is going to run in a given situation.\nSo I made a chart."
layout: revision
guid: 'https://blog.narf.ssji.net/?p=1569'
permalink: '/?p=1569'
---

It’s always a bit confusing to reason about which startup files [`bash`(1)](https://manpages.org/bash) is going to run in a given situation. [It is documented, but the logic is not trivial](https://www.gnu.org/software/bash/manual/bash.html#Bash-Startup-Files).

So I made a chart ([using PlantUML](http://www.plantuml.com/plantuml/uml/nLD1Jp8n4BttLpIJxm07Fkvu43KOJOm7JJnXDiiw2mtTpgRjWiReRvVMx12RGa8ys0Ebsvath-_DJ9qlhUyQBU8V8LGj1yfiQ5rwHKQQii6Xz2iqSW2mADqAO2Ya_0xpQClAgmsUzp5lwC9r2DZ5ZqOjEVKAa5o7DG7uzpwxV_e0E8kVK3iCQPgMoZ2WeJvX3sh8LbdCk9odbiyHbL4I75lLIYD0fXPpd7-E_uTdswhdoSkGnuaijIEv3VdAj9sNjQLcRWpwBTcrhCWOh8AKdCka01wkhc_lPW1fsVucAOdcHTKYEJ9U8eGk5wXbe5v4HJCgjfPOWDEbPAvZzDMOiNum3csorx3WeBHVyfeNEL1k54Rc9nx7JQCpg8TR8CyaEY1JHpYrSsYbG-SKcMTnW0XrFg9oUaAbjojopbgr94-fqUbhuhHTNZpU53noNB3VHT-MfmnvEgt7nplRet_QeNb_4pT_OynHMvX-wWHlOhhxwHhz1G00)!). You’re welcome.

**EDIT**: There is also one for [`zsh`(1)](https://manpages.org/zsh) ([PlantUML](http://www.plantuml.com/plantuml/uml/pLJ1QkCm4BthAuJM1-SItxF6cyrc2GjX0qdfeRGKnvd48efK93cGrkstrsF5E55JGY6qzS68DvetxyqmwXkRQbji12aPUpGvOoKfVupvAhSpI4SQG9R1zCyCqQdQfM8W2YY3qNWo-3s-Tm76C2zYREtooG5NJK_uaePSRjKwjLn9AjCDTAZDGT9mVxD3AErL962pg090RXdxIIeGK-Dv4cTAADrhD2MCeIh6ugWE974qJnfA0nRfADqhnpEI1pV3oTNmtpJg7bN06g5GAov_DGmxC1qNyWKCrM856fk04fesd5M2tr7N6hGr_Q3LaWj0KIu2mW0D2tb00dB1btZsp7dsV2wNrbZbqe9ECyktyAM6JQwpZxgb9-qYa-VrsuorLd0PcuxAy-apDcpj2k9c5GOqDM0CL_BkacjrkiVlwbU5HGEVFmCiV7u8vnjB7EgUFAeqtRzwUEFDGzXAQ1VIWRSlKTV7WgU__w-Vw_QuMkq84I3zwbTin2i0)).

The main takeaway from this exercise is:

> In `sh` mode, `bash` and `zsh` do *slightly different things*.

# Bash

<div class="wp-block-image"><figure class="aligncenter size-large">![An activity diagram showing which startup files are processed by `bash` depending on context.](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2022/11/bash_startup_files_logic-1-1024x501.png)<figcaption class="wp-element-caption">Graphical representation of bash‘s startup logic.</figcaption></figure></div># Zsh

Sure enough, as soon as I shared this post. Someone chimed in asking for a version for [`zsh`(1)](https://manpages.org/zsh). As I suspected, it is equally hairy, but certainly different in incompatible ways.

<div class="wp-block-image"><figure class="aligncenter size-large">![](https://blog.narf.ssji.net/wp-content/uploads/sites/3/2023/03/zsh-startup-file-logic-456x1024.png)<figcaption class="wp-element-caption">Graphical representation of zsh‘s startup logic.</figcaption></figure></div>Update 2023-03-13: Fixed confusion between `zshrc` (interactive) and `zlogin` (login).