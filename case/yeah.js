
                
I accidentally committed the wrong files to Git but didn't push the commit to the server yet.
How can I undo those commits from the local repository?
The only way seems to be to copy the edits in some kind of GUI text editor, then wipe the whole local clone, then re-clone the repository, then re-applying the edits. However,

This can cause data loss.
It's very hard to do this when only an accidental git commit was run.

Is there a better way?
    Undo a commit & redo
$ git commit -m "Something terribly misguided" # (0: Your Accident)
$ git reset HEAD~                              # (1)
[ edit files as necessary ]                    # (2)
$ git add .                                    # (3)
$ git commit -c ORIG_HEAD                      # (4)


git reset is the command responsible for the undo. It will undo your last commit while leaving your working tree (the state of your files on disk) untouched. You'll need to add them again before you can commit them again).
Make corrections to working tree files.
git add anything that you want to include in your new commit.
Commit the changes, reusing the old commit message. reset copied the old head to .git/ORIG_HEAD; commit with -c ORIG_HEAD will open an editor, which initially contains the log message from the old commit and allows you to edit it. If you do not need to edit the message, you could use the -C option.

Alternatively, to edit the previous commit (or just its commit message), commit --amend will add changes within the current index to the previous commit.
To remove (not revert) a commit that has been pushed to the server, rewriting history with git push origin main --force[-with-lease] is necessary. It's almost always a bad idea to use --force; prefer --force-with-lease instead, and as noted in the git manual:

You should understand the implications of rewriting history if you [rewrite history] has already been published.


Further Reading
You can use git reflog to determine the SHA-1 for the commit to which you wish to revert. Once you have this value, use the sequence of commands as explained above.

HEAD~ is the same as HEAD~1. The article What is the HEAD in git? is helpful if you want to uncommit multiple commits.
    Undoing a commit is a little scary if you don't know how it works.  But it's actually amazingly easy if you do understand. I'll show you the 4 different ways you can undo a commit.
option 1: git reset --hard
Say you have this, where C is your HEAD and (F) is the state of your files.
   (F)
A-B-C
    ↑
  master

You want to nuke commit C and never see it again and lose all the changes in locally modified files.  You do this:
git reset --hard HEAD~1

The result is:
 (F)
A-B
  ↑
master

Now B is the HEAD.  Because you used --hard, your files are reset to their state at commit B.
option 2: git reset
Ah, but suppose commit C wasn't a disaster, but just a bit off.  You want to undo the commit but keep your changes for a bit of editing before you do a better commit.  Starting again from here, with C as your HEAD:
   (F)
A-B-C
    ↑
  master

You can do this, leaving off the --hard:
git reset HEAD~1

In this case the result is:
   (F)
A-B-C
  ↑
master

In both cases, HEAD is just a pointer to the latest commit.  When you do a git reset HEAD~1, you tell Git to move the HEAD pointer back one commit.  But (unless you use --hard) you leave your files as they were.  So now git status shows the changes you had checked into C.  You haven't lost a thing!
option 3: git reset --soft
For the lightest touch, you can even undo your commit but leave your files and your index:
git reset --soft HEAD~1

This not only leaves your files alone, it even leaves your index alone.  When you do git status, you'll see that the same files are in the index as before.  In fact, right after this command, you could do git commit and you'd be redoing the same commit you just had.
option 4: you did git reset --hard and need to get that code back
One more thing: Suppose you destroy a commit as in the first example, but then discover you needed it after all?  Tough luck, right?
Nope, there's still a way to get it back.  Type git reflog and you'll see a list of (partial) commit shas (that is, hashes) that you've moved around in.  Find the commit you destroyed, and do this:
git checkout -b someNewBranchName shaYouDestroyed

You've now resurrected that commit.  Commits don't actually get destroyed in Git for some 90 days, so you can usually go back and rescue one you didn't mean to get rid of.
    There are two ways to "undo" your last commit, depending on whether or not you have already made your commit public (pushed to your remote repository):
How to undo a local commit
Let's say I committed locally, but now I want to remove that commit.
git log
    commit 101: bad commit    # Latest commit. This would be called 'HEAD'.
    commit 100: good commit   # Second to last commit. This is the one we want.

To restore everything back to the way it was prior to the last commit, we need to reset to the commit before HEAD:
git reset --soft HEAD^     # Use --soft if you want to keep your changes
git reset --hard HEAD^     # Use --hard if you don't care about keeping the changes you made

Now git log will show that our last commit has been removed.
How to undo a public commit
If you have already made your commits public, you will want to create a new commit which will "revert" the changes you made in your previous commit (current HEAD).
git revert HEAD

Your changes will now be reverted and ready for you to commit:
git commit -m 'restoring the file I removed by accident'
git log
    commit 102: restoring the file I removed by accident
    commit 101: removing a file we don't need
    commit 100: adding a file that we need

For more information, check out Git Basics - Undoing Things.
    Add/remove files to get things the way you want:

git rm classdir
git add sourcedir


Then amend the commit:

git commit --amend


The previous, erroneous commit will be edited to reflect the new index state - in other words, it'll be like you never made the mistake in the first place.

Note that you should only do this if you haven't pushed yet. If you have pushed, then you'll just have to commit a fix normally.
    git rm yourfiles/*.class
git commit -a -m "deleted all class files in folder 'yourfiles'"


or

git reset --hard HEAD~1


Warning: The above command will permanently remove the modifications to the .java files (and any other files) that you wanted to commit.

The hard reset to HEAD-1 will set your working copy to the state of the commit before your wrong commit.
    To change the last commit
Replace the files in the index:
git rm --cached *.class
git add *.java

Then, if it's a private branch, amend the commit:
git commit --amend

Or, if it's a shared branch, make a new commit:
git commit -m 'Replace .class files with .java files'


(To change a previous commit, use the awesome interactive rebase.)

ProTip™: Add *.class to a gitignore to stop this happening again.

To revert a commit
Amending a commit is the ideal solution if you need to change the last commit, but a more general solution is reset.
You can reset Git to any commit with:
git reset @~N

Where N is the number of commits before HEAD, and @~ resets to the previous commit.
Instead of amending the commit, you could use:
git reset @~
git add *.java
git commit -m "Add .java files"

Check out git help reset, specifically the sections on --soft --mixed and --hard, for a better understanding of what this does.
Reflog
If you mess up, you can always use the reflog to find dropped commits:
$ git reset @~
$ git reflog
c4f708b HEAD@{0}: reset: moving to @~
2c52489 HEAD@{1}: commit: added some .class files
$ git reset 2c52489
... and you're back where you started


    Use git revert <commit-id>.

To get the commit ID, just use git log.
    If you are planning to undo a local commit entirely, whatever you change you did on the commit, and if you don't worry anything about that, just do the following command.
git reset --hard HEAD^1

(This command will ignore your entire commit and your changes will be lost completely from your local working tree). If you want to undo your commit, but you want your changes in the staging area (before commit just like after git add) then do the following command.
git reset --soft HEAD^1

Now your committed files come into the staging area. Suppose if you want to upstage the files, because you need to edit some wrong content, then do the following command
git reset HEAD

Now committed files to come from the staged area into the unstaged area. Now files are ready to edit, so whatever you change, you want to go edit and added it and make a fresh/new commit.
More (link broken) (Archived version)
    If you have Git Extras installed, you can run git undo to undo the latest commit. git undo 3 will undo the last three commits.
    I wanted to undo the latest five commits in our shared repository. I looked up the revision id that I wanted to rollback to. Then I typed in the following.

prompt> git reset --hard 5a7404742c85
HEAD is now at 5a74047 Added one more page to catalogue
prompt> git push origin master --force
Total 0 (delta 0), reused 0 (delta 0)
remote: bb/acl: neoneye is allowed. accepted payload.
To git@bitbucket.org:thecompany/prometheus.git
 + 09a6480...5a74047 master -> master (forced update)
prompt>

    I prefer to use git rebase -i for this job, because a nice list pops up where I can choose the commits to get rid of. It might not be as direct as some other answers here, but it just feels right.

Choose how many commits you want to list, then invoke like this (to enlist last three)

git rebase -i HEAD~3


Sample list

pick aa28ba7 Sanity check for RtmpSrv port
pick c26c541 RtmpSrv version option
pick 58d6909 Better URL decoding support


Then Git will remove commits for any line that you remove.
    How to fix the previous local commit

Use git-gui (or similar) to perform a git commit --amend. From the GUI you can add or remove individual files from the commit. You can also modify the commit message. 

How to undo the previous local commit

Just reset your branch to the previous location (for example, using gitk or git rebase). Then reapply your changes from a saved copy. After garbage collection in your local repository, it will be like the unwanted commit never happened. To do all of that in a single command, use git reset HEAD~1.

Word of warning: Careless use of git reset is a good way to get your working copy into a confusing state. I recommend that Git novices avoid this if they can.

How to undo a public commit

Perform a reverse cherry pick (git-revert) to undo the changes.

If you haven't yet pulled other changes onto your branch, you can simply do...

git revert --no-edit HEAD


Then push your updated branch to the shared repository.

The commit history will show both commits, separately.



Advanced: Correction of the private branch in public repository

This can be dangerous -- be sure you have a local copy of the branch to repush.

Also note: You don't want to do this if someone else may be working on the branch.

git push --delete (branch_name) ## remove public version of branch


Clean up your branch locally then repush...

git push origin (branch_name)


In the normal case, you probably needn't worry about your private-branch commit history being pristine.  Just push a followup commit (see 'How to undo a public commit' above), and later, do a squash-merge to hide the history.
    If you want to permanently undo it and you have cloned some repository.
The commit id can be seen by:
git log 

Then you can do like:
git reset --hard <commit_id>

git push origin <branch_name> -f

    If you have committed junk but not pushed,

git reset --soft HEAD~1



  HEAD~1 is a shorthand for the commit before head. Alternatively you can refer to the SHA-1 of the hash if you want to reset to. --soft option will delete the commit but it will leave all your changed files "Changes to be committed", as git status would put it.
  
  If you want to get rid of any changes to tracked files in the working tree since the commit before head use "--hard" instead.


OR


  If you already pushed and someone pulled which is usually my case, you can't use git reset. You can however do a git revert,


git revert HEAD



  This will create a new commit that reverses everything introduced by the accidental commit.

    On SourceTree (GUI for GitHub), you may right-click the commit and do a 'Reverse Commit'. This should undo your changes.

On the terminal:

You may alternatively use:

git revert


Or:

git reset --soft HEAD^ # Use --soft if you want to keep your changes.
git reset --hard HEAD^ # Use --hard if you don't care about keeping your changes.

    A single command:

git reset --soft 'HEAD^' 


It works great to undo the last local commit!
    Just reset it doing the command below using git:

git reset --soft HEAD~1


Explain: what git reset does, it's basically reset to any commit you'd like to go back to, then if you combine it with --soft key, it will go back, but keep the  changes in your file(s), so you get back to the stage which the file was just added, HEAD is the head of the branch and if you combine with ~1 (in this case you also use HEAD^), it will go back only one commit which what you want...

I create the steps in the image below in more details for you, including all steps that may happens in real situations and committing the code:


    "Reset the working tree to the last commit"
git reset --hard HEAD^ 

"Clean unknown files from the working tree"
git clean    

see - Git Quick Reference
NOTE: This command will delete your previous commit, so use with caution! git reset --hard is safer.
    How to undo the last Git commit?

To restore everything back to the way it was prior to the last commit, we need to reset to the commit before HEAD.


If you don't want to keep your changes that you made:

git reset --hard HEAD^

If you want to keep your changes:

git reset --soft HEAD^



Now check your git log. It will show that our last commit has been removed.
    Use reflog to find a correct state

git reflog



REFLOG BEFORE RESET

Select the correct reflog (f3cb6e2 in my case) and type 

git reset --hard f3cb6e2


After that the repo HEAD will be reset to that HEADid

LOG AFTER RESET

Finally the reflog looks like the picture below


REFLOG FINAL
    First run: 

git reflog


It will show you all the possible actions you have performed on your repository, for example, commit, merge, pull, etc.

Then do:

git reset --hard ActionIdFromRefLog

    Undo last commit:

git reset --soft HEAD^ or git reset --soft HEAD~

This will undo the last commit.

Here --soft means reset into staging.

HEAD~ or HEAD^ means to move to commit before HEAD.



Replace last commit to new commit:

git commit --amend -m "message"


It will replace the last commit with the new commit.
    Another way:

Checkout the branch you want to revert, then reset your local working copy back to the commit that you want to be the latest one on the remote server (everything after it will go bye-bye). To do this, in SourceTree I right-clicked on the and selected "Reset BRANCHNAME to this commit".

Then navigate to your repository's local directory and run this command:

git -c diff.mnemonicprefix=false -c core.quotepath=false push -v -f --tags REPOSITORY_NAME BRANCHNAME:BRANCHNAME


This will erase all commits after the current one in your local repository but only for that one branch.
    Type git log and find the last commit hash code and then enter:

git reset <the previous co>

    In my case I accidentally committed some files I did not want to. So I did the following and it worked:

git reset --soft HEAD^
git rm --cached [files you do not need]
git add [files you need]
git commit -c ORIG_HEAD


Verify the results with gitk or git log --stat
    Simple, run this in your command line:

git reset --soft HEAD~ 

    There are two main scenarios

You haven't pushed the commit yet

If the problem was extra files you commited (and you don't want those on repository), you can remove them using git rm and then commiting with --amend

git rm <pathToFile>


You can also remove entire directories with -r, or even combine with other Bash commands

git rm -r <pathToDirectory>
git rm $(find -name '*.class')


After removing the files, you can commit, with --amend option

git commit --amend -C HEAD # the -C option is to use the same commit message


This will rewrite your recent local commit removing the extra files, so, these files will never be sent on push and also will be removed from your local .git repository by GC.

You already pushed the commit

You can apply the same solution of the other scenario and then doing git push with the -f option, but it is not recommended since it overwrites the remote history with a divergent change (it can mess your repository).

Instead, you have to do the commit without --amend (remember this about -amend`: That option rewrites the history on the last commit).
    For a local commit

git reset --soft HEAD~1


or if you do not remember exactly in which commit it is, you might use

git rm --cached <file>


For a pushed commit

The proper way of removing files from the repository history is using git filter-branch. That is,

git filter-branch --index-filter 'git rm --cached <file>' HEAD


But I recomnend you use this command with care. Read more at git-filter-branch(1) Manual Page.
    To reset to the previous revision, permanently deleting all uncommitted changes: 

git reset --hard HEAD~1

    WHAT TO USE, reset --soft or reset --hard?

I am just adding two cents for @Kyralessa's answer:

If you are unsure what to use go for --soft (I used this convention to remember it --soft for safe).

Why ?

If you choose --hard by mistake you will LOSE your changes as it wasn't before.
If you choose --soft by mistake you can achieve the same results of --hard by applying additional commands

git reset HEAD file.html
git checkout -- file.html


Full example

echo "some changes..." > file.html
git add file.html
git commit -m "wrong commit"

# I need to reset
git reset --hard HEAD~1 (cancel changes)
# OR
git reset --soft HEAD~1 # Back to staging
git reset HEAD file.html # back to working directory
git checkout -- file.html # cancel changes


Credits goes to @Kyralessa.
    