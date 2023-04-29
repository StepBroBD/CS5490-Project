# CS5490 Project

CS 5490 Spring 2023 @ The University of Utah

Gates Lamb u1033920@utah.edu

Sam Smith u0629883@utah.edu

Yifei Sun u1298569@utah.edu

## Development Guide

1. Use `virtualenv`:

   ```shell
   pip install virtualenv
   virtualenv venv
   . venv/bin/activate
   ```

2. Lock dependencies:

   ```shell
   pip list --format freeze >requirements.txt
   ```

3. Reproduce dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Editable install:

   ```shell
   pip install -e . # then you can run the project with `project`
   ```

## Evaluation

To run an evaluation, start server first:

```shell
project start server --host 127.0.0.1 --port 8000
```

Then start client:

```shell
project start attack --host 127.0.0.1 --port 8000 --count 1000 --save
```

To get enough data for each evaluation, we've the traffic lower bound to be 1000, use the `--save` flag to save the run result to `./result` folder.

Or, simply run:

```shell
./scripts/test.sh 2500
```

To run an evaluation with 2500 traffic load.

If you are lazy, you can also start run multiple evaluations at once:

```shell
for i in {1..10}; do
 scripts/test.sh 2500; sleep 60;
done
```

Please make sure to let the system sleep for a while before running next session, our evaluation script will consume a large number of ports, the additional time is for the system scheduler to clean up the run.

## Resources

- [Python Socket Server](https://docs.python.org/3/library/socketserver.html)
- [Click](https://click.palletsprojects.com/en/latest/)
- [Click Option Group](https://click-option-group.readthedocs.io/en/latest/)
