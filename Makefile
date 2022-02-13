setup:
	@pip install -e .[tests]

test_%:
	@docker build -t $* -f thumbor_plugins/optimizers/$*/tests/docker/Dockerfile .
	docker run --rm -v$(CURDIR):/app $* /bin/bash -c "pip install -r test_requirements.txt && pip install -e thumbor_plugins/optimizers/$* && pytest --cov=thumbor_plugins.optimizers.$* thumbor_plugins/optimizers/$*/tests"

test_unit:
	pytest -s `find . -type d -name 'unit' | tr "\n" " "`
