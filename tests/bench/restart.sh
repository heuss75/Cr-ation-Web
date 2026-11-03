#!/bin/bash
cd "$(dirname "$0")"
[ -f server.pid ] && kill "$(cat server.pid)" 2>/dev/null
sleep 1
REPO_DIR=/home/claude/heuss75/cr-ation-web WORKER_PATH=$PWD/worker.mjs PORT=8787 nohup node --no-warnings devserver.mjs > server.log 2>&1 &
echo $! > server.pid
sleep 3; cat server.log
