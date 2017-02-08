import bz2
import ConfigParser
import json
import os.path
import shelve
import subprocess

import requests


class EventGetter:
    def __init__(self, db_file=None, config_file='config.ini'):
        self.config = ConfigParser.ConfigParser()
        self.config.read(config_file)

        self.db = shelve.open(db_file or self.config.get('core', 'db_file'))

    def parse_replay(self, replay_file):
        replay_file = os.path.expanduser(replay_file)

        if not os.path.isfile(replay_file):
            raise Exception('The file does not exist')

        # This is horrendous but works, couldn't get requests to do it
        cmd = 'curl {host}:{port} -s --data-binary "@{filename}"'.format(
            host=self.config.get('parse_server', 'host'),
            port=self.config.get('parse_server', 'port'),
            filename=replay_file
        )

        events = []
        try:
            raw = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True);                         
        except CalledProcessError as exc:                                                                                                   
            raise Exception('Couldn\'t get parsed data from parse server: {}'.format(exc))
        else:
            for line in raw.strip('\n').split('\n'):
                events.append(json.loads(line))

        return events

    def download_replay(self, match_id):
    	replay_data = requests.get(
            self.config.get('replay_server', 'url'),
            params={'match_id': match_id}
        ).json()[0]

        download_url = 'http://replay{cluster}.valve.net/570/{match_id}_{replay_salt}.dem.bz2'.format(
            cluster=replay_data['cluster'],
            match_id=replay_data['match_id'],
            replay_salt=replay_data['replay_salt']
        )

        replay_file = os.path.join(self.config.get('core', 'temp_folder'), '{match_id}.dem'.format(match_id=match_id))
        response = requests.get(download_url, stream=True)
        with open(replay_file, 'w') as f:
            f.write(bz2.decompress(response.content))

        return replay_file

    def process_events(self, events):
        event_dict = {}
        for event in events:
            event_dict.setdefault(event['type'], []).append(event)
        return event_dict

    def get_events(self, match_id, replay_file=None):
        events = self.db.get(str(match_id))
        if events is None:
            replay_file = replay_file or self.download_replay(match_id)
            events = self.parse_replay(replay_file)
            self.db[str(match_id)] = events
            self.db.sync()
        return self.process_events(events)
