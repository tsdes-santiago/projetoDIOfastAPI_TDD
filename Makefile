run:
	@uvicorn store.main:app --reload

test:
	@pipenv run pytest

test-matching:
	@pipenv run pytest -s -rx -k $(K) --pdb store ./tests/
