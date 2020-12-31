#!/bin/bash
SRC_PROJECT_PATH=algorithms
TESTS_PROJECT_PATH=tests/

echo "Running pytest and generating xml coverage report..."
pytest --cov=$SRC_PROJECT_PATH --cov-report xml --cov-report term $TESTS_PROJECT_PATH