# Resume protocol (read first when the user says "continue")

This repo is a long-running research-paper project (Battery Energy submission). Work is
checkpointed to git so any new session/container can pick up where the last one stopped.

1. Read `PROJECT_STATE.md` (status + exact next steps), then `EXPERIMENT_LOG.md`.
2. Environment: `pip install -r Target_Journal_Submission/code/requirements.txt`.
   Raw data is NOT needed for experiments (feature tables are in `Target_Journal_Submission/data/features/`).
3. If experiments are unfinished, resume (finished experiments/chunks are skipped automatically):
   ```
   cd Target_Journal_Submission/code
   setsid nohup python run_all.py --mode full --stages experiments analysis figures > ../results_full_stdoutN.log 2>&1 &
   ```
   Check status: `ls Target_Journal_Submission/results/raw Target_Journal_Submission/results/raw/chunks` and the newest log.
4. Start the autosave loop so progress is pushed every 10 min: `setsid nohup tools/autosave.sh >/dev/null 2>&1 &`
5. After every meaningful step: update `PROJECT_STATE.md` ("Next steps (exact)"), commit, push.
   Never keep important outputs only in the container (e.g. REVIEW/ reports must be committed).
