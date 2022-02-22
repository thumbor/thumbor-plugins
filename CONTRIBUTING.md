## Steps

There are a few things you'll need to start hacking on it properly.

1. [Fork it](http://help.github.com/fork-a-repo/)
2. Install dependencies and initialize the environment
3. Hack, in no particular order:
   - Write enough code
   - Write tests for that code
   - Check that other tests pass
   - Repeat until you're satisfied
4. Submit a pull request

## Install dependencies
To run the tests, you will only need [Docker](https://www.docker.com/).

## Creating a new optimizer
Each folder in [optimizers](https://github.com/thumbor/thumbor-plugins/tree/master/thumbor_plugins/optimizers)
is a separate package.
You can copy an existing optimizer and rename it to create a new one.
You will find a [Dockerfile](https://github.com/thumbor/thumbor-plugins/blob/master/thumbor_plugins/optimizers/gifv/tests/docker/Dockerfile) 
on each of them that will be used when running the integration test.

## Running the tests
Imagine that you just created a new optimizer named `doge`,
then to test it, you need to run `make test_doge`.

## How should my commits look like?
This project is using [release-please](https://github.com/googleapis/release-please)
to manage all the packages.
So make sure that your commits are following the [Conventional commits message](https://www.conventionalcommits.org/en/v1.0.0/#summary)

