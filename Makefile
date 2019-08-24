test:
	rm -f *test.db
	python database_test.py
	python source_test.py

install:
	cp hourlybot.service /lib/systemd/system/
	systemctl enable hourlybot.service

uninstall:
	systemctl disable hourlybot.service

start:
	systemctl start hourlybot.service

stop:
	systemctl stop hourlybot.service

status:
	systemctl status hourlybot.service

log:
	journalctl -r -u hourlybot.service

log-follow:
	journalctl -f -u hourlybot.service

.PHONY: test install start stop log log-follow status

