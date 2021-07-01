#!/bin/bash -e

opts=(-r -m home --rebuild-index)
while [[ $1 = -* ]] ; do
	opts=("${opts[@]}" "$1")
	shift
done

if [[ $# -eq 0 ]] ; then
	echo "Usage: $0 [spack buildcache create options] SPECS .."
	echo "Convenience wrapper for 'spack buildcache create ${opts[@]}'"
	echo "You may often need to add -a."
	exit 1
fi

pkgs=$(spack find --format "{name}@{version}/{hash:7}" "$@")

set -- $pkgs
# must be an easier way...
root=$(spack find --format "{spack_install}" "$1" | head -1)
if [[ ${#root} -ne 32 ]] ; then
	echo "Your install tree root must be padded to 32 characters."
	exit 1
fi

echo "Caching packages:"
echo "$pkgs"
echo spack buildcache create "${opts[@]}" "$@"
exec spack buildcache create "${opts[@]}" "$@"
