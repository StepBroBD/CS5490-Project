#!/bin/bash

set -eo pipefail

# start two running two commands, server first, wait 1 second, then client
# wait until client exits, then kill server

project start server --host 127.0.0.1 --port 8000 &
server_pid=$!

sleep 1

project start attack --host 127.0.0.1 --port 8000 --count $1 --save

client_exit_code=$?

kill $server_pid

exit $client_exit_code
