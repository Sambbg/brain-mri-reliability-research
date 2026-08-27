# GitHub Connection Log for Reproducible Research Repository

## Purpose

This document records the Git/GitHub connection process used for the local research repository. It is intended to preserve the setup history so that the workflow can be reviewed later by the user, a supervisor, or an AI assistant without relying on memory.

This file deliberately **does not include any GitHub personal access token, password, private SSH key, or other secret**. One GitHub token was pasted during the session and must be treated as compromised. It should be revoked in GitHub immediately if not already revoked.

---

## Local Repository Context

The local repository is located at:

```bash
~/research
```

The terminal prompt during the setup showed the active virtual environment and machine context as:

```text
(venv) raha@raha-B450-I-AORUS-PRO-WIFI:~/research$
```

The repository branch was renamed from `master` to:

```text
main
```

---

## GitHub Repository URL

The intended GitHub repository is:

```text
https://github.com/Sambbg/brain-mri-reliability-research.git
```

The SSH-form remote URL should be:

```text
git@github.com:Sambbg/brain-mri-reliability-research.git
```

Repository name:

```text
brain-mri-reliability-research
```

GitHub username / owner used:

```text
Sambbg
```

---

## Files Committed Before GitHub Push

The following reproducibility documentation file was added and committed:

```bash
git add REPRODUCIBLE_ENVIRONMENT_SETUP.md
git commit -m "add reproducible environment setup documentation"
git status
```

Observed successful commit:

```text
[main 156479a] add reproducible environment setup documentation
 1 file changed, 1224 insertions(+)
 create mode 100644 REPRODUCIBLE_ENVIRONMENT_SETUP.md
On branch main
nothing to commit, working tree clean
```

This means the local repository was clean before attempting to connect to GitHub.

---

## HTTPS Remote Setup Attempt

The HTTPS remote was added with:

```bash
git remote add origin https://github.com/Sambbg/brain-mri-reliability-research.git
```

The remote was verified with:

```bash
git remote -v
```

Observed output:

```text
origin	https://github.com/Sambbg/brain-mri-reliability-research.git (fetch)
origin	https://github.com/Sambbg/brain-mri-reliability-research.git (push)
```

---

## Failed HTTPS Push Attempts

The initial push command was:

```bash
git push -u origin main
```

### Error 1: Password authentication not supported

Observed error:

```text
Username for 'https://github.com': Sambbg 
Password for 'https://Sambbg@github.com': 
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/Sambbg/brain-mri-reliability-research.git/'
```

Interpretation:

GitHub does not allow normal account passwords for Git operations over HTTPS. A Personal Access Token or SSH authentication is required.

### Error 2: Write access not granted

After attempting token authentication, the following error occurred:

```text
remote: Write access to repository not granted.
fatal: unable to access 'https://github.com/Sambbg/brain-mri-reliability-research.git/': The requested URL returned error: 403
```

Interpretation:

Authentication reached GitHub, but GitHub denied write access. Likely causes include:

- the token did not have write permission,
- the token was not granted access to this specific repository,
- the repository did not exist under the expected owner,
- the authenticated account did not have permission to push to the repository.

Status:

The HTTPS/token route was abandoned in favor of SSH.

---

## Security Incident: Token Exposure

A GitHub Personal Access Token was pasted during the session. This token must be considered compromised.

Required action:

```text
GitHub → Settings → Developer settings → Personal access tokens → revoke/delete the exposed token
```

Do not store personal access tokens in Markdown files, Git repositories, notebooks, scripts, shell history, or chat logs intended for reuse.

---

## SSH Key Generation

To avoid HTTPS token issues, an SSH key was generated.

Command used:

```bash
ssh-keygen -t ed25519 -C "samuel.b.gonzalves@gmail.com"
```

Observed output:

```text
Generating public/private ed25519 key pair.
Enter file in which to save the key (/home/raha/.ssh/id_ed25519): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/raha/.ssh/id_ed25519
Your public key has been saved in /home/raha/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:5GS2ZXU5oq8wCqgHLNyisuhWZF7jiZZsGi0Bsg1Yd4w samuel.b.gonzalves@gmail.com
```

The private key path is:

```text
/home/raha/.ssh/id_ed25519
```

The public key path is:

```text
/home/raha/.ssh/id_ed25519.pub
```

Important:

- Never share the private key: `~/.ssh/id_ed25519`
- Only the public key should be copied into GitHub: `~/.ssh/id_ed25519.pub`

---

## Command to Display Public Key

The public key can be displayed using:

```bash
cat ~/.ssh/id_ed25519.pub
```

The output starts with:

```text
ssh-ed25519
```

and usually ends with the email/comment used when generating the key.

Only this public key should be pasted into GitHub.

---

## GitHub SSH Key Registration Steps

In the GitHub web interface:

```text
Profile picture → Settings → SSH and GPG keys → New SSH key
```

Recommended fields:

```text
Title: Ubuntu research machine
Key type: Authentication Key
Key: paste output of cat ~/.ssh/id_ed25519.pub
```

Then click:

```text
Add SSH key
```

---

## Switch Git Remote From HTTPS to SSH

After adding the SSH key to GitHub, the remote should be changed from HTTPS to SSH:

```bash
cd ~/research
git remote set-url origin git@github.com:Sambbg/brain-mri-reliability-research.git
git remote -v
```

Expected output:

```text
origin  git@github.com:Sambbg/brain-mri-reliability-research.git (fetch)
origin  git@github.com:Sambbg/brain-mri-reliability-research.git (push)
```

---

## Test SSH Authentication

Run:

```bash
ssh -T git@github.com
```

On first connection, GitHub may ask:

```text
Are you sure you want to continue connecting?
```

Type:

```text
yes
```

Expected successful output:

```text
Hi Sambbg! You've successfully authenticated, but GitHub does not provide shell access.
```

This confirms that GitHub recognizes the SSH key.

---

## Push Local Repository to GitHub

After SSH authentication works, push the repository:

```bash
cd ~/research
git push -u origin main
```

Expected result:

The local `main` branch should be pushed to GitHub and linked to `origin/main`.

Verify with:

```bash
git status
```

Expected clean state after successful push:

```text
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

---

## Troubleshooting Table

| Issue | Exact symptom/error | Likely root cause | Fix applied / recommended | Status |
|---|---|---|---|---|
| HTTPS password authentication failed | `Password authentication is not supported for Git operations.` | GitHub no longer accepts account passwords for Git over HTTPS | Use Personal Access Token or SSH | HTTPS abandoned |
| Token authentication failed with 403 | `Write access to repository not granted` | Token did not have correct repo/write permission, repo access not granted, or repo ownership mismatch | Use SSH key or create correct token with repo write access | Switched to SSH |
| Token exposed in chat | Token was pasted directly into chat | Secret handling mistake | Revoke/delete token immediately in GitHub | Must verify revoked |
| SSH key needed | HTTPS push failed repeatedly | Token approach was fragile | Generated ED25519 SSH key | Key generated successfully |
| Public key must be added to GitHub | SSH key exists locally but GitHub will not know it until registered | Public key not yet added to GitHub | Add `~/.ssh/id_ed25519.pub` to GitHub SSH keys | User to complete/verify |
| Remote still uses HTTPS | `git remote -v` shows `https://...` | Remote URL not changed after SSH setup | `git remote set-url origin git@github.com:Sambbg/brain-mri-reliability-research.git` | Pending/verify |

---

## Current Known State at Time of Documentation

Confirmed from the session:

- Local Git repository exists at `~/research`
- Branch is `main`
- Working tree was clean before GitHub connection attempt
- `REPRODUCIBLE_ENVIRONMENT_SETUP.md` was committed successfully
- HTTPS remote was added successfully
- HTTPS push failed because password authentication is unsupported and then because write access was denied
- SSH key pair was generated successfully at:
  - private key: `/home/raha/.ssh/id_ed25519`
  - public key: `/home/raha/.ssh/id_ed25519.pub`

Not yet confirmed in the chat at the time this file was created:

- Whether the public SSH key was added to GitHub
- Whether `ssh -T git@github.com` succeeded
- Whether the remote was changed to SSH
- Whether `git push -u origin main` succeeded via SSH

---

## Recommended Next Commands

Run these only after the public SSH key has been added to GitHub:

```bash
cd ~/research

# Switch remote to SSH
git remote set-url origin git@github.com:Sambbg/brain-mri-reliability-research.git

# Confirm remote
git remote -v

# Test GitHub SSH authentication
ssh -T git@github.com

# Push local main branch to GitHub
git push -u origin main

# Verify final state
git status
```

---

## Security Rules for Future Work

1. Never paste GitHub tokens into chat, Git commits, notebooks, scripts, or documentation.
2. Never share the private SSH key file: `~/.ssh/id_ed25519`.
3. It is safe to share the public key file: `~/.ssh/id_ed25519.pub`.
4. Use SSH for long-term GitHub work on this research machine.
5. Keep the repository private until sensitive files, datasets, model weights, and paper drafts are reviewed.
6. Do not commit datasets, trained model weights, virtual environments, passwords, or API keys.
7. Maintain a `.gitignore` that excludes at least:

```text
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.env
.DS_Store
```

---

## Academic Reproducibility Note

Connecting the local repository to GitHub is not just a convenience step. It supports publication-grade reproducibility by preserving:

- exact code history,
- environment documentation,
- setup decisions,
- command-level reproducibility records,
- future experiment commits,
- paper/supplementary material traceability.

For each future experiment, the Git commit hash should be recorded alongside:

- dataset version,
- train/validation/test split,
- random seed,
- Python package environment,
- GPU/driver/CUDA state,
- model configuration,
- evaluation metrics.

