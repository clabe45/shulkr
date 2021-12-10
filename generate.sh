#!/usr/bin/bash

if [ "$#" -eq 0 ]
then
	echo "Usage: ./gen-sources.sh MAPPINGS_VERSION1 [MAPPINGS_VERSION2 [...]]"
	exit 1
fi

function gen_sources {
	local mappings_version=$1

	# The minecraft version is the substring of the mappings version before the '+
	local tokens=(${mappings_version//+/ })
	local minecraft_version=${tokens[0]}

	# Clear loom cache
	if [ -d ~/.gradle/caches/fabric-loom ]
	then
		rm -r ~/.gradle/caches/fabric-loom
	fi

	cd fabric-example-mod
	sed -i -e "s/\tminecraft_version=.*/\tminecraft_version=$minecraft_version/" gradle.properties
	sed -i -e "s/\tyarn_mappings=.*/\tyarn_mappings=$mappings_version/" gradle.properties
	gradle genSources

	cd ..
	local src_jar="$(find ~/.gradle/caches/fabric-loom/* -maxdepth 0 | head -n 1)"
	rm -r src
	mkdir src
	unzip "$src_jar/*-sources.jar" -d src

	git add src

	# Clean working directory of fabric-example-mod submodule
	cd fabric-example-mod
	git reset --hard HEAD
	cd ..

	git commit -m "version $minecraft_version"
}

for mappings_version in "$@"
do
	gen_sources $mappings_version
done
