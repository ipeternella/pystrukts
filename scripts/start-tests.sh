#!/bin/bash
COVER_PROJECT_PATH=.
TESTS_PROJECT_PATH=tests

# covers whole project: this avoids errors when running sonar anaylsis
# due to different absolute filepaths and we filter unwanted dirs with sonar.properties later
echo "Running pytest and generating xml coverage report..."
pytest $TESTS_PROJECT_PATH \
    --cov=$COVER_PROJECT_PATH \
    --cov-report xml \
    --cov-report term \
    --junitxml=test-results.xml