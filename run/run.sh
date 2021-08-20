#!/bin/bash
CUR_DIR=`dirname $0`
cd $CUR_DIR/../src
source activate dev
# craw data
python crawler.py
# push to github
cd ~/git/vnfunds_data/data
git add .
git commit -m "Update data"
git push
