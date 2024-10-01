---
id: 677
title: 'Unlock a logged-in Mac OS X account before minutesUntilFailedLoginReset has expired'
date: '2022-10-28T13:21:33+11:00'
author: 'Jen Cuthbert'
layout: revision
guid: 'https://narf.jencuthbert.com/?p=677'
permalink: '/?p=677'
---

**XXX: This doesn’t actually work!**

Do you fat-finger your password often enough that you get locked out of your Mac often? Is `minutesUntilFailedLoginReset` too long to wait?

Here’s a solution that doesn’t require a reboot. It uses the `pwpolicy` tool, and another, pre-existing admin account (you should create one now).

Ahead of time, you’ll need another admin account (*with a good password*). You’ll need one more admin account than however many you intend to lock yourself out.

In general, an admin has the right to simply reset another admin user’s password in the *Users &amp; Groups* settings, but *only when they are not logged in.* This is fine if you were trying to log in, but if you were trying to unlock your running session, the other admin account cannot reset your password in this way

A tell-tale indication that your account is locked out:

```
USER=user
pwpolicy -u ${USER}  authentication-allowed
User <user> is not allowed to authenticate: Failed record policy "ProfilePayload:3599cd6c-6229-3bd5-a280-2bf6389cf6ca:minutesUntilFailedLoginReset"
```

Switch to the other admin account, and clear/re-set the password policies. It will reset the timeout.

<div class="wp-block-group"><div class="wp-block-group__inner-container is-layout-flow wp-block-group-is-layout-flow"><div class="wp-block-group"><div class="wp-block-group__inner-container is-layout-flow wp-block-group-is-layout-flow">```
USER=user
sudo pwpolicy -u ${USER} getaccountpolicies | sed 1d | xpath ' /plist/dict' > ${USER}.pwpolicy
sudo pwpolicy -u ${USER} clearaccountpolicies
sudo pwpolicy -u ${USER} setaccountpolicies ${USER}.pwpolicy
```

</div></div></div></div>The following should now be expected. But because this solution doesn’t actually work, except if you spend more than `autoEnableInSeconds` working it out. The best would be to be able to reset `policyAttributeLastFailedAuthenticationTime`.

```
USER=user
pwpolicy -u ${USER}  authentication-allowed
Policy allows user <user> to authenticate
```

This is convoluted and far from straightforward, but it works. If someone knows of a better of immediately resetting the lockout timer, and allowing the user to log in, I’d be delighted to learn it!

Not locked-out yet? Create a separate admin account now!