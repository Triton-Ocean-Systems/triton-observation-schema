# Agent instructions

## Security rules (mandatory)

Every coding agent working in this repository (Codex, Claude or any other) must follow these rules, without exception. They exist because forged commits carrying hidden malware were force-pushed to Triton repositories on 2026-09-28 and 2026-10-01.

1. Never force push. Never push to `main` or any default branch. Work on a new branch and open a pull request; a human merges.
2. Never rewrite, amend, rebase or recreate commits that are already on GitHub, and never create a commit that copies another commit's message and author date.
3. Before every commit and every push, run these from the repository root and STOP if any of them prints anything:

   ```sh
   git grep -n -I -P '_\$_90e0|global\.o=' HEAD
   git grep -n -I -P '\S {40,}\S|\S\t{10,}\S' HEAD -- '*.js' '*.mjs' '*.cjs' '*.ts' '*.py' '*.sh' '*.ps1'
   git grep -n -I -P '^.{1500,}$' HEAD -- '*.js' '*.mjs' '*.cjs' '*.ts' ':!*package-lock.json' ':!*.min.js'
   ```

   If anything matches: do not push, do not run `npm install` or `node` in this repository, and report the file and line to the user. The first check is written as a regular expression so that this file does not match its own check.
4. Never write obfuscated or minified code by hand, never put code after long runs of spaces or tabs, never add `eval`, `new Function`, or code built from base64, hex or character codes, and never add code that downloads and runs something.
5. Never add install-time or open-time hooks: no `preinstall`/`install`/`postinstall` scripts, no `"runOn": "folderOpen"` tasks, no git hooks.
6. Never add a CI step that sends secrets anywhere, or prints or encodes them.
7. Work only in your own working copy. Do not modify, stage or commit in folders other agents use (for example another agent's clone of this repository), and do not restart the bench console without saying so.
8. After every push, report: repository, branch, commit hash, every file changed, and the output of the checks in rule 3.
