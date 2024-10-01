---
id: 811
title: 'Pure CSS folding menu'
date: '2023-02-09T23:49:06+11:00'
author: 'Olivier Mehani'
layout: revision
guid: 'https://blog.narf.ssji.net/?p=811'
permalink: '/?p=811'
---

A few of the sites that I maintain are static, and I dare think that thay are hand-crafted. At the very least, they took that amount of time to do. As static, all-public sites, I try to have them as devoid of dependencies as possible, and this involves Javascript.

Now, I recently decided to give them all a mobile support, which would display a lighter interface with less elements when the device width is small enough. This usually involves taking whatever sidebar was around, and hiding it by default.

The problem was how to make it come back, and for a long time (well, not so long, but it felt like it), I had to have a mini function registered to the <tt>onclick</tt> event of the menu header. It simply made the rest appear or disappear by changing the CSS class of the menu container (rather than the <tt>visibility</tt> of the kids directly, to avoid problem when rotating the device. Fortunately, using the <tt>:target</tt> CSS selector, it is possible to dispose of this trick, and make an (almost) perfect CSS folding menu.

The <tt>:target</tt> CSS selector applies to an element when its <tt>id</tt> is passed as the *fragment identifier* in the URL (the bit at the end of the URL, after the <tt>\#</tt>). This allows to create two different styles for the menu container, depending on whether it is targetted (shown) or not (hidden).

Let’s take an example.

```
...
<body>
  <nav id="menu">
    <h2 class="open"><a href="#menu">Menu</a></h2>
    <h2 class="close"><a href="#">Menu</a></h2>
    <ul>
      <li>Foo</li>
      <li>Bar</li>
      <li>Baz</li>
    </ul>
  </nav>
  ...
</body>
```

Here, we have a <tt>nav</tt> element with <tt>id</tt> “<tt>menu</tt>”, and some content, including some markup to let the user change the visibility of the menu. What’s important at this stage is the <tt>h2</tt> which contains a link to “<tt>\#menu</tt>”.

At this stage, we need some CSS which implements the toggling that is, shows the menu contents only when <tt>\#menu</tt> is targetted.

```
@media screen and (max-width: 480px) { /* We only want this behaviour on small screens */
  #menu li 
  #menu h2.close,
  #menu:target h2.open {
    visibility: hidden;
  }
  #menu:target li,
  #menu:target h2.close,
  #menu h2.open {
    visibility: block;
  }
  #
}
```

And that’s it. Almost as easy as it could be. The only trickery here is that my HTML code up there has two <tt>h2</tt> element with the menu title. They have hardcoded links to either <tt>\#menu</tt> or <tt>\#</tt> that is, they allow to open or close the menu. In addition to toggling visibility of the contents of the menu, this little bit of CSS also takes care of only displaying the <tt>h2</tt> element containing the right link.

The last thing to fix is that most devices with small screens still try to fit the page in it as if it were much larger. Adding a <tt>meta</tt> in the <tt>head</tt> telling that device that it should be honest does the trick.

```
  <meta name="viewport" content="width=device-width">
```

This is a nice and simple solution overall, but it has a few drawbacks. The most obvious one is probably the double <tt>h2</tt> element. I could probably have used some Javascript to change the link dynamically, but this would have defeated the purpose; another option would have been to use specific clickey elements with a nice icon on it, to avoid the redundancy, but I was at the end of my hand-crafting session. Another small detail is that this probably interferes with the normal use of targets to navigate within a page, so it should probably be limited to mobile layouts, lest some unwanted jumping happens. However, altogether, I have a nice and short CSS solution, and no need for Javascript, so I am quite happy. You can try it out on this very site!

**Update 2014-04-23:** This trick is no longer used on this site, now hosted on WordPress. It still works nicely nonetheless.

</body>