winid=$(xprop -root | awk '/_NET_ACTIVE_WINDOW\(WINDOW\)/{print $NF}')
#winid=$(xdpyinfo | grep focus | grep -E -o 0x[0-9a-f]+)
d=$(xprop -id $winid | awk '/_NET_WM_PID\(CARDINAL\)/{print $NF}')
#r=$(cat /proc/$d/cmdline)
r=$(ps -o command -p $d --no-heading)
title=$(xwininfo -id $winid|awk 'BEGIN {FS="\""}/xwininfo: Window id/{print $2}' | sed 's/-[^-]*$//g')
echo "$title||$r"
