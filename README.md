# py-odota-events
A python interface to [odota/parser](https://github.com/odota/parser)

## About
This module was created to help getting meaningful data from dota's .dem files using python. It can:
* accept a match_id, download a corresponding replay, pass it to parse server and then return a list of events (dicts)
* accept an already downloaded replay and do the same thing
* cache parse results using [shelve](https://docs.python.org/2/library/shelve.html)

## Quickstart

### Setup Docker
For me (Fedora 24) it was:
```
sudo dnf install docker
sudo systemctl start docker
```
You should probably look for instructions at https://docs.docker.com/engine/installation/.

### Setup a parse server
```
docker pull odota/parser
sudo docker run --hostname 172.18.0.22 -p 5600:5600 odota/parser
```
This will run the image in the terminal, but it's also possible to run it in detached mode.

### Use the module
```python
>>> from core import EventGetter
>>> getter = EventGetter()
>>> events = getter.get_events(2978824598)
>>> print filter(lambda event: event['type'] == 'DOTA_COMBATLOG_DAMAGE', events)[0]
{u'attackerhero': True,
u'targethero': False,
u'attackername': u'npc_dota_hero_nevermore',
u'sourcename': u'npc_dota_hero_nevermore',
u'type': u'DOTA_COMBATLOG_DAMAGE',
u'value': 44,
u'inflictor': u'dota_unknown',
u'targetillusion': False,
u'attackerillusion': False,
u'time': 261,
u'gold_reason': 0,
u'xp_reason': 0,
u'targetname': u'npc_dota_creep_badguys_melee',
u'targetsourcename': u'npc_dota_creep_badguys_melee'}
```
There are many types of events and they will probably be documented as i explore them myself.

## Why
To my knowledge, there is currently no pure python solution for parsing replays and implementing one myself seemed very complicated. That's why I desided to pass replays to another solutions and parse them. I chose https://github.com/odota/parser. It offers a simple API - you POST a replay file and get `\n` separated json's containing events. There is a [dockerhub image](https://hub.docker.com/r/odota/parser/) for it which  makes it very easy to run.
