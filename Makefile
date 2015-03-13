setup:
	@pip install -e .[tests]

f ?= "vows/"
test pyvows:
	@pyvows -vv --profile --cover --cover-package=thumbor_plugins --cover-threshold=90 $f

ci_test: compile_ext
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	@echo "TORNADO IS `python -c 'import tornado; import inspect; print(inspect.getfile(tornado))'`"
	@echo "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	$(MAKE) mongo redis
	@pyvows -vvv --profile --cover --cover-package=thumbor_plugins --cover-threshold=90 vows/
