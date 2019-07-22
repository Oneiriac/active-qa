import os
from typing import List
from pathlib import Path

from px.nmt import reformulator
from px.proto import reformulator_pb2

OUT_PATH = Path(os.environ.get('OUT_DIR') or '/tmp/active-qa')
REFORMULATOR_PATH = OUT_PATH / 'reformulator'
REFORMULATOR_PATH.mkdir(parents=True, exist_ok=True)


class FlaskReformulator:
    def __init__(self,
                 environment_server_address='localhost:10000'):
        hparams_path = './reformulator.json'
        source_prefix = '<en> <2en> '
        self.instance = reformulator.Reformulator(
            hparams_path=hparams_path,
            source_prefix=source_prefix,
            out_dir=str(REFORMULATOR_PATH),
            environment_server_address=environment_server_address
        )

    def reformulate(self,
                    questions: List[str],
                    inference_mode=reformulator_pb2.ReformulatorRequest.BEAM_SEARCH
                    ) -> List[str]:
        responses = self.instance.reformulate(
            questions=questions,
            inference_mode=inference_mode)

        if inference_mode == reformulator_pb2.ReformulatorRequest.GREEDY:
            # Since we are using greedy decoder, keep only the first rewrite.
            reformulations = [r[0].reformulation for r in responses]
        else:
            reformulations = [[t.reformulation for t in r] for r in responses]

        output = []
        for r in reformulations:
            for t in r:
                output.append(t)
        return output
