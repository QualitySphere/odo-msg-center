#!/bin/sh
set -e

echo "Check template"
if [ -d template ]; then
    echo "Check and generate template files"
    for tmpl_file in $(ls tmpl)
    do
        if [ -f template/$tmpl_file ]; then
            echo "Template file: $tmpl_file exists"
        else
            echo "Copy template file: $tmpl_file"
            cp tmpl/$tmpl_file template/
        fi
    done
else
    echo "Generate template dir and files"
    cp -R tmpl template
fi
echo "Check complete"

echo "Check config"
if [ -d config ]; then
    echo "Check and generate config files"
    for cfg_file in $(ls cfg)
    do
        if [ -f config/$cfg_file ]; then
            echo "Config file: $cfg_file exists"
        else
            echo "Copy config file: $cfg_file"
            cp cfg/$cfg_file config/
        fi
    done
else
    echo "Generate config dir and files"
    cp -R cfg config
fi
echo "Check complete"

echo "Start OpenDevOps MSG Center APP"
export PYTHONPATH=$PWD
python app/run.py
