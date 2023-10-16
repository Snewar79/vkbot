import yaml
import os

cfg_path = os.environ.get("CONFIG_PATH", "/usr/local/vkbot/etc/config.yaml.sample")

if not cfg_path or not os.path.exists(cfg_path):
    raise Exception('Not specified correct config file path, '
                    'or file not exists')


def parse_config(filepath):
    try:
        tmp = open(filepath, 'r')
        config = yaml.safe_load(tmp)
        return config
    except IOError as e:
        raise Exception('config file not found: "%s", error: %s' %
                        (filepath, str(e)))

config = parse_config(cfg_path)
