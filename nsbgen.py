import re
import requests
import json
import os.path

while True:
    try:
        _ns_config_path = input('NoScript config path: ').strip('"')
        _ns_config_json = json.load(open(_ns_config_path))
    except FileNotFoundError:
        print('Invalid file path.')
        continue
    else:
        break

_blacklist_pool = set()
_whitelist_pool = []

_regex_hosts = re.compile(r'^(?:[0-9.]+\s+)?(?:https?://)?(?:www\.)?([a-z0-9.\-_]+\.[a-z]+)', re.I | re.M)
_regex_adblock = re.compile(r'^\|\|([a-z0-9\-_.]+)\^\$?(?:third-party)?(?:popup)?$', re.I | re.M)
_regex_scheme = re.compile(r'^https?://', re.I)

_hosts_filters = [
    # Dan Pollock’s hosts file
    r'http://someonewhocares.org/hosts/hosts',
    # Peter Lowe’s Ad and tracking server list
    r'https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext',
    # MVPS HOSTS
    r'http://winhelp2002.mvps.org/hosts.txt',
    # Disconnect filters
    r'https://s3.amazonaws.com/lists.disconnect.me/simple_ad.txt',
    r'https://s3.amazonaws.com/lists.disconnect.me/simple_malvertising.txt',
    r'https://s3.amazonaws.com/lists.disconnect.me/simple_malware.txt',
    r'https://s3.amazonaws.com/lists.disconnect.me/simple_tracking.txt',
    # Spam404
    r'https://raw.githubusercontent.com/Dawsey21/Lists/master/main-blacklist.txt',
    # Malware Domain List
    r'https://www.malwaredomainlist.com/hostslist/hosts.txt',
    # Malware domains
    r'https://mirror.cedia.org.ec/malwaredomains/justdomains',
    # hpHosts’ Ad and tracking servers
    r'http://hosts-file.net/download/hosts.txt'
    ]

_adblock_filters = [
    # TUR: Adguard Turkish Filter
    r'https://filters.adtidy.org/extension/chromium/filters/13.txt',
    # Fanboy+Easylist-Merged Ultimate List
    r'https://www.fanboy.co.nz/r/fanboy-ultimate.txt',
    # EasyPrivacy
    r'https://easylist.to/easylist/easyprivacy.txt'
    # uBlock filters
    r'https://github.com/uBlockOrigin/uAssets/raw/master/filters/filters.txt',
    r'https://github.com/uBlockOrigin/uAssets/raw/master/filters/badware.txt',
    r'https://github.com/uBlockOrigin/uAssets/raw/master/filters/privacy.txt',
    # Fanboy’s Enhanced Tracking List
    r'https://www.fanboy.co.nz/enhancedstats.txt'
    ]

for _ in _hosts_filters:
    filter_ = requests.get(_)
    for domain in _regex_hosts.findall(filter_.text):
        _blacklist_pool.add(domain.lower())

for _ in _adblock_filters:
    filter_ = requests.get(_)
    for domain in _regex_adblock.findall(filter_.text):
        _blacklist_pool.add(domain.lower())

_ns_config_json['prefs']['untrusted'] = ' '.join(sorted(_blacklist_pool))

for entry in _ns_config_json['whitelist'].split():
    domain = _regex_scheme.sub('', entry)
    if domain not in _blacklist_pool:
        _whitelist_pool.append(entry)

_ns_config_json['whitelist'] = ' '.join(_whitelist_pool)

with open(os.path.join(os.path.dirname(_ns_config_path), 'noscript_nsbgen.json'), 'w') as _ns_config_file_new:
    json.dump(_ns_config_json, _ns_config_file_new, sort_keys=True, indent=4)

# print(json.dumps(_ns_config_json, sort_keys=True, indent=4))
