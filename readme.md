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
