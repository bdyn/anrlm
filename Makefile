PROJECT = leaguemanager
DEFAULT_DJANGO_SETTINGS = ${PROJECT}.settings

# Use binaries in the virtual environment.
VIRTUALENV = .virtualenv
BIN = ${VIRTUALENV}/bin
PYTHON = ${BIN}/python
PIP = ${BIN}/pip
MANAGE = ${PYTHON} manage.py

# Dependency-related.
PIP_CACHE = ~/.pip_cache
WHEEL_CACHE = ~/.wheel_cache
PIP_INSTALL = ${PIP} install --download-cache ${PIP_CACHE}
REQS_PROD = requirements/base.txt
REQS_DEV = requirements/dev.txt

virtualenv:
	virtualenv ${VIRTUALENV}

hooks:
	githooks/update_githooks.sh

pip:
	${PIP_INSTALL} --upgrade pip wheel

reqs-prod: ${REQS_PROD} pip
	$(foreach reqs,${REQS_PROD}, ${PIP_INSTALL} -r ${reqs};)

reqs-dev: ${REQS_DEV}
	$(foreach reqs,${REQS_DEV}, ${PIP_INSTALL} -r ${reqs};)

reqs: reqs-prod reqs-dev

bootstrap-prod: virtualenv reqs-prod

bootstrap: bootstrap-prod reqs-dev hooks

clean:
	# Delete all .pyc and .pyo files.
	find . \( -name "*~" -o -name "*.py[co]" -o -name ".#*" -o -name "#*#" \) -exec rm '{}' +

lint: clean
	${BIN}/flake8 --config=setup.cfg ${PROJECT}
	${BIN}/pylint --rcfile=pylint.rc ${PROJECT}

test: clean
	${MANAGE} test

shell: SETTINGS = ${DEFAULT_DJANGO_SETTINGS}
shell:
	${MANAGE} shell --settings=${SETTINGS}

dbshell: SETTINGS = ${DEFAULT_DJANGO_SETTINGS}
dbshell:
	${MANAGE} dbshell --settings=${SETTINGS}
