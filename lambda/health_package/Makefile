.SHELL := /bin/sh
.DEFAULT_GOAL := zip
.PHONY = clean

clean:
	rm -rf __pycache__ .coverage *.zip *.egg-info .tox venv .pytest_cache htmlcov **/__pycache__ **/*.pyc .target setup.cfg

test:
	rm setup.cfg; tox

target_dir:
	rm -rf .target/
	mkdir .target
	mkdir .target/components

add_deps: target_dir
	bash -c "echo -e '[install]\nprefix=\n' > setup.cfg"; python3 -m pip install -r requirements.txt -t .target

copy_dir:
	cp *.py .target/
	cp components/*.py .target/components/

build: clean target_dir add_deps copy_dir

run:
	python generate_metric_alarms.py

zip: build
	cd .target; zip -X -9 ../health_package.zip -r .
