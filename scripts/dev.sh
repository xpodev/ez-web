#!/bin/bash

# Parse command-line arguments
while [ $# -gt 0 ]; do
  case "$1" in
    --sitedir)
      shift
      sitedir="$1"
      ;;
    --port)
      shift
      port="${1:-8000}"
      ;;
    --hostname)
      shift
      hostname="${1:-localhost}"
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
  shift
done

# Mandatory parameter check
if [ -z "$sitedir" ]; then
  echo "Missing mandatory parameter: --sitedir"
  exit 1
fi

# Resolve path for sitedir
sitedir=$(realpath "$sitedir")

# Set environment variables
root="$(dirname "$(dirname "$0")")"
export EZ_PYTHONPATH="$root/core:$sitedir/lib/dependencies"

# Build and execute the command
command="$root/lib/python/python $root/core/main.py $sitedir --port $port --host $hostname"
echo "$command"
(cd "$sitedir" && eval "$command")
