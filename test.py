import requests
import re
import json

# Configurable variables #
##########################
HOST = '192.168.0.1'
USER = 'admin'
PASSWORD = 'qq1357900'
##########################

ROW_LENGTH = 13
r = requests.get('http://{}/userRpm/SystemStatisticRpm.htm'.format(HOST) +
                 '?interval=10&sortType=5&Num_per_page=10&Goto_page=1',
                 auth=(USER, PASSWORD))

print r.text

match = re.search(r'var statList = new Array\((.*?)\);', r.text, re.DOTALL)
table = match.group(1)   # get content inside parentheses
table = table.replace('\n', ' ').split(',')
parsed = []
for x in table:
    x = x.strip()
    parsed_x = (
        x[1:-1] if len(x) >= 2 and x[0] == '"' and x[-1] == '"'
        else int(x))
    parsed.append(parsed_x)

rows = []
i = 0
while i < len(parsed):
    new_row = parsed[i:i + ROW_LENGTH]
    if len(new_row) == ROW_LENGTH:
        rows.append(new_row)
    i += ROW_LENGTH

records = []
for row in rows:
    record = {}
    record['index'] = row[0]
    record['ip'] = row[1]
    record['mac'] = row[2]
    record['total_packets'] = row[3]
    record['total_bytes'] = row[4]
    record['current_packets'] = row[5]
    record['current_bytes'] = row[6]
    record['icmp'] = {'current_rate': row[7], 'max_rate': row[8]}
    record['udp'] = {'current_rate': row[9], 'max_rate': row[10]}
    record['syn'] = {'current_rate': row[11], 'max_rate': row[12]}
    records.append(record)

print(json.dumps(records, indent=4, separators=(',', ': ')))