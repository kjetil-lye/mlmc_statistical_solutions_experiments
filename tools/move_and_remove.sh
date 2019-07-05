#!/bin/bash
set -e
rsync -avP $1 $2
rm -rf $1/*.nc
