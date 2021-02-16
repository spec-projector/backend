generate_graphql_schema:
	@./manage.py graphql_schema --schema server.gql.schema --out tests/schema.graphql

lint:
	@./scripts/lint.sh

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

