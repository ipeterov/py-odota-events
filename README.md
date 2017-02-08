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
Setup: 
```python
>>> from core import EventGetter
>>> getter = EventGetter()
>>> events = getter.get_events(2978824598)
```
An example event: 
```python
>>> print events['DOTA_COMBATLOG_DAMAGE'][0]
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
Event types:
```python
>>> sorted(events.keys())
[u'CHAT_MESSAGE_AEGIS',
 u'CHAT_MESSAGE_BARRACKS_KILL',
 u'CHAT_MESSAGE_BUYBACK',
 u'CHAT_MESSAGE_DISCONNECT',
 u'CHAT_MESSAGE_DISCONNECT_TIME_REMAINING_PLURAL',
 u'CHAT_MESSAGE_DISCONNECT_WAIT_FOR_RECONNECT',
 u'CHAT_MESSAGE_EFFIGY_KILL',
 u'CHAT_MESSAGE_FIRSTBLOOD',
 u'CHAT_MESSAGE_GLYPH_USED',
 u'CHAT_MESSAGE_HERO_BANNED',
 u'CHAT_MESSAGE_HERO_BAN_COUNT',
 u'CHAT_MESSAGE_HERO_KILL',
 u'CHAT_MESSAGE_HERO_NOMINATED_BAN',
 u'CHAT_MESSAGE_INFORMATIONAL',
 u'CHAT_MESSAGE_INTHEBAG',
 u'CHAT_MESSAGE_ITEM_PURCHASE',
 u'CHAT_MESSAGE_PAUSED',
 u'CHAT_MESSAGE_PAUSE_COUNTDOWN',
 u'CHAT_MESSAGE_RECONNECT',
 u'CHAT_MESSAGE_REPORT_REMINDER',
 u'CHAT_MESSAGE_ROSHAN_KILL',
 u'CHAT_MESSAGE_RUNE_BOTTLE',
 u'CHAT_MESSAGE_RUNE_PICKUP',
 u'CHAT_MESSAGE_SCAN_USED',
 u'CHAT_MESSAGE_STREAK_KILL',
 u'CHAT_MESSAGE_TOWER_DENY',
 u'CHAT_MESSAGE_TOWER_KILL',
 u'CHAT_MESSAGE_UNPAUSED',
 u'CHAT_MESSAGE_UNPAUSE_COUNTDOWN',
 u'CHAT_MESSAGE_VICTORY_PREDICTION_STREAK',
 u'DOTA_COMBATLOG_ABILITY',
 u'DOTA_COMBATLOG_BUYBACK',
 u'DOTA_COMBATLOG_DAMAGE',
 u'DOTA_COMBATLOG_DEATH',
 u'DOTA_COMBATLOG_FIRST_BLOOD',
 u'DOTA_COMBATLOG_GAME_STATE',
 u'DOTA_COMBATLOG_GOLD',
 u'DOTA_COMBATLOG_HEAL',
 u'DOTA_COMBATLOG_ITEM',
 u'DOTA_COMBATLOG_KILLSTREAK',
 u'DOTA_COMBATLOG_MODIFIER_ADD',
 u'DOTA_COMBATLOG_MODIFIER_REMOVE',
 u'DOTA_COMBATLOG_MULTIKILL',
 u'DOTA_COMBATLOG_PLAYERSTATS',
 u'DOTA_COMBATLOG_PURCHASE',
 u'DOTA_COMBATLOG_TEAM_BUILDING_KILL',
 u'DOTA_COMBATLOG_XP',
 u'actions',
 u'chat',
 u'cosmetics',
 u'epilogue',
 u'interval',
 u'obs',
 u'obs_left',
 u'pings',
 u'player_slot',
 u'sen',
 u'sen_left']


```
There are many types of events and they will probably be documented as I explore them myself.

## Why
To my knowledge, there is currently no pure python solution for parsing replays and implementing one myself seemed very complicated. That's why I desided to pass replays to another solutions and parse them. I chose https://github.com/odota/parser. It offers a simple API - you POST a replay file and get `\n` separated json's containing events. There is a [dockerhub image](https://hub.docker.com/r/odota/parser/) for it which  makes it very easy to run.
