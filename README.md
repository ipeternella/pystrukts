<h1 align="center">Pystrukts!</h1>

<p align="center">
  <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
  <img alt="Quality Gate Status" src="https://sonarcloud.io/api/project_badges/measure?project=pystrukts&metric=alert_status">
  <img alt="Maintainability Rating" src="https://sonarcloud.io/api/project_badges/measure?project=pystrukts&metric=sqale_rating">
  <img alt="Security Rating" src="https://sonarcloud.io/api/project_badges/measure?project=pystrukts&metric=security_rating">
  <img alt="Reliability Rating" src="https://sonarcloud.io/api/project_badges/measure?project=pystrukts&metric=reliability_rating">
  <img alt="Coverage" src="https://sonarcloud.io/api/project_badges/measure?project=pystrukts&metric=coverage">
  <img alt="Bugs" src="https://sonarcloud.io/api/project_badges/measure?project=pystrukts&metric=bugs">
  <img alt="Technical Debt" src="https://sonarcloud.io/api/project_badges/measure?project=pystrukts&metric=sqale_index">
</p>

<p align="center">
  <img src="docs/pystrukts.png">
</p>

<h2 align="center">Some classical algorithms and data structures in pure Python.</h2>

## Table of Contents

- [Pystrukts](#pystrukts)
- [Running Tests with Sonar](#Running-tests-with-Sonar)

## Pystrukts

`Pystrukts` is a collection of classical algorithms and data structures implementations written in Python. It's main objective is to contain easy to understand algorithms so that anyone can use its implementations for studying.

## Running Tests with Sonar

This project supports running `sonarqube` analysis by creating docker local containers via `docker-compose` commands which execute the instructions on the [docker-compose.yml](docker-compose.yml) file.

- `sonar`: brings up the `sonarqube` server which is used for the code and code coverage analysis
- `sonar scanner`: container which contains the `sonar-scanner` cli
- `tests`: container which runs the projec tests

The first step is to bring up the `sonar` server:

```bash
docker-compose up sonar  # authenticate on localhost:9000 and create an auth token there
```

If it's the first time running the `sonar`, go to `http://localhost:9000` and use the credentials `admin:admin (user:password)` to login. Also, a token will be generated for authenticating with this local sonar server on later steps such as: `c11361e5ce0719a8be5249dcc329f31` (example). Write this token down for later steps.

After that, we should run the project tests or the sonar analysis will be incomplete. For that, run:

```bash
docker-compose up tests  # will generate, via volume mounts, coverage.xml and test-results.xml files
```

This will generate `coverage.xml` and `test-results.xml` files required by sonar. One **very important** thing is that the `coverage.xml` will contain the test paths using absolute paths like `/app/algorithms`. As a consequence, we must put all of our source code in an `/app` folder inside the `sonar_scanner` container. This is crucial for the `sonar_scanner` to be able to understand the coverage paths on the analysis. The following `docker-compose.yml` snippet shows this mechanism:

```yml
sonar_scanner:
  container_name: algorithms_sonar_scanner
  image: sonarsource/sonar-scanner-cli:latest
  environment:
    - SONAR_HOST_URL=http://sonar:9000
  working_dir: /app # this is the same /app folder in which the tests are run!
  volumes:
    - .:/app # coverage.xml results filepath must begin with '/app'
```

`PS`: if `pytest` runs with `--cov=.` option, the absolute path consideration with `/app` is not really required as `sonar_scanner` will just raise a `WARN` but will understand the `coverage.xml` in anyway. However, if the project runs pytest with the option `--cov=algorithm` (coverage of the src code folder only), which changes the `coverage.xml` file's absolute path, then if the `/app` convention is not followed, `sonar_scanner` will raise `ERROR` instead of warnings and will NOT perform any coverage analysis. In order to avoid such problems, we run pytest with `--cov=.` so that no errors are observed even if we locally run `start-tests.sh` to run tests.

As a final step, we run the sonar analysis by running the `sonar_scanner` service which will capture our source code via volumes and send to the sonar server. Now, we execute a `docker-compose run` command by passing the auth token that we noted in the previous steps, and that's it:

```bash
docker-compose run -e SONAR_LOGIN=c11361e5ce0719a8be5249dcc329f31 sonar_scanner  # change with your local auth token
```

Now, just navigate to `http://localhost:9000` (sonar server page) and check out your code quality!
