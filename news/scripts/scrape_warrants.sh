#!/usr/bin/env bash

# external sources
source "${HOME}"/finlp/utils/common.sh


### Main:
eligible_options=("--cool-down" "--break-period" "--headless" "--help")
if [[ ${#} -gt 0 ]]; then
  check_eligible_options "${@}"
fi

cmd="python3 -m news.scripts.scrape_warrants"

until [ "$#" == "0" ]; do
  case "${1}" in
    "--cool-down")
      shift 1
      cmd+=" --cool-down $1"
      shift 1
      ;;
    "--break-period")
      shift 1
      cmd+=" --break-period $1"
      shift 1
      ;;
    "--headless")
      shift 1
      cmd+=" --headless"
      ;;
    "--help")
      echo "Script to scrape VN warrants"
      echo "[--headless]: run in headless mode"
      echo "[--cool-down]: cool-down period"
      echo "[--break-period]: break period"
      exit 0
      ;;
    *)
      ;;
  esac
done

# setup_git
export PYTHONPATH="${HOME}/finlp/"
log "Run ${cmd}"
echo "Run ${cmd}"
eval "${cmd}"
