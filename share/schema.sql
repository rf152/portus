CREATE TABLE IF NOT EXISTS points (
	time text,
	lat real,
	lathem text,
	lon real,
	lonhem text,
	qual integer,
	numsats integer,
	hdop real,
	height real,
	gheight real
);

CREATE TABLE IF NOT EXISTS transits (
	time text,
	speed real,
	course real,
	magvar real,
	magvardir text
);
