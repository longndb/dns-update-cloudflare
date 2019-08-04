import requests as rq
import sys
import json

domain = ''
ip = rq.get('http://ipconfig.io/ip').text.split('\n')[0]
url = r'https://api.cloudflare.com/client/v4/zones/'
headers = {'X-Auth-Email': None, 'X-Auth-Key': None, 'Content-Type': 'application/json'}
data = {'type': 'A', 'name': None, 'content': None}

if len(sys.argv) == 4:
    headers['X-Auth-Email'] = sys.argv[1]
    headers['X-Auth-Key'] = sys.argv[2]
    domain = sys.argv[3]
    data['name'] = domain
    data['content'] = ip
else:
    print("Usage: {} <email> <api token> <domain>".format(sys.argv[0]))
    sys.exit(1)

request = rq.get(url=url, headers=headers)

if request.status_code != 200:
    for err in request.json()['errors']:
        print(err['message'])
        sys.exit(1)
else:
    result = json.loads(request.text)['result']

    for each in result:
        if not each['name'] in domain:
            continue
        request = rq.get(url=url+r'/'+str(each['id'])+r'/dns_records', headers=headers)
        for dm in json.loads(request.text)['result']:
            if not dm['name'] == domain:
                continue
            request = rq.put(url=url + r'/' + str(each['id']) + r'/dns_records/' + str(dm['id']), data=json.dumps(data)
                             , headers=headers)
            if request.status_code == 200:
                print("Update DNS record successfully")
                sys.exit(1)
    else:
        print("The domain can not be found")