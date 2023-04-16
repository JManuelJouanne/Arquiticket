lint:
	source ./venv/bin/activate; \
	autopep8 ./api --recursive --in-place; \
	autopep8 ./subscriber --recursive --in-place;
