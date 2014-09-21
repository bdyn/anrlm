anrlm
=====

A league manager for [Fantasy Flight's *Android: Netrunner* Living Card
Game][ffg].


Getting Started
---------------
Fork and clone the repostory, then make sure you have GNU Make installed
(`which make`). To create a Python virtual environment and install all the
project dependencies,

```bash
cd ~/projects/anrlm  # substitute the location of your clone here
make bootstrap
```

Before using any of Django's built-in `manage.py` commands, you'll need to
activate the virtual environment: `source .virtualenv/bin/activate`. A handy,
cross-repository shell alias for this is

```bash
alias virt='REPO=`git rev-parse --show-toplevel`; source $REPO/.virtualenv/bin/activate'
```


Disclaimer & License
--------------------
All code is copyright Brandyn Lee, 2014. The Netrunner card game is copyrighted
by Fantasy Flight Publishing, Inc. ANRLM is not affiliated with or approved by
Fantasy Flight.

[ffg]: http://www.fantasyflightgames.com/edge_minisite.asp?eidm=207&enmi=Android:%20Netrunner%20The%20Card%20Game
