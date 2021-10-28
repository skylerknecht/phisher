import os
import random
import sqlite3
import sys

from collections import namedtuple

chars = ['a', 'b' 'c' 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def generate_str():
    _new_str = [str(chars[random.randint(0, len(chars)-1)]) for random_char in range (0,10)]
    _new_str = ''.join(_new_str)
    return _new_str

def generate_path(file_path):
    _new_path = f'{file_path}_{generate_str()}.old'
    while(os.path.exists(_new_path)):
        _new_path = f'{file_path}_{generate_str()}.old'
    return _new_path

class Engine:

    Result = namedtuple('Result', ['type', 'rid', 'ip', 'date'])
    User = namedtuple('Users', ['first', 'last', 'email'])

    results = []
    users = {}

    def __init__(self, visits_file, downloads_file, blocked_file):
        self.blocked_file = blocked_file
        self.downloads_file = downloads_file
        self.visits_file = visits_file
        return

    def ret_downloads(self):
        _results = []
        if not os.path.exists(f'{self.downloads_file}'):
            print('[-] No downloads found')
            return
        with open(f'{self.downloads_file}', 'r') as downloads:
            for download in downloads:
                data = download.rstrip().split('@')
                _results.append(self.Result('download', data[0], data[1], data[2]))
        return _results


    def ret_visits(self):
        _results = []
        if not os.path.exists(f'{self.visits_file}'):
            print('[-] No visits found')
            return
        with open(f'{self.visits_file}', 'r') as visits:
            for visit in visits:
                data = visit.rstrip().split('@')
                _results.append(self.Result('visit', data[0], data[1], data[2]))
        return _results

    def ret_blocked(self):
        _results = []
        if not os.path.exists(f'{self.blocked_file}'):
            print('[-] No blocks found')
            return
        with open(f'{self.blocked_file}', 'r') as blocks:
            for block in blocks:
                data = block.rstrip().split('@')
                _results.append(self.Result('block', data[0], data[1], data[2]))
        return _results

    def parse_results(self, database):
        try:
            query = sqlite3.connect(database).cursor()
        except:
            print('[-] Invalid database file')
            return
        for item in query.execute('select * from results'):
            self.users[item[3]] = self.User(item[4], item[5], item[6])
        self.results.extend(self.ret_downloads())
        self.results.extend(self.ret_visits())
        print('')
        for result in self.results:
            try:
                print('[+] ' + result.type.upper() + ': ' + self.users[result.rid].first + ' ' + self.users[result.rid].last + ', ' + self.users[result.rid].email  +  ', ' + result.ip + ', ' + result.date)
            except:
                continue
        print('')

    def backup_results(self, backup_path):
        if os.path.exists(f'{self.downloads_file}'):
            print('\n[+] Found downloads.txt', end='')
            _backup_path = generate_path(f'{backup_path}downloads')
            os.rename(f'{self.downloads_file}', _backup_path)
            print(f'\n[+] Downloads backed up to: {_backup_path}')
        else:
            print(f'\n[-] No downloads found')
        if os.path.exists(f'{self.visits_file}'):
            print('\n[+] Found visits.txt', end='')
            _backup_path = generate_path(f'{backup_path}visits')
            os.rename(f'{self.visits_file}', _backup_path)
            print(f'\n[+] Visits backed up to: {_backup_path}')
        else:
            print(f'\n[-] No visits found')

    def show_results(self):
        if os.path.exists(f'{self.downloads_file}'):
            self.results.extend(self.ret_downloads())
        if os.path.exists(f'{self.visits_file}'):
            self.results.extend(self.ret_visits())
        if os.path.exists(f'{self.blocked_file}'):
            self.results.extend(self.ret_blocked())
        if not self.results:
            print('[-] No results')
        for result in self.results:
            print('[+] ' + result.type.upper() + ': ' + result.rid + ', ' + result.ip + ', ' + result.date)
        print('')
