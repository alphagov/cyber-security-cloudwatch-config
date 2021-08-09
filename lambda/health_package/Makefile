.SHELL := /bin/sh
.DEFAULT_GOAL := zip
.PHONY = clean

clean:
	rm -rf __pycache__ .coverage *.zip *.egg-info .tox venv .pytest_cache htmlcov **/__pycache__ **/*.pyc .target setup.cfg

test: add_dev_deps
	tox

target_dir:
	rm -rf .target/
	mkdir .target
	mkdir .target/components

add_deps: target_dir
	bash -c "echo -e '[install]\nprefix=\n' > setup.cfg"; python3 -m pip install -r requirements.txt -t .target

add_dev_deps:
	python3 -m pip install -r requirements-dev.txt

copy_dir:
	cp *.py .target/
	cp *.json .target/
	cp components/*.py .target/components/

build: clean target_dir add_deps copy_dir

run: add_dev_deps
	python generate_metric_alarms.py

zip: build
	cd .target; zip -X -9 ../health_package.zip -r .
