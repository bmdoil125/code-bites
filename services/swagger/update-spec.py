import os
import sys
import yaml
import io

def update_yaml_file(url):
    full_path = os.path.abspath('swagger.yaml')
    with io.open(full_path, 'r') as file:
        data = yaml.safe_load(file)
    data['servers'][0]['url'] = url
    with io.open(full_path, 'w', encoding='utf8') as file:
        yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
    return True


if __name__ == '__main__':
    try:
        update_yaml_file(sys.argv[1])
    except IndexError:
        print('Please provide a URL.')
        print('USAGE: python update-spec.py URL')
        sys.exit()