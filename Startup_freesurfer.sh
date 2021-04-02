#!/bin/bash

cd /home/lg/Science/freesurfer/subjects

## bash
export FREESURFER_HOME=/home/lg/Science/freesurfer
source $FREESURFER_HOME/SetUpFreeSurfer.sh

recon-all $1 -i $2 -s $3 $4


