# config.py
import ConfigParser

path = 'config.ini'

def read(a,b):
    cf = ConfigParser.ConfigParser()
    cf.read(path)
    return cf.get(a,b)
