#!/usr/bin/env bash

export DATA_DIR=$HOME/data
export PRETRAINED_DIR=$DATA_DIR/pretrained

export OUT_DIR=/tmp/active-qa
mkdir $OUT_DIR

export REFORMULATOR_DIR=$OUT_DIR/reformulator
mkdir $REFORMULATOR_DIR

echo "model_checkpoint_path: \"$PRETRAINED_DIR/translate.ckpt-1460356\"" > checkpoint
cp -f checkpoint $REFORMULATOR_DIR
cp -f checkpoint $REFORMULATOR_DIR/initial_checkpoint.txt