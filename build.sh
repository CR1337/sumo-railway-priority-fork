#!/bin/sh
export SUMO_HOME="$PWD"
mkdir build/cmake-build
cd build/cmake-build
cmake ../..
make -j$(nproc)