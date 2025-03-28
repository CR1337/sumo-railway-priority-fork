#!/bin/bash
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2008-2022 German Aerospace Center (DLR) and others.
# This program and the accompanying materials are made available under the
# terms of the Eclipse Public License 2.0 which is available at
# https://www.eclipse.org/legal/epl-2.0/
# This Source Code may also be made available under the following Secondary
# Licenses when the conditions for such availability set forth in the Eclipse
# Public License 2.0 are satisfied: GNU General Public License, version 2
# or later which is available at
# https://www.gnu.org/licenses/old-licenses/gpl-2.0-standalone.html
# SPDX-License-Identifier: EPL-2.0 OR GPL-2.0-or-later

# @file    dailyUpdateMakeGCC.sh
# @author  Michael Behrisch
# @date    2008

# Does the nightly git pull on the linux server and then runs build and tests
PREFIX=$1
export FILEPREFIX=$2
export SMTP_SERVER=$3
MAKELOG=$PREFIX/${FILEPREFIX}make.log
MAKEALLLOG=$PREFIX/${FILEPREFIX}makealloptions.log
STATUSLOG=$PREFIX/${FILEPREFIX}status.log
TESTLOG=$PREFIX/${FILEPREFIX}test.log
export SUMO_BATCH_RESULT=$PREFIX/${FILEPREFIX}batch_result
export SUMO_REPORT=$PREFIX/${FILEPREFIX}report
export SUMO_BINDIR=$PREFIX/sumo/bin
# the following is only needed for the clang build but it does not hurt others
export LSAN_OPTIONS=suppressions=$PREFIX/sumo/build/clang_memleak_suppressions.txt
if test $# -ge 4; then
  CONFIGURE_OPT=$4
fi

rm -f $STATUSLOG
echo -n "$FILEPREFIX " > $STATUSLOG
date >> $STATUSLOG
echo "--" >> $STATUSLOG
cd $PREFIX/sumo
rm -rf build/$FILEPREFIX
basename $MAKELOG >> $STATUSLOG
git pull &> $MAKELOG || (echo "git pull failed" | tee -a $STATUSLOG; tail -10 $MAKELOG)
git submodule update >> $MAKELOG 2>&1 || (echo "git submodule update failed" | tee -a $STATUSLOG; tail -10 $MAKELOG)
GITREV=`tools/build/version.py -`
date >> $MAKELOG
mkdir build/$FILEPREFIX && cd build/$FILEPREFIX
cmake ${CONFIGURE_OPT:5} -DCMAKE_INSTALL_PREFIX=$PREFIX ../.. >> $MAKELOG 2>&1 || (echo "cmake failed" | tee -a $STATUSLOG; tail -10 $MAKELOG)
if make -j32 >> $MAKELOG 2>&1; then
  date >> $MAKELOG
  make lisum >> $MAKELOG 2>&1
  if make install >> $MAKELOG 2>&1; then
    if test "$FILEPREFIX" == "gcc4_64"; then
      make -j distcheck >> $MAKELOG 2>&1 || (echo "make distcheck failed" | tee -a $STATUSLOG; tail -10 $MAKELOG)
    fi
  else
    echo "make install failed" | tee -a $STATUSLOG; tail -10 $MAKELOG
  fi
else
  echo "make failed" | tee -a $STATUSLOG; tail -20 $MAKELOG
fi
date >> $MAKELOG
echo `grep -ci 'warn[iu]ng:' $MAKELOG` warnings >> $STATUSLOG

echo "--" >> $STATUSLOG
cd $PREFIX/sumo
if test -e $SUMO_BINDIR/sumo -a $SUMO_BINDIR/sumo -nt build/$FILEPREFIX/Makefile; then
  # run tests
  export PATH=$PREFIX/texttest/bin:$PATH
  export TEXTTEST_TMP=$PREFIX/texttesttmp
  TESTLABEL=`LANG=C date +%d%b%y`r$GITREV
  rm -rf $TEXTTEST_TMP/*
  if test ${FILEPREFIX::6} == "extra_"; then
    tests/runExtraTests.py --gui "b $FILEPREFIX" &> $TESTLOG
  else
    tests/runTests.sh -b $FILEPREFIX -name $TESTLABEL &> $TESTLOG
    if which Xvfb &>/dev/null; then
      tests/runTests.sh -a sumo.gui -b $FILEPREFIX -name $TESTLABEL >> $TESTLOG 2>&1
    fi
  fi
  tests/runTests.sh -b $FILEPREFIX -name $TESTLABEL -coll >> $TESTLOG 2>&1
  if test -e build/$FILEPREFIX/src/CMakeFiles/sumo.dir/sumo_main.cpp.gcda; then
    echo "lcov/html" >> $STATUSLOG
    echo "Coverage report" >> $STATUSLOG
  else
    echo "batchreport" >> $STATUSLOG
  fi
fi

# running extra tests for the coverage report
if test -e build/$FILEPREFIX/src/CMakeFiles/sumo.dir/sumo_main.cpp.gcda; then
  date >> $TESTLOG
  tests/runExtraTests.py --gui "b $FILEPREFIX" >> $TESTLOG 2>&1
#  $SIP_HOME/tests/runTests.sh -b $FILEPREFIX >> $TESTLOG 2>&1
  cd build/$FILEPREFIX
  make lcov >> $TESTLOG 2>&1 || (echo "make lcov failed"; tail -10 $TESTLOG)
  cd $PREFIX/sumo
  date >> $TESTLOG
fi

echo "--" >> $STATUSLOG
basename $MAKEALLLOG >> $STATUSLOG
export CXXFLAGS="$CXXFLAGS -Wall -W -pedantic -Wno-long-long -Wformat -Wformat-security"
rm -rf build/debug-$FILEPREFIX
mkdir build/debug-$FILEPREFIX && cd build/debug-$FILEPREFIX
cmake ${CONFIGURE_OPT:5} -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX=$PREFIX ../.. > $MAKEALLLOG 2>&1 || (echo "cmake debug failed" | tee -a $STATUSLOG; tail -10 $MAKEALLLOG)
if make -j32 >> $MAKEALLLOG 2>&1; then
  make install >> $MAKEALLLOG 2>&1 || (echo "make install with all options failed" | tee -a $STATUSLOG; tail -10 $MAKEALLLOG)
else
  echo "make with all options failed" | tee -a $STATUSLOG; tail -20 $MAKEALLLOG
fi
cd $PREFIX/sumo
echo `grep -ci 'warn[iu]ng:' $MAKEALLLOG` warnings >> $STATUSLOG
echo "--" >> $STATUSLOG

basename $TESTLOG >> $STATUSLOG
date >> $STATUSLOG
echo "--" >> $STATUSLOG

# netedit tests
if test -e $SUMO_BINDIR/netedit -a $SUMO_BINDIR/netedit -nt build/$FILEPREFIX/Makefile; then
  if test "$FILEPREFIX" == "gcc4_64"; then
    tests/runNeteditDailyTests.sh -b ${FILEPREFIX}netedit -name $TESTLABEL >> $TESTLOG 2>&1
    tests/runTests.sh -b ${FILEPREFIX} -name $TESTLABEL -coll >> $TESTLOG 2>&1
  fi
fi

# macOS M1 wheels
if test ${FILEPREFIX: -2} == "M1"; then
  rm -rf dist dist_native _skbuild wheelhouse
  python3 tools/build/setup-sumo.py bdist_wheel
  python3 tools/build/setup-libsumo.py bdist_wheel
  python3 tools/build/setup-libtraci.py bdist_wheel
  mv dist/eclipse_sumo-* `echo dist/eclipse_sumo-* | sed 's/cp39-cp39/py2.py3-none/'`
  # the credentials are in ~/.pypirc
  twine upload --skip-existing -r testpypi dist/*
  mv dist dist_native  # just as backup
  docker run --rm -v $PWD:/github/workspace manylinux2014_aarch64 tools/build/build_wheels.sh $HTTPS_PROXY
  twine upload --skip-existing -r testpypi wheelhouse/*
fi
