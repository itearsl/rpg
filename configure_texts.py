
import configparser


def createConfig(path):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("Config")
    config.set("Config", "Terrain", "Вы пришли в {}")
    config.set("Config", "attack", "Вас атаковал {} на {}")
    config.set("Config", "hp", "Здоровье: {}/{} ")
    #config.set("Config","")
    with open(path, "w") as config_file:
        config.write(config_file)


def Terrain(terr):
    return (config.get("Config",'Terrain')).format(terr)

def Attack(monster,damage):

    return (config.get("Config",'attack')).format(monster,damage)

def hp(now,max):
    return (config.get("Config",'hp')).format(now,max)


if __name__ == "__main__":
    path = "settings.ini"
    createConfig(path)
    config = configparser.ConfigParser()
    config.read(path)
    Attack('ok','q')
    print(hp(100,1000))