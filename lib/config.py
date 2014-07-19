import sys;
if sys.version_info < (3, 0):
	import ConfigParser;
	config = ConfigParser.ConfigParser();
else:
	import configparser;
	config = configparser.ConfigParser();

config.read(['/opt/portus/conf/portus.conf']);


def get(section, option):
	return config.get(section, option);

def getint(section, option):
	return config.getint(section, option);

def getfloat(section, option):
	return config.getfloat(section, option);

def getboolean(section, option):
	return config.getboolean(section, option);

def items(section):
	return config.items(section);
