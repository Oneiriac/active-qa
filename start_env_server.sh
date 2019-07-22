#!/usr/bin/env bash
export ACTIVE_QA_DIR='.'
source $ACTIVE_QA_DIR/venv/bin/activate

python -m px.environments.bidaf_server \
    --port=10000 \
    --squad_data_dir=$ACTIVE_QA_DIR/data/squad \
    --bidaf_shared_file=$ACTIVE_QA_DIR/data/bidaf/shared.json \
    --bidaf_model_dir=$ACTIVE_QA_DIR/data/bidaf/