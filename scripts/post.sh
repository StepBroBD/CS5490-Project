#!/bin/bash

set -eo pipefail

authority=$(echo $1 | sed -E 's/https?:\/\/([^\/]+)\/.*/\1/')

curl $1 \
	-H 'authority: '$authority \
	-H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7' \
	-H 'accept-language: en-US,en;q=0.9' \
	-H 'cache-control: max-age=0' \
	-H 'dnt: 1' \
	-H 'sec-ch-ua: "Not:A-Brand";v="99", "Chromium";v="112"' \
	-H 'sec-ch-ua-platform: "macOS"' \
	-H 'sec-fetch-dest: document' \
	-H 'sec-fetch-mode: navigate' \
	-H 'sec-fetch-site: same-origin' \
	-H 'sec-fetch-user: ?1' \
	-H 'upgrade-insecure-requests: 1' \
	-H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36' \
	-H 'Content-Type: application/json' \
	-d '{"name": "test", "description": "test", "price": 1, "category": "test", "image": "test"}'
