setup:
	@pip install -e .[tests]

compile_ext:
	@python setup.py build_ext -i

f ?= "vows/"
test pyvows: compile_ext
	@pyvows -vv --profile --cover --cover-package=thumbor_plugins --cover-threshold=90 $f
	@nosetests -sv

ci_test: compile_ext
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	@echo "TORNADO IS `python -c 'import tornado; import inspect; print(inspect.getfile(tornado))'`"
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"

	@pyvows -vvv --profile --cover --cover-package=thumbor_plugins --cover-threshold=90 vows/

install:
	@pip install install https://github.com/thumbor/thumbor-plugins/archive/master.zip

test_gifv:
	@docker build -t gifv -f thumbor_plugins/optimizers/gifv/tests/docker/Dockerfile .
	docker run --rm -v$(CURDIR):/app gifv /bin/bash -c "pip install -e .[tests,gifv] && pytest thumbor_plugins/optimizers/gifv/tests"

test_mozjpeg:
	@docker build -t mozjpeg -f thumbor_plugins/optimizers/mozjpeg/tests/docker/Dockerfile .
	docker run --rm -v$(CURDIR):/app mozjpeg /bin/bash -c "pip install -e .[tests,mozjpeg] && pytest thumbor_plugins/optimizers/mozjpeg/tests"

test_unit:
	pytest -s `find . -type d -name 'unit' | tr "\n" " "`
