# Required executables
ifeq (, $(shell which python3))
 $(error "No python3 on PATH.")
endif
ifeq (, $(shell which pipenv))
 $(error "No pipenv on PATH.")
endif

# Suppress warning if pipenv is started inside .venv
export PIPENV_VERBOSITY=1
# Use relative .venv folder instead of home-folder based
export PIPENV_VENV_IN_PROJECT=1
# Ignore existing venvs (required for travis)
export PIPENV_IGNORE_VIRTUALENVS=1
# Setup python path
export PYTHONPATH=.
# Make sure we are running with an explicit encoding
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
# Current package version
VERSION=$(shell python3 setup.py --version)
# Default my_module flask port
PORT_NUMBER=22174
# Default project docker image and container names
CONTAINER_NAME="python3-flask-boilerplate"
IMAGE_NAME="bastiteehome/python3-flask-boilerplate"

all: clean venv build dockerbuild

venv: clean
	@echo Initialize virtualenv, i.e., install required packages etc.
	pipenv --three install --dev

shell:
	@echo Initialize virtualenv and open a new shell using it
	pipenv shell

clean:
	@echo Clean project base
	rm -rfv .venv .tox .egg build dist src
	find . -type d -name ".ropeproject" -exec rm -rf "{}" +;
	find . -type d -name ".pytest_cache" -exec rm -rf "{}" +;
	find . -type d -name "__pycache__" -exec rm -rf "{}" +;

test:
	@echo Run all tests in default virtualenv
	pipenv run py.test tests

testall:
	@echo Run all tests against all virtualenvs defined in tox.ini
	pipenv run tox -c setup.cfg tests

coverage:
	@echo Run test coverage checks
	pipenv run py.test --verbose tests

isort:
	@echo Check for incorrectly sorted imports
	pipenv run isort --check-only .

lint:
	@echo Run code formatting checks against source code base
	pipenv run flake8 my_module tests

build: test coverage isort lint
	@echo Run setup.py-based build process to package application
	pipenv run python setup.py bdist_wheel

publish: all
	@echo Release to pypi.org and create git tag
	pipenv run twine upload dist/*
	git tag -a $(VERSION) -m "Version $(VERSION)"
	git push --tags

dockerbuild:
	@echo Run full build toolchain and create a docker image for publishing
	docker build -t $(IMAGE_NAME) . || exit 1

dockerrun: dockerbuild
	@echo Run docker build process and run a new container using the latest
	mkdir -vp ~/.python3-flask-boilerplate
	docker run --rm --interactive --tty \
	--volume ~/.python3-flask-boilerplate:/instance \
	--publish $(PORT_NUMBER):80 \
	--name $(CONTAINER_NAME) \
	$(IMAGE_NAME)

dockerpush: dockerbuild
	@echo Push docker image to dockerhub. Expects docker login available
	docker push $(IMAGE_NAME)

run:
	@echo Execute my_module directly
	FLASK_APP=my_module FLASK_DEBUG=1 pipenv run \
    flask run --host 0.0.0.0 --port $(PORT_NUMBER)

initdb:
	@echo Execute my_module directly
	FLASK_APP=my_module FLASK_DEBUG=1 pipenv run flask init-db

fetch-latest-boilerplate:
	@echo Fetch latest python3-boilerplate version from github
	git remote add py3template git@github.com:BastiTee/python3-boilerplate.git \
	||true
	git pull py3template master --allow-unrelated-histories ||true
	@echo ----------------------------------------------------
	@echo Resolve all merge conflicts and commit your changes!
	@echo ----------------------------------------------------
