#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew install imagemagick
    brew install python && brew link --overwite python
else
   sudo apt-get -qq update
   sudo apt-get install -y imagemagick
fi
