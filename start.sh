#!/bin/bash

trap "kill 0" EXIT

node --experimental-modules danmu-server.mjs &
sleep 1s

python3 discord-bot.py &
python3 telegram-bot.py &

wait
