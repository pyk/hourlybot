test:
	rm -f *test.db
	python database_test.py

.PHONY: test
