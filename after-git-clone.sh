#!/bin/bash

git submodule update --init --recursive
if [ -x /usr/local/bin/pre-commit ]; then
  pre-commit install
fi
