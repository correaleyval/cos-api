import markdown
import re
import json
import requests

def getdata():
    file = open("lista.md")
    # file = requests.get('https://raw.githubusercontent.com/cuban-opensourcers/cuban-opensource/master/README.md')

    body = file.read()
    # body = file.text

    html = markdown.markdown(body, output_format='html')
    links = list(set(re.findall(r'href=[\'"]?([^\'" >]+)', html)))
    links = list(filter(lambda l: l[0] != "{", links))

    data = dict()

    for l in links:
        s = l.split('/')

        try:
            if s[2] == 'github.com':
                try:
                    data[s[3]].append(s[4])
                except KeyError:
                    data[s[3]] = list()
                    data[s[3]].append(s[4])

        except IndexError:
            pass

    data_json = list()

    for user in data:
        user_dict = dict()
        user_dict['name'] = user
        user_dict['repos'] = data[user]
        data_json.append(user_dict)

    return data_json

# file_data = open("data.json", 'w')

# file_data.write(json_string)
# file_data.close()
