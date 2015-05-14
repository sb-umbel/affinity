clean:
	find . -name "*.pyc" -exec rm -rf {} \;


lint:
	flake8 --exclude=migrations --ignore=E501,E225,E121,E123,E124,E125,E127,E128 affinity


check:
	python manage.py check --settings=tests.settings


coverage: clean lint check
	coverage run --source=affinity --omit="*/migrations/*" --branch manage.py test --settings=tests.settings
	coverage html


test: clean lint check
	python manage.py test --settings=tests.settings


test-fast: clean lint check
	python manage.py test --settings=tests.settings --failfast
