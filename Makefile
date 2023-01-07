.PHONY: install
install:
	sh ./tools/install_project.sh

.PHONY: reset_db
reset_db:
	python ./tools/reset_db.py

.PHONY: run
run:
	python -m data_api.app