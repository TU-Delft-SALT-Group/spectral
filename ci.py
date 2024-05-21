#!/usr/bin/env python3
import os
import sys

stages = {
    "app": """
            cd app &&
            pnpm lint &&
            pnpm exec vitest run --coverage &&
            cd ..
    """,
    "kernel": [],
    "end-to-end": [],
}

args = sys.argv


def run_stage(stage: str):
    print(f"[INFO]: Attempting to run {stage} stage.")

    if stage not in stages:
        sys.stderr.write(f"[ERROR]: Stage {args[1]} is not in stages.\n")
        exit(-2)

    os.system(stages[stage])


if len(args) > 2:
    sys.stderr.write("[ERROR]: Please give at least one argument.\n")
    exit(-1)

if len(args) == 1:
    for stage in stages:
        run_stage(stage)
    exit(0)

run_stage(args[1])
exit(0)
