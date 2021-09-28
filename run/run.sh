#!/bin/bash
echo "Run $0"
CUR_DIR=`dirname $0`
cd $CUR_DIR/../src
#source activate dev
# craw data
#which python
/home/mario/miniconda3/envs/dev/bin/python crawler.py
# push to github
cd ~/git/vnfunds_data/data
git add .
git commit -m "Update data"
git push
