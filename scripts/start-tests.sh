#!/bin/bash
SRC_PROJECT_PATH=algorithms
TESTS_PROJECT_PATH=tests

echo "Running pytest and generating xml coverage report..."
pytest $TESTS_PROJECT_PATH \
    --cov=$SRC_PROJECT_PATH \
    --cov-report xml \
    --cov-report term \
    --junitxml=test-results.xml