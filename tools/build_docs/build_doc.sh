#! /usr/bin/env bash

# find local apps
MARKDOWN=`which markdown`
HTML2PS=`which html2ps`
PS2PDF=`which ps2pdf`

# set initial value for dependencies being met
DEPEND=true

# get action and file from args
ACTION=$1
FILE=$2
FILE_BASE=${FILE%.*}

#echo $MARKDOWN
#echo $HTML2PS
#echo $PS2PDF
#echo $ACTION
#echo $FILE
#echo $FILE_BASE

# short circuit
#MARKDOWN=`which asdasdasd`
#HTML2PS=`which asdasdasdasd`

# test for dependencies
if [ -z $MARKDOWN ] ; then
    DEPEND=false
    echo 'Please install markdown.'
fi

if [ -z $HTML2PS ] ; then
    DEPEND=false
    echo 'Please install html2ps.'
fi

if [ -z $PS2PDF ] ; then
    DEPEND=false
    echo 'Please install ps2pdf.'
fi

# test for action
if [ $DEPEND = true ] ; then
    if [ $ACTION = 'pdf' ] || [ $ACTION = 'PDF' ] ; then
        $MARKDOWN $FILE | $HTML2PS -f html2ps.conf --toc h | $PS2PDF - $FILE_BASE.pdf
    else
        if [ $ACTION = 'html' ] || [ $ACTION = 'HTML' ] ; then
            $MARKDOWN $FILE > $FILE_BASE.html
        fi
    fi
else
    exit
fi

#markdown TCAREe-Spec.md | html2ps -f html2ps.conf --toc h | ps2pdf - TCAREe.pdf && evince TCAREe.pdf&
