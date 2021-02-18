import os
import json

if __name__ == '__main__':
    f = open('coverage/codeclimate.json', 'r')
    summary = json.load(f)
    f.close()
    for i in range(len(summary['source_files'])):
        if summary['source_files'][i]['name'][0] == '/':
            path = summary['source_files'][i]['name'].replace('//', '/')
            fields = path.split(os.sep)
            local = list(fields)
            for field in fields:
                if field == 'Dtect':
                    break
                local.remove(field)
            new_name = os.path.join(*local)
            summary['source_files'][i]['name'] = new_name
    f = open('coverage/codeclimate.json', 'w')
    json.dump(summary, f)
