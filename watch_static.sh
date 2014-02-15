coffee --watch --compile cashout/core/static/scripts/ &
sass --watch cashout/core/static/stylesheets/ &
read
trap 'kill $(jobs -p)' EXIT
