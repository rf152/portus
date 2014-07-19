import logging;
import config;

def get(name):
	fmt = '%(asctime)-15s [%(levelname)s] %(message)s';
	datefmt = '%Y-%m-%d %H:%M:%S';
	try:
		level = config.get('core', 'loglevel');
	except:
		level = "info";
	try:
		intlevel = int(level);
	except ValueError:
		if level.lower() == "debug":
			intlevel = logging.DEBUG;
		elif level.lower() == "info":
			intlevel = logging.INFO;
		elif level.lower() == "warning":
			intlevel = logging.WARNING;
		elif level.lower() == "error":
			intlevel = logging.ERROR;
		elif level.lower() == "critical":
			intlevel = logging.CRITICAL;
		else:
			intlevel = logging.INFO;
	
	logging.basicConfig(
		format=fmt,
		datefmt=datefmt,
		filename="/opt/portus/log/portus.log",
		level=intlevel
	);
	return logging.getLogger(name);
