#!/bin/sh
echo "Check template"
if [ -d template ]; then
    if [ $(ls template | wc -l) == 0 ]; then
        echo "Generate template files"
        for tmpl_file in $(ls tmpl)
        do
            cp tmpl/$tmpl_file template/
        done
    fi
else
    echo "Generate template dir and files"
    cp -R tmpl template
fi
echo "Check complete"
echo "Start app"
export PYTHONPATH=$PWD
python app/run.py
