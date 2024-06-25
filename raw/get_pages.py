import os

import requests

DIR = 'api'


def get_pages(url: str):
    endpoint = url.rsplit('/', 1)[1]
    page = 1
    while True:
        filename_base = endpoint + '_' + str(page)
        print(url, page)
        response = requests.get(url, params={'page': page})
        assert response.status_code == 200
        with open(os.path.join(DIR, filename_base+'.json'), 'wb') as f:
            f.write(response.content)
        data = response.json()
        items = set()
        for d in data['data'][endpoint]:
            items.add('user:'+d['user_id'])
            items.add('cdn:'+d['thumbnail'].split('/', 2)[2])
            if d['user'] is not None:
                items.add('{}:{}:{}'.format(endpoint[:-1], d['user']['user_name'], d['id']))
        with open(os.path.join(DIR, filename_base+'_item.txt'), 'w') as f:
            f.write('\n'.join(items)+'\n')
        if len(data['data'][endpoint]) > 0:
            page += 1
            continue
        break


def main():
    if not os.path.isdir(DIR):
        os.makedirs(DIR)
    get_pages('https://picdig.net/api/v2/projects')
    get_pages('https://picdig.net/api/v2/articles')

if __name__ == '__main__':
    main()

