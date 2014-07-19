import log
import db;
import serial;
import re;
import subprocess;
import config;


def run():
	logger = log.get("core");
	logger.info("Starting up");
	
	db.load_schema();
	
	portname = config.get('core', 'serialport');
	logger.debug("Opening Serial: {}".format(portname));
	try:
		port = serial.Serial(
			portname,
			baudrate=9600,
			timeout=2,
		);
	except serial.SerialException as e:
		logger.error("Could not open serial port {}".format(portname));
		exit(1);
	
	logger.debug("Checking for GPS device");
	# Check whether there is a GPS device on this serial port
	line = port.readline();
	if line.strip() == '':
		# There doesn't appear to be a GPS device on this port (or anything)
		logger.error("No GPS Device found on serial port %s" % portname);
		exit(1);
	
	logger.debug("Waiting for GPRMC");
	while line[1:6] != 'GPRMC':
		line = port.readline().strip().decode("utf-8");
		#print(line[1:6]);
	
	logger.debug("Got GPRMC");
	
	pattern = '[A-Z]+,([0-9]{6}),[A-Z],[0-9\.]+,[A-Z],[0-9\.]+,[A-Z],[0-9\.]+,[0-9\.]+,([0-9]{6}).*';
	
	m = re.search(pattern, line);
	
	d = m.group(2);
	t = m.group(1);
	dt = d[2:4] + d[0:2] + t[0:4] + d[4:] + '.' + t[4:];
	
	logger.debug("Setting date: " + dt);
	nl = open("/dev/null", "w");
	subprocess.call(["sudo", "/bin/date",  '-u',  dt],stdout=nl);
	
	# Now need to output status to status file
	statusfile = config.get('core', 'statusfile');
	fh = open(statusfile, 'w');
	fh.write('running');
	fh.close();

	# Prepare the regular expressions
#	ggapattern = '[A-Z]+,([0-9]{6}),([0-9\.]+),([A-Z]),([0-9\.]+),([A-Z]),([0-2]),([0-9]{2}),([0-9\.]+),([0-9\.]+),([0-9\.]+)';
	ggapattern = '\$GPGGA,([0-9]{6}),([0-9\.]+),([NS]),([0-9\.]+),([EW]),([0-2]),([0-9]{2}),([0-9\.]+),([\-]?[0-9]+\.[0-9]),M,([\-]?[0-9]+\.[0-9])';
	ggare = re.compile(ggapattern);
	
	while True:
		text = port.readline();
		text = text.strip().decode("utf-8");
		
		if text[0] != '$':
			# Caught an incomplete line
			continue;
		
		sentence = text[1:6];
		
		if sentence == 'GPGGA':
			# Positional data
			try:
				matches = ggare.search(text);
			except AttributeError:
				# Invalid data
				continue;
			parts = matches.groups();
			db.cursor.execute('INSERT INTO points VALUES (?,?,?,?,?,?,?,?,?,?)', parts);
			db.connection.commit();
#		print(sentence);
	#	print(text.strip());

