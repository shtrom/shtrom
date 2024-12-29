---
id: 1716
title: 'Monkeypatch with side-effects'
date: '2024-12-05T16:33:50+11:00'
author: 'Olivier Mehani'
layout: post
guid: 'https://blog.narf.ssji.net/?p=1716'
permalink: '/?p=1716'
categories:
    - Uncategorised
---

“`  
def test\_GitSCM\_clone(git\_repo: Path, tmp\_path: Path, monkeypatch):   
 clone\_path = tmp\_path / “repo\_test\_GitSCM\_clone”   
 scm = GitSCM(str(clone\_path))   
  
 mock\_git\_run = \_monkeypatch\_scm(monkeypatch, scm, “\_git\_run”)   
  
 scm.clone(str(git\_repo))   
  
 mock\_git\_run.assert\_called\_with(“clone”, str(git\_repo), str(clone\_path), cwd=”/”)   
 assert clone\_path.exists(), f”New git clone {clone\_path} wasn’t created”   
 assert (   
 clone\_path / “.git”   
 ).exists(), f”New git clone {clone\_path} doesn’t contain a .git directory”  
  
def \_monkeypatch\_scm(monkeypatch, scm: GitSCM, method: str) -&gt; MagicMock:  
 “””  
 Mock a method on `scm` to test the call, but let it continue with its original side  
 effect, so we can test that it’s correct, too.  
  
 Returns:  
 MagicMock: The mock object.  
 “””  
 original = scm.\_\_getattribute\_\_(method)  
 mock = MagicMock()  
 mock.side\_effect = original  
 monkeypatch.setattr(scm, method, mock)  
 return mock  
“`