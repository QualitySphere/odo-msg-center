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
echo "Start MSG Center APP"
export PYTHONPATH=$PWD
python app/run.py
