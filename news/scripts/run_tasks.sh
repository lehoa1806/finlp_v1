#!/usr/bin/env bash

# external sources
source "${HOME}"/finlp/common/common.sh


### Main:
eligible_options=("--headless" "--help")
if [[ ${#} -gt 0 ]]; then
  check_eligible_options "${@}"
fi

cmd="python3 -m news.scripts.run_tasks"

case "${1}" in
  "--headless")
    cmd+=" --headless"
    ;;
  "--help")
    echo "Script to scrape news and announcements"
    echo "[--headless]: run in headless mode"
    exit 0
    ;;
  *)
    ;;
esac

setup_git
export PYTHONPATH="${HOME}/finlp/"
log "Run ${cmd}"
eval "${cmd}"
