---
id: 267
title: 'SSH (Secure SHell'
date: '2024-02-13T00:02:54+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=267'
permalink: '/?p=267'
categories:
    - Uncategorised
tags:
    - wip
---

## SSH (Secure SHell)

### What is SSH good for?

1. Remote shell 
    1. `<strong>ssh</strong> [remote_login]@hostname`
    2. uses your local login if unspecified
    3. encrypted channel
2. Remote command execution 
    1. `ssh [remote_login]@hostname <strong>"COMMAND1; OTHER COMMAND"</strong><br></br>`
    2. same return status as if executing the command locally
3. File access 
    1. `<strong>scp</strong> [[remote_login1]@hostname1<strong>:</strong>]/path/to/source [[remote_login2]@hostname2<strong>:</strong>]/path/to/destination`
4. Dedicated remote access (through limited login), e.g., git 
    1. Difference between [https://github.com**/**Project/codebase](https://github.com/Learnosity/project) and git@github.com**:**Project/codebase 
        1. https is public read-only (unless HTTP auth); git+ssh is reflects your read/write permissions on the project (e.g., can push without having to re-authenticate)
        2. git+ssh:// uses keys to authenticate

### How does authentication work?

1. Public/Private keys 
    1. Mutual authentication 
        1. Generate a shared session key using Diffie-Hellman
        2. Server authenticates to client 
            1. `The authenticity of host '<a href="http://gitlab.com">gitlab.com</a> (104.210.2.228)' can't be established.`  
                `ECDSA key fingerprint is SHA256:HbW3g8zUjNSksFbqTiUWPWg2Bq1x8xdGUrliXFzSnUw.`  
                `Are you sure you want to continue connecting (yes/no)?`
                1. **Check the keys**! For example <https://help.github.com/articles/what-are-github-s-ssh-key-fingerprints/>
                2. Trust on first contact, later on stored in `.ssh/known_hosts`
            2. `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`
                1. server’s key is different from know\_hosts 
                    1. You trashed/rebuild your VG
                    2. Man-in-the-middle?
                    3. **Check the keys**
                        1. `<strong>ssh-keygen</strong> -R hostname` (if you know the old key is no longer valid
        3. Client authenticates to server 
            1. First tries keys 
                1. Allowed if key present in `~remote_login/.ssh/authorized_keys`
                2. Generate key with 
                    1. ssh-keygen -t ed25519
                    2. ssh-keygen -o -t rsa -b 3048\_OR\_LARGER -o
                    3. **Use a passphrase**
                3. Install new keys with `<strong>ssh-copy-id</strong> [remote_login@]server`
            2. Ends up with password
2. Setting up an agent to avoid having to repeatedly type the passphrase 
    1. **Don’t store in keychain/iCloud**
    2. Add key to agent 
        1. `ssh-add<strong> </dev/null</strong>`
            1. Don’t ask…
        2. Set a lifetime to you agent with **`ssh-agent -t 8h`**
            1. will forget the key after that
    3. Check the key 
        1. `ssh-add <strong>-L</strong>`
    4. Forwarding the agent 
        1. `ssh <strong>-A</strong> [remote_login]@hostname`

### Advanced stuff

1. Port forwarding 
    1. Make services on the remote network available to the local machine 
        1. `ssh <strong>-L localport:remote_hostname:remote_localhost_port</strong> [remote_login]@hostname`
        2. *Local* connections to `localhost:localport` will expose the service on `remote_hostname:remote_hostame_port` in the remote network
    2. Make services on the local network available to the remote machine 
        1. `ssh <strong>-R remote_localhost_port:local_hostname:local_hostname_port</strong> [remote_login]@hostname`
        2. Connecrions from the remote machineto `localhost:remote_localhost_port` will expose the service on `local_hostname:local_hostname_port`
        3. Good when working from home[![img_20161103_161802](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2016/11/IMG_20161103_161802-300x152.jpg)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2016/11/IMG_20161103_161802.jpg)
2. `.ssh/config`
    1. Record default hostnames, usernames, port forwarding,… to avoid having to type them

| ``` Host work   Hostname 192.0.2.142   User USER   # needs   #   #    127.0.0.3        dev.example.com   #   # in /etc/hosts   # no need for root access   LocalForward 127.0.0.3:10080 dev.example.com:80   LocalForward 127.0.0.3:10443 dev.example.com:443   # sudo iptables -t nat -A OUTPUT -d dev.example.com -p tcp --dport 80 -j DNAT --to 127.0.0.3:10080   # sudo iptables -t nat -A OUTPUT -d dev.example.com -p tcp --dport 443 -j DNAT --to 127.0.0.3:10443 ``` |
|---|

## Take home messages

- Pretty useful tool
- Use keys to avoid having to enter passwords all the time 
    - Use a passphrase
    - Use an agent 
        - **Don’t store it in keychain** OR **Don’t sync keychain to iCloud**
        - Having to type a passphrase once a day confirms that the passphrase is adequately protecting your key
    - Rotate your keys every so often
- Check the remote hosts’ keys before accepting them
- Forward all the ports[![72855711](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2016/11/72855711-300x225.jpg)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2016/11/72855711.jpg)