with open('bot_config') as cfg:
    name, secret, token, proxy = map(lambda s: s.rstrip(' \n'), cfg.readlines()[:4])

