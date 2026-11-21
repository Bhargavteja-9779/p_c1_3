# Resume protocol (read first when the user says "continue")

Long-running research-paper project (Battery Energy submission). Several sessions/accounts have worked on it in
parallel, each on its own `claude/*` branch. Before doing anything:

1. `git fetch origin` and find the most advanced branch:
   `git for-each-ref --sort=-committerdate --format='%(committerdate:iso) %(refname:short)' refs/remotes/origin`
   Read its `PROJECT_STATE.md` ("RESUME HERE" section) with `git show <branch>:PROJECT_STATE.md`.
   If it is ahead of your branch, bring it in (merge; when histories conflict, keep the most advanced branch's tree).
2. Follow "RESUME HERE" in `PROJECT_STATE.md` (environment, resuming experiments, next tasks).
3. Start the autosave loop (commits + pushes every 10 min): `setsid nohup tools/autosave.sh >/dev/null 2>&1 &`
4. After every meaningful step: update `PROJECT_STATE.md` ("RESUME HERE"), commit, push.
   Never keep important outputs only in the container (REVIEW/ reports, chunks, drafts must be committed).
