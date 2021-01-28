check_quality:
	@./scripts/quality.sh

make_messages:
	@./manage.py makemessages --ignore=.venv/* -l en --no-location

compile_messages:
	@./manage.py compilemessages

pre_commit:
	@ pre-commit

pre_commit_install:
	@ pre-commit install && pre-commit install --hook-type commit-msg

pre_commit_update:
	@ pre-commit autoupdate

