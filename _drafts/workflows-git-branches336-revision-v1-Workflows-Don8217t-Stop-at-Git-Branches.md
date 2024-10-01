---
id: 701
title: 'Workflows Don&#8217;t Stop at Git Branches'
date: '2022-10-30T00:21:17+11:00'
author: 'Jen Cuthbert'
layout: revision
guid: 'https://narf.jencuthbert.com/?p=701'
permalink: '/?p=701'
---

*I wrote this article for the [Learnosity blog, where it originally appeared](https://learnosity.com/workflows-dont-stop-git-branches/). I repost it here, with permission, for archival.*

A few weeks ago, a debate started on our channel for Git-related discussions. Following someone posting a link to [<span class="s1">Nicola Paolucci’s article on Core \[Git\] Concept, Workflows And Tips</span>](https://www.atlassian.com/git/articles/core-concept-workflows-and-tips), a question was raised:

> *Do we really need merge commits?*

What sounded like a fairly straightforward question quickly snowballed into one of those long chat threads that left us none the wiser. A follow-up face-to-face discussion helped us get down to the root of the problem: code and functional reviews on feature branches may leave us exposed to integration issues after non-fast-forward merges, and can only be caught too late for comfort.

We had to consider our Git workflow alongside the lifecycle of our tickets to come up with an improvement. Merge commits remain, but we rebase (and fix conflicts) on the latest main branch before any review in order to make sure we look at the final code.

The rest of this article describes our Git workflow, our ticket lifecycle, their interactions, and how we made them better.

### **tl;dr**

1. Rebase onto `develop` before code review (original developer)
2. Rebase onto `develop` before functional review (functional reviewer)
3. Deploy to staging as soon as possible (i.e., all codebases merged for the feature; original developer)

## Our Lightweight Git Workflow

For context, we follow a lightweight version of [<span class="s1">gitflow</span>](http://nvie.com/posts/a-successful-git-branching-model/).

[![A Git workflow showing feature branches merged into master and tagged as releases](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2018/02/Screenshot-from-2018-01-07-15-42-53.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2018/02/Screenshot-from-2018-01-07-15-42-53.png)

- We branch off `develop` for any new development work (feature of bugfix).
- We merge back into `develop` when the work is deemed complete (more on that later).
- We merge all the work from `develop` into `master` whenever we are ready to tag a new release candidate (which may contain one or more newly merged branches).
- We tag the latest RC as an official release when all is good (more on that later).
- We also backpatch important bug and security fixes by cherry-picking the commits onto previous release tags, and tagging a new patch release.

In this context, using merge commits works reasonably well, so the merge commit question came as a bit of a surprise to me. The asker elaborated:

> *Not* *having them would require us to fast-forward commits to develop which would then enforce proper rebasing to the tip of the branch. Merge commits have two parents, while fast-forwarded commits have only one, so it is much nicer, cleaner, and easier to check how things happened… Of course, the master branch could still have merge commits only because the message with a version in that branch is very helpful.*

A lively discussion ensued but we couldn’t reach a satisfactory conclusion, so I suggested we continue it during a brown-bag session.

### Merging vs. rebase

In preparation of the brown-bag session, I tried to collate all the pros and cons in the “Merge or Rebase” argument and summon a few more.

|  | **Pros** | **Cons** |
|---|---|---|
| **Merge** | - Branch name and ticket number easily linked to our issue tracker - See the history and where changes integrate | - Noisy for single-commit branches |
| **Rebase/Fast forward** | - Cleaner history | - Can’t revert whole set - No link to PR - People not necessarily comfortable with rebase - Normalises force push |

At face value, merges still seemed better to me, so I was curious to hear differing views.

## This is not the argument you are looking for

Pretty early on in the discussion, it turned out the real value of a rebased branch was that it includes newer commits from `develop`, even prior to merging. This is better for earlier integration and regression testing. What seemed to be a Git workflow question just got larger.

When I described our Git workflow earlier, I skipped over two questions:

1. *when is the work on a branch complete?* and
2. *when is a release candidate ready?*

This is because those questions are answered not by Git, but by the lifecycle of our tickets. We have two reviews stages, and two integration stages, in different environments.

[![Workflow from Development to Staging via Code and Functional Reviews](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2018/02/Screenshot-from-2018-01-07-15-53-38-1024x299.png)](http://narf.jencuthbert.com/wp-content/uploads/sites/3/2018/02/Screenshot-from-2018-01-07-15-53-38.png)

- **Code review**, on the differences in the pull request between the feature branch, and the branch to merge it in (generally `develop`).
- **Functional review**, where the feature branch is checked out in another developer’s development environment, and the work tested against the acceptance criteria of the ticket. Some regression testing is also done in areas touched by the changes and, of course, all automated unit and integration test suites are run.
- Integration testing in our **staging environment**. This is essentially a second round of functional review on release candidates rather than feature branches. The staging environment is a continuously-integrated, always-on platform. However, we require that all new code is deployed to staging no later than five working days before the release date.
- Integration testing in our **QA environment**, which is a freshly baked version of the soon-to-be new production environment, containing all new versions. The QA environment is spun up the day before the release.

## Back to the questions in our Git workflow

1. The functional review steps tell us *when the work on a branch is complete*, i.e., whether we can merge it to `develop`.
2. The staging tests tell us *whether an RC is ready* to be an actual released version.

The QA tests are a final safeguard, allowing us to do across-the-board checks to ensure that everything, new or pre-existing, is still in working order. While this has allowed us to find last-minute bugs before deploying a new release, detecting them at this stage is costly and stressful for everyone.

However, due to the way code is tested and merged in the workflow I have described, we have sometimes missed some fine *–* but often thorny *–* integration issues until the QA environment was up for a final test. This is because features are only checked in isolation during the functional reviews, and only the newly merged changes are checked for after staging the deployment.

This takes us back to the initial question, and some of the additional discussion.

> *Do we really need merge commits?*
> 
> *Not having them would require us to fast-forward commits to develop which would then enforce proper rebasing to the tip of the branch.*

The real question is not about merge commits, but about testing on rebased branches. Merge commits are only mentioned because rebasing is necessary without them to enable a fast-forward.

A new set of pros and cons emerges.

|  | **Pros** | **Cons** |
|---|---|---|
| **Non fast-forward merge** |  | - Tests are not run on the final merged code |
| **Rebase and fast forward merge** | - What’s merged has already been reviewed and tested as is |  |

It becomes clear from this table that performing code and functional reviews on rebased branches allows us to evaluate something much closer to the final state and spot issues earlier that would otherwise slip through to later integration stages.

This is particularly important with UI-related code, where getting automated tests to cover all the combinations of features and options is not trivial, and a manual test of combinations known to have seen change is often more effective.

## So, what should we do with Git?

The first table strongly suggested that having merge commits was better for legibility and manageability of the codebase’s history. Yet, rebasing and fast-forwarding has significant advantages during the review phases of our tickets’ lifecycles. Which one do we choose?

Both. A merge commit has *typically* two parents. It can, however, have as few as one, and as many as … many more. Nothing prevents us from creating single-parented merge commits for a fast-forward. This essentially allows us to retain the advantages of visible merges, while not foregoing the added benefit of rebased branches for review.

More specifically, I suggest that we rebase at key points during the ticket’s lifecycle. For completeness, I also discuss what to do with fixups coming from the reviews.

### Code review

Before code review, the branch should be rebased by the developer onto the latest `develop`. This gives an opportunity to fix potential conflicts, and get those fixes reviewed.

New commits should be added on top of the branch to address the reviewer’s comments ([<span class="s1">`git commit --fixup`</span>](https://git-scm.com/docs/git-commit#git-commit---fixupltcommitgt) is useful, as is [<span class="s1">`git commit --squash`</span>](https://git-scm.com/docs/git-commit#git-commit---squashltcommitgt) if you want to add more to the commit message). This allows us to distinguish fixes from the initial code, and makes multiple rounds of CR easier.

In mandating rebases before reviews, we cannot avoid two issues identified in our first pros/cons table, namely:

1. people may not be familiar or confident with doing rebases, and
2. this may normalize reckless `--force` pushes.

The first issue can be addressed in an ad-hoc fashion when needed, or perhaps through a hands on brown-bag session, and through our Git bootcamp for newcomers. [<span class="s1">LearnGitBranching</span>](https://learngitbranching.js.org/) also has at least two levels that are worthy of running through, [intro4](https://learngitbranching.js.org/?NODEMO&command=level%20intro4), and [move2](https://learngitbranching.js.org/?NODEMO&command=level%20move2) (interactive rebases).

The second issue is thornier, but can be resolved with [<span class="s1">`git push --force-with-lease`, which only allows sensible pushes</span>](https://git-scm.com/docs/git-push#git-push---no-force-with-lease), making sure not to overwrite anybody else’s work on the branch. We could also set up [<span class="s1">mechanisms to kick the `push -f` habit</span>](https://stackoverflow.com/questions/30542491/push-force-with-lease-by-default/47543571#47543571).

### Functional review

Once approved, and before the ticket moves to functional review, the fixup commits should be squashed as appropriate. The functional reviewer should then rebase the branch onto `develop`.

The functional review should focus on the acceptance criteria of the ticket under study, making sure all the test-suite pass, and keeping an eye out for incorrect interactions with other features introduced since the previous release.

Once again, new commits addressing comments from the functional review should be added on top of the branch and undergo their own mini-round of CR before returning to FR.

Once the reviewer is happy with the branch, fixup commits can once again be squashed, and the branch is ready to be merged.

In some cases, it may happen that new branches were merged into `develop` during the two reviews. In this case (or when the rebase conflicts), another rebase is necessary and, unfortunately, yet another round of CR and FR to ensure everything on the branch is still acceptable.

### Deploy to staging ASAP

Our process so far did not specify when to deploy to staging. This cannot be done automatically as we have a number of interrelated codebases for which features sometimes need to be deployed in unison.

Rather, whenever there was enough work merge, or somebody was very keen to see their work on staging, would a new RC be made. This generally meant that we had a rush to deploy to staging in the last few days before the staging deadline.

A better approach would be to deploy to staging as soon as the work for a feature is complete (that is, done across all involved codebases). This allows us to test integration of the new feature earlier, as well as get many more eyeballs (other people testing other work) on the newly merged code. This creates more opportunities to spot bugs earlier, and go back to fixing them, along with new automated tests for the newly found condition.

Once deployed to staging, a summary test should be performed to confirm that the new feature or bugfix has indeed landed. Later on, closer to the staging deadline, a more thorough test should be conducted, keeping an eye for regressions in both the new features and the rest of the system. At this stage, the relevant systems can be marked as *Ready for QA*, and the release process is ready to start.

## Conclusion

What started off framed as a pure Git-centric question on a detail led us to revisit not our Git workflow itself as much as its interaction with the lifecycle of our tickets.

The real need was not to dispense of merge commits, but rather to avoid non-fast-forward commits to `develop` after code and functional reviews. Indeed, the state of `develop` after the merge is otherwise an unreviewed and untested unknown, particularly if conflicts had to be resolved during the merge.

The core of the proposed solution is to rebase a feature branch onto `develop` before the reviews. This enables us to perform the review on code that is exactly what `develop` will be after the merge. For legibility of the commit history, however, we still want to create fast-forward merge commits; this also makes them more easily revertable.

Another aspect of the solution is to deploy the merged code to our staging integration environment as soon as possible. This way everyone else using the environment has their eyeballs on the very latest version of the system, along with any potential new bugs, nice and early.

On a final note, it’s worth being mindful of how a simple question on a technical detail could reveal a much more involved root cause. Getting to the bottom of this required us taking a step back and moving to a richer conversation medium (face to face and audio/video) rather than just a text-based chat.