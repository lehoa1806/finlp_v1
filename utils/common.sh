#!/usr/bin/env bash


# Write log with INFO tag
# Usage: log <message>
# - message: logging string
function log() {
  logger -p user.info "INFO: ${*}"
  echo "INFO: ${*}" 2>&1
}


# Write log with ERROR tag
# Usage: error <message>
# - message: logging string
function error() {
  logger -p user.info "ERROR: ${*}"
  echo "ERROR: ${*}" 2>&1
}


# validate the script's arguments
# Usage: set eligible_options before triggering this function
# - eligible_options: a list of eligible arguments
function check_eligible_options() {
  local _found=0
  for _elopt in "${eligible_options[@]}"; do
    case ${1} in
      "${_elopt}")
        _found=1
        break
        ;;
    esac
  done
  if [[ ${_found} -eq 0 ]]; then
    echo "Option ${1} is not supported. Try help for more information."
    error "Option ${1} is not supported. Try help for more information."
    exit 1
  fi
}


# pull new commits and do other configs
function setup_git() {
  log "Git setup starts ..."
  cd "${HOME}/finlp/" || exit 1
  log "Git clean ..."
  git clean -fxd
  log "Git reset ..."
  git reset --hard
  log "Git pull ..."
  git pull --all
  log "Git pull submodules..."
  git submodule update --init --recursive --jobs 5
  git pull --recurse-submodules
  log "Git apply patchs..."
  for patch in "${HOME}/finlp/deploy/patchs"/*
  do
    if [[ "${patch}" == *"0002"*  ]]; then
      continue
    fi
    log "Applying ${patch} ..."
    git apply "${patch}"
  done
  log "Git setup is done ..."
}
