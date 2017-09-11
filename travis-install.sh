#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew install imagemagick
else
   sudo apt-get -qq update
   sudo apt-get install -y imagemagick
fi
