.PHONY: install
install:
	sh ./tools/install_project.sh

.PHONY: reset_db
reset_db:
	python -m data_api.reset_db

.PHONY: run
run:
	python -m data_api.app