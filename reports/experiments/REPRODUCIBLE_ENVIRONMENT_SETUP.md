# Reproducible Computational Environment Setup for Deep Learning-Based Medical Imaging Research

## 1. Title

**Reproducible Computational Environment Setup for Deep Learning-Based Medical Imaging and Research Computing**

This document records the step-by-step construction, verification, troubleshooting, and final state of a local research computing environment intended for deep learning experimentation, medical imaging model development, and publication-grade reproducibility.

---

## 2. Purpose and Scope

The purpose of this environment is to support reproducible deep learning research with an emphasis on:

- transparent computational setup;
- isolated software environments;
- command-level documentation;
- version-controlled project structure;
- GPU verification for accelerated training;
- future medical imaging experiments;
- future thesis, appendix, supplementary material, or GitHub repository documentation.

The broader research context is reliability-focused machine learning for medical imaging, especially brain MRI tumour classification, calibration, uncertainty estimation, and cross-dataset evaluation. This setup is not itself sufficient for a publication-grade study, but it establishes the computational foundation needed for reproducible experimentation.

This document distinguishes between:

- **confirmed from this setup session**: commands, outputs, configuration, and verified states that were explicitly observed;
- **recommended next steps**: additional practices required to strengthen the environment for thesis-level or journal-level reproducibility.

No claim is made that the environment alone satisfies Q1-journal standards. Rather, it is a documented foundation for publication-grade reproducibility.

---

## 3. Hardware Specification

The machine used was described as a desktop/gaming computer. The following specifications were provided or confirmed during setup.

| Component | Specification | Verification status |
|---|---:|---|
| Computer type | Desktop/gaming computer | Stated by user |
| Storage | 1 TB storage, partitioned into multiple drives | Stated by user and partially observed during partitioning |
| RAM | 16 GB RAM | Stated by user, not independently verified in terminal output |
| CPU | AMD Ryzen 5 5500G | Stated by user, not independently verified in terminal output |
| GPU | NVIDIA GeForce RTX 3060 | Confirmed by `nvidia-smi` and PyTorch |
| GPU VRAM | 12,288 MiB shown by `nvidia-smi` | Confirmed |
| Motherboard/hostname clue | `raha-B450-I-AORUS-PRO-WIFI` | Observed from terminal prompt |

The GPU was explicitly verified by both NVIDIA system utilities and PyTorch. CPU, RAM, and full disk model details should be formally recorded later using commands such as `lscpu`, `free -h`, and `lsblk`.

---

## 4. Operating System and System Context

The machine was set up using Ubuntu 22.04.5 LTS Desktop installer.

The selected image was:

```text
ubuntu-22.04.5-desktop-amd64.iso
```

The user was guided away from the server image and WSL image because the objective was a full local Linux research environment with GUI support, terminal support, and direct GPU access.

The terminal prompt observed after installation was:

```text
(venv) raha@raha-B450-I-AORUS-PRO-WIFI:~/research$
```

This indicates:

- username: `raha`
- hostname: `raha-B450-I-AORUS-PRO-WIFI`
- active Python virtual environment: `venv`
- working directory: `~/research`

The environment is Ubuntu/Debian-based, supported by the use of `apt`, `ubuntu-drivers`, and Ubuntu installation media.

The exact OS version should still be formally recorded using:

```bash
lsb_release -a
cat /etc/os-release
uname -a
```

---

## 5. Storage and Operating System Installation Decisions

### 5.1 Installation media

The Ubuntu Desktop ISO was written to USB using Rufus. The file was **not** copied directly to USB, because an ISO file must be flashed as a bootable disk image.

Recommended Rufus settings used during guidance:

```text
Partition scheme: GPT
Target system: UEFI (non-CSM)
Mode: ISO Image mode (recommended)
```

### 5.2 Partitioning decision

Initially, the Ubuntu installer showed a smaller SSD option for installing Ubuntu alongside Windows. The user also had a 1 TB drive, but it contained important files. The installer’s simple “Install alongside Windows Boot Manager” method did not provide the desired control over that 1 TB disk.

The user therefore entered manual partitioning using:

```text
Something else
```

The 1 TB drive contained an NTFS partition with important files. Because of this, the existing NTFS partition was **not deleted**.

Instead, the safe approach was:

1. reboot into Windows;
2. open Disk Management;
3. shrink the existing 1 TB data partition;
4. create approximately 400 GB of unallocated space;
5. return to the Ubuntu installer;
6. install Ubuntu only into the newly created free space.

### 5.3 Final partitioning action

The user freed approximately 400 GB. In the Ubuntu installer, the observed free space was approximately:

```text
419431 MB free space
```

This free space was used to create:

- an ext4 root partition mounted at `/`;
- a swap partition.

The confirmation screen showed formatting of newly created Linux partitions only:

```text
partition #2 of SCSI1 (0,0,0) (sda) as ext4
partition #3 of SCSI1 (0,0,0) (sda) as swap
```

The existing NTFS partition containing user data was not selected for formatting.

---

## 6. GPU and NVIDIA Driver Setup

### 6.1 Confirmed GPU verification

The following command was run successfully:

```bash
nvidia-smi
```

Observed output included:

```text
NVIDIA-SMI 580.126.09             Driver Version: 580.126.09     CUDA Version: 13.0
GPU  Name: NVIDIA GeForce RTX 3060
Memory: 325MiB / 12288MiB
```

This confirms:

- the NVIDIA driver is installed and active;
- the RTX 3060 is detected by the operating system;
- the NVIDIA driver reports CUDA runtime compatibility up to CUDA 13.0;
- the display server and desktop shell are using a small amount of GPU memory.

### 6.2 PyTorch GPU verification

The following Python verification command was run inside the virtual environment:

```bash
python - <<'PY'
import torch
print("PyTorch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("CUDA version used by PyTorch:", torch.version.cuda)
else:
    print("No GPU detected by PyTorch")
PY
```

Observed output:

```text
PyTorch: 2.11.0+cu130
CUDA available: True
GPU: NVIDIA GeForce RTX 3060
CUDA version used by PyTorch: 13.0
```

This confirms that PyTorch can access the GPU through CUDA.

### 6.3 GPU sanity test

A GPU matrix multiplication test was created as `test_gpu.py` and executed successfully.

```python
import torch
import time

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if not torch.cuda.is_available():
    raise SystemExit("CUDA is not available. Stop here.")

device = torch.device("cuda")
print("GPU:", torch.cuda.get_device_name(0))

# Small GPU workload
x = torch.rand((8000, 8000), device=device)
y = torch.rand((8000, 8000), device=device)

torch.cuda.synchronize()
start = time.time()

z = torch.matmul(x, y)

torch.cuda.synchronize()
end = time.time()

print("Matrix multiplication completed on GPU.")
print("Result shape:", z.shape)
print("Time:", round(end - start, 4), "seconds")
print("GPU memory allocated:", round(torch.cuda.memory_allocated() / 1024**3, 2), "GB")
```

Observed output:

```text
PyTorch version: 2.11.0+cu130
CUDA available: True
GPU: NVIDIA GeForce RTX 3060
Matrix multiplication completed on GPU.
Result shape: torch.Size([8000, 8000])
Time: 0.4135 seconds
GPU memory allocated: 0.72 GB
```

This confirms real GPU computation, not merely driver detection.

### 6.4 Recommended additional NVIDIA checks

The following commands were recommended for complete system-level documentation but were not shown as executed in the chat:

```bash
lsmod | grep nvidia
```

Purpose: verifies that NVIDIA kernel modules are loaded.

```bash
lspci -k | grep -A 3 -E "VGA|3D"
```

Purpose: identifies the GPU hardware and the kernel driver currently bound to it.

### 6.5 Secure Boot / MOK status

A Secure Boot / MOK issue was mentioned as a possible driver installation pitfall in guidance, but no actual Secure Boot or MOK error was observed in the confirmed terminal output. Therefore, this setup document does **not** claim that Secure Boot was encountered or resolved.

If Secure Boot problems occur in future NVIDIA driver installation, they should be documented separately with exact error messages and resolution steps.

### 6.6 NVIDIA command typo status

No confirmed `nvidea-smi` typo or related terminal output was observed in the chat transcript. The correct command used and verified was:

```bash
nvidia-smi
```

---

## 7. Python Environment Setup

### 7.1 Project directory creation

The research workspace was created under the user’s home directory:

```bash
mkdir ~/research
cd ~/research
```

In the confirmed terminal output, the working directory was:

```text
~/research
```

### 7.2 Virtual environment creation

A Python virtual environment named `venv` was used.

The active prompt confirmed activation:

```text
(venv) raha@raha-B450-I-AORUS-PRO-WIFI:~/research$
```

Activation command:

```bash
source venv/bin/activate
```

Verification commands used:

```bash
python --version
pip --version
```

Observed output:

```text
Python 3.10.12
pip 26.0.1 from /home/raha/research/venv/lib/python3.10/site-packages/pip (python 3.10)
```

This confirms that Python and pip were being used from the virtual environment path, not the system Python environment.

### 7.3 Missing ensurepip issue

The user requested inclusion of the following error:

```text
The virtual environment was not created successfully because ensurepip is not available
```

This exact error was not visible in the confirmed transcript excerpts provided during the final verification phase, but it is a common Ubuntu issue when the `python3.10-venv` package is missing.

When encountered, the root cause is that Ubuntu separates the virtual environment support package from the base Python installation. The fix is:

```bash
sudo apt update
sudo apt install python3.10-venv
```

Then recreate the environment:

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

Verification of activation:

```bash
which python
which pip
python --version
pip --version
```

Expected evidence of correct activation is that `which python` and `which pip` point inside:

```text
/home/raha/research/venv/
```

### 7.4 Confirmed active environment

The final confirmed Python state was:

```text
Python 3.10.12
pip 26.0.1
PyTorch: 2.11.0+cu130
CUDA available: True
GPU: NVIDIA GeForce RTX 3060
CUDA version used by PyTorch: 13.0
```

---

## 8. Package Management and Requirements

### 8.1 Requirements file

The environment was captured using:

```bash
pip freeze > requirements.txt
```

The file `requirements.txt` was then added to Git and committed:

```bash
git add requirements.txt
git commit -m "add requirements file"
```

Observed commit output:

```text
[master 6ef512e] add requirements file
 1 file changed, 139 insertions(+)
 create mode 100644 requirements.txt
```

### 8.2 Importance of requirements.txt

The `requirements.txt` file records installed Python package versions at the time of setup. This improves reproducibility by allowing another researcher to recreate a similar Python environment using:

```bash
pip install -r requirements.txt
```

However, `requirements.txt` is not a perfect long-term lockfile. It captures Python package versions, but not necessarily all system-level libraries, GPU driver state, CUDA runtime details, or binary compatibility. For stronger future reproducibility, a container, Conda lockfile, or Dockerfile should be considered.

### 8.3 Recommended dependency refresh

After GPU tests and package installation, the requirements file should be refreshed:

```bash
pip freeze > requirements.txt
git status
git add requirements.txt
git commit -m "update locked Python dependencies"
git status
```

If Git reports nothing to commit, then the file was already up to date.

---

## 9. Git and Version Control Setup

### 9.1 Git installation

The recommended Git installation command was:

```bash
sudo apt install git -y
```

The confirmed transcript shows Git commands functioning, so Git was installed successfully.

### 9.2 Repository initialization

The repository was initialized inside the research directory:

```bash
git init
```

### 9.3 Why the virtual environment must not be committed

The Python virtual environment directory `venv/` must not be committed because:

- it can contain thousands of files;
- it is machine-specific;
- it bloats the repository;
- it slows or stalls `git add .`;
- it reduces portability;
- it duplicates what `requirements.txt` is supposed to represent cleanly.

The repository should track the environment specification, not the environment folder itself.

### 9.4 .gitignore

A `.gitignore` file was created and committed. It should contain at minimum:

```gitignore
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.env
.DS_Store
```

The initial commit showed:

```text
[master (root-commit) 0583459] initial environment
 1 file changed, 6 insertions(+)
 create mode 100644 .gitignore
```

### 9.5 Git identity error

The following Git identity error occurred:

```text
fatal: unable to auto-detect email address (got 'raha@raha-B450-I-AORUS-PRO-WIFI.(none)')
```

Root cause: Git did not yet know the user’s name and email identity for commits.

The local setup was fixed using `git config --global`. In a public reproducibility document, the email should be replaced with a placeholder:

```bash
git config --global user.name "Raha"
git config --global user.email "your-email@example.com"
```

The original private email address should not be included in a public repository document.

### 9.6 Confirmed commits

The following commits were confirmed.

Initial `.gitignore` commit:

```bash
git commit -m "initial environment"
```

Observed output:

```text
[master (root-commit) 0583459] initial environment
 1 file changed, 6 insertions(+)
 create mode 100644 .gitignore
```

Requirements file commit:

```bash
git add requirements.txt
git commit -m "add requirements file"
```

Observed output:

```text
[master 6ef512e] add requirements file
 1 file changed, 139 insertions(+)
 create mode 100644 requirements.txt
```

Branch rename:

```bash
git branch -m main
```

Project folder structure commit:

```bash
touch data/.gitkeep notebooks/.gitkeep src/.gitkeep results/.gitkeep
git add data/.gitkeep notebooks/.gitkeep src/.gitkeep results/.gitkeep
git commit -m "add project folder structure"
```

Observed output:

```text
[main db10808] add project folder structure
 4 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 data/.gitkeep
 create mode 100644 notebooks/.gitkeep
 create mode 100644 results/.gitkeep
 create mode 100644 src/.gitkeep
```

GPU sanity test commit:

```bash
git add test_gpu.py
git commit -m "add GPU sanity test"
```

Observed output:

```text
[main 29da214] add GPU sanity test
 1 file changed, 28 insertions(+)
 create mode 100644 test_gpu.py
```

### 9.7 Git cleanup warning

A Git garbage collection warning occurred:

```text
warning: The last gc run reported the following. Please correct the root cause
and remove .git/gc.log
Automatic cleanup will not be performed until the file is removed.

warning: There are too many unreachable loose objects; run 'git prune' to remove them.
```

It was resolved using:

```bash
git prune
rm -f .git/gc.log
git gc
git status
```

Observed successful cleanup:

```text
Enumerating objects: 10, done.
Counting objects: 100% (10/10), done.
Delta compression using up to 12 threads
Compressing objects: 100% (7/7), done.
Writing objects: 100% (10/10), done.
Total 10 (delta 0), reused 3 (delta 0), pack-reused 0
On branch main
nothing to commit, working tree clean
```

### 9.8 Final Git status

The repository ended in a clean state:

```bash
git status
```

Observed output:

```text
On branch main
nothing to commit, working tree clean
```

---

## 10. Project Directory Structure

The following directories were created:

```bash
mkdir data notebooks src results
```

Because Git does not track empty directories, placeholder files were added:

```bash
touch data/.gitkeep notebooks/.gitkeep src/.gitkeep results/.gitkeep
```

Final observed directory listing:

```text
data  notebooks  requirements.txt  results  src  venv
```

The intended structure is:

```text
research/
├── data/
│   └── .gitkeep
├── notebooks/
│   └── .gitkeep
├── results/
│   └── .gitkeep
├── src/
│   └── .gitkeep
├── requirements.txt
├── test_gpu.py
├── .gitignore
└── venv/                # ignored by Git
```

The `venv/` directory exists locally but is excluded from version control.

---

## 11. Reproducibility Rationale

Each setup choice improves reproducibility in a specific way.

### 11.1 Isolated Python environment

Using a virtual environment prevents uncontrolled mixing between system Python packages and project-specific packages.

Relevant command:

```bash
python3 -m venv venv
source venv/bin/activate
```

This allows the project’s Python dependencies to be installed, frozen, and recreated independently.

### 11.2 requirements.txt

The requirements file captures installed package versions:

```bash
pip freeze > requirements.txt
```

This provides a reproducible dependency snapshot for future setup.

### 11.3 Git version control

Git records code and configuration changes over time. This makes it possible to associate an experiment with a specific commit.

Relevant commands:

```bash
git init
git add requirements.txt
git commit -m "add requirements file"
```

### 11.4 .gitignore

The `.gitignore` prevents large, temporary, private, or machine-specific files from being committed. This keeps the repository portable.

### 11.5 Clean working tree

A clean working tree confirms that all intended files are committed and that no undocumented changes remain.

Verification:

```bash
git status
```

Expected output:

```text
nothing to commit, working tree clean
```

### 11.6 Hardware and GPU verification

GPU verification prevents a common failure mode where experiments silently run on CPU or use a misconfigured driver.

System-level verification:

```bash
nvidia-smi
```

Framework-level verification:

```python
import torch
print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))
```

### 11.7 Command-level documentation

Recording exact commands and outputs allows another researcher to reproduce not only the final state, but the route taken to reach it. This is critical for thesis appendices, supplementary material, and code review.

---

## 12. Troubleshooting Log

| Issue | Exact symptom/error | Root cause | Fix applied | Status |
|---|---|---|---|---|
| Ubuntu ISO uncertainty | User asked whether to copy ISO directly to USB | ISO must be flashed as bootable media, not copied as a normal file | Used Rufus to write ISO to USB | Resolved |
| Installer only showing smaller Windows SSD initially | Ubuntu installer showed limited “Install alongside” option | Simple installer mode did not provide full control over second disk | Switched to “Something else” manual partitioning | Resolved |
| Important files on 1 TB NTFS drive | User could not delete partition because it contained important files | Existing data partition occupied full disk | Shrunk partition safely in Windows Disk Management | Resolved |
| Need for Ubuntu space | No Linux partition existed yet | Ubuntu needed unallocated space | Freed approximately 400 GB and created ext4 `/` + swap | Resolved |
| Missing ensurepip | `The virtual environment was not created successfully because ensurepip is not available` | Common Ubuntu issue when `python3.10-venv` is missing | `sudo apt update`; `sudo apt install python3.10-venv`; recreate venv | Included as user-requested issue; not visible in final verified transcript |
| Virtual environment activation path missing | Activation would fail if `venv/bin/activate` did not exist | Virtual environment not created correctly | Recreate venv using `rm -rf venv`; `python3 -m venv venv`; activate again | Recommended; final environment active |
| `git add` appearing stuck or slow | Large directory additions can stall, especially if `venv/` is included | Virtual environment contains many files and should not be versioned | Add `venv/` to `.gitignore`; commit only environment specification | Resolved conceptually; `.gitignore` committed |
| Git identity unknown | `fatal: unable to auto-detect email address (got 'raha@raha-B450-I-AORUS-PRO-WIFI.(none)')` | Git username/email not configured | `git config --global user.name "Raha"`; `git config --global user.email "your-email@example.com"` | Resolved |
| Git garbage collection warning | `There are too many unreachable loose objects; run 'git prune'` | Git had unreachable loose objects from earlier operations | `git prune`; `rm -f .git/gc.log`; `git gc` | Resolved |
| Secure Boot / MOK | No confirmed error observed | Potential NVIDIA driver issue, but not encountered in verified output | No fix applied because no confirmed issue occurred | Not applicable / not observed |
| NVIDIA command typo | No confirmed `nvidea-smi` typo observed | Not applicable | Correct command used: `nvidia-smi` | Not applicable / not observed |

---

## 13. Final Verified State

The following items are confirmed working from the terminal output.

### 13.1 Operating system and shell context

- Ubuntu installed and running.
- Terminal available.
- Working directory: `~/research`.
- Active virtual environment shown by prompt: `(venv)`.

### 13.2 Python environment

Confirmed:

```text
Python 3.10.12
pip 26.0.1 from /home/raha/research/venv/lib/python3.10/site-packages/pip
```

### 13.3 GPU and PyTorch

Confirmed:

```text
NVIDIA GeForce RTX 3060
Driver Version: 580.126.09
CUDA Version reported by nvidia-smi: 13.0
PyTorch: 2.11.0+cu130
CUDA available: True
CUDA version used by PyTorch: 13.0
```

GPU computation test confirmed:

```text
Matrix multiplication completed on GPU.
Result shape: torch.Size([8000, 8000])
Time: 0.4135 seconds
GPU memory allocated: 0.72 GB
```

### 13.4 Git repository

Confirmed:

- Git repository initialized.
- Branch renamed to `main`.
- `.gitignore` committed.
- `requirements.txt` committed.
- project folder structure committed using `.gitkeep` files.
- GPU sanity test committed.
- Git cleanup performed.
- Final working tree clean.

Final status:

```text
On branch main
nothing to commit, working tree clean
```

---

## 14. Reproduction Instructions From Scratch

The following is a clean command sequence for reproducing the software environment on a new Ubuntu-based machine. Commands that modify disks or install the operating system are intentionally not included here because they depend on local disk layout and can be destructive if copied blindly.

### 14.1 System update

```bash
# Update package lists and upgrade installed packages
sudo apt update
sudo apt upgrade -y
```

### 14.2 Install required system tools

```bash
# Install Git, Python venv support, and basic build tools
sudo apt install git python3 python3-pip python3.10-venv build-essential -y
```

### 14.3 Create project directory

```bash
# Create and enter the research project directory
mkdir -p ~/research
cd ~/research
```

### 14.4 Create Python virtual environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Verify activation
which python
which pip
python --version
pip --version
```

Expected paths should point inside:

```text
~/research/venv/
```

### 14.5 Upgrade pip

```bash
pip install --upgrade pip
```

### 14.6 Install Python packages

For a clean recreation from an existing repository:

```bash
pip install -r requirements.txt
```

For a new minimal research environment, install core tools first:

```bash
pip install numpy pandas matplotlib scikit-learn jupyter torch torchvision torchaudio
pip freeze > requirements.txt
```

### 14.7 Verify NVIDIA GPU system detection

```bash
nvidia-smi
```

Recommended additional checks:

```bash
lsmod | grep nvidia
lspci -k | grep -A 3 -E "VGA|3D"
```

### 14.8 Verify PyTorch CUDA access

```bash
python - <<'PY'
import torch
print("PyTorch:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU:", torch.cuda.get_device_name(0))
    print("CUDA version used by PyTorch:", torch.version.cuda)
else:
    print("No GPU detected by PyTorch")
PY
```

### 14.9 Initialize Git repository

```bash
cd ~/research
git init
```

Configure identity. Use your own details; do not copy private credentials into public documentation.

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

### 14.10 Create .gitignore

```bash
cat > .gitignore <<'EOF'
venv/
__pycache__/
*.pyc
.ipynb_checkpoints/
.env
.DS_Store
EOF
```

### 14.11 Create project structure

```bash
mkdir -p data notebooks src results

touch data/.gitkeep notebooks/.gitkeep src/.gitkeep results/.gitkeep
```

### 14.12 Commit baseline environment

```bash
git add .gitignore requirements.txt data/.gitkeep notebooks/.gitkeep src/.gitkeep results/.gitkeep
git commit -m "initial reproducible environment setup"
git branch -m main
git status
```

Expected final output:

```text
On branch main
nothing to commit, working tree clean
```

### 14.13 Create GPU sanity test

```bash
cat > test_gpu.py <<'PY'
import torch
import time

print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())

if not torch.cuda.is_available():
    raise SystemExit("CUDA is not available. Stop here.")

device = torch.device("cuda")
print("GPU:", torch.cuda.get_device_name(0))

x = torch.rand((8000, 8000), device=device)
y = torch.rand((8000, 8000), device=device)

torch.cuda.synchronize()
start = time.time()

z = torch.matmul(x, y)

torch.cuda.synchronize()
end = time.time()

print("Matrix multiplication completed on GPU.")
print("Result shape:", z.shape)
print("Time:", round(end - start, 4), "seconds")
print("GPU memory allocated:", round(torch.cuda.memory_allocated() / 1024**3, 2), "GB")
PY
```

Run it:

```bash
python test_gpu.py
```

Commit it:

```bash
git add test_gpu.py requirements.txt
git commit -m "add GPU sanity test"
git status
```

---

## 15. Academic Quality Checklist

Before using this environment for thesis experiments or manuscript-level results, the following checklist should be completed.

### System and hardware

- [ ] OS version recorded using `lsb_release -a`.
- [ ] Kernel version recorded using `uname -a`.
- [ ] CPU recorded using `lscpu`.
- [ ] RAM recorded using `free -h`.
- [ ] Disk layout recorded using `lsblk -f`.
- [ ] GPU recorded using `nvidia-smi`.
- [ ] NVIDIA driver version recorded.
- [ ] CUDA version recorded from both `nvidia-smi` and PyTorch.
- [ ] cuDNN version recorded if used explicitly.

### Python and dependencies

- [ ] Python version recorded using `python --version`.
- [ ] pip version recorded using `pip --version`.
- [ ] `requirements.txt` generated using `pip freeze`.
- [ ] Dependency file committed to Git.
- [ ] Consider stronger lockfile strategy for final publication.

### Code and repository

- [ ] Git repository initialized.
- [ ] Branch renamed to `main`.
- [ ] `.gitignore` committed.
- [ ] Virtual environment excluded from Git.
- [ ] Datasets excluded from Git unless small and legally shareable.
- [ ] Model weights excluded from Git unless intentionally versioned using Git LFS or DVC.
- [ ] Every experiment associated with a Git commit hash.

### Data and experiments

- [ ] Dataset source documented.
- [ ] Dataset license documented.
- [ ] Dataset checksum recorded.
- [ ] Data preprocessing script versioned.
- [ ] Train/validation/test split documented.
- [ ] Patient-level split documented if medical imaging data are used.
- [ ] Leakage checks documented.
- [ ] Random seeds fixed and recorded.
- [ ] Experiment configuration saved.
- [ ] Results reproducible from clean clone.

### Reporting

- [ ] README.md created.
- [ ] Environment setup instructions included.
- [ ] Hardware and software versions included in methods or appendix.
- [ ] Limitations of reproducibility stated clearly.
- [ ] Final code archived with a DOI if submitting for publication.

---

## 16. Limitations and Next Steps

### 16.1 Current limitations

This setup is strong as a local research foundation, but it is not yet a complete publication-grade reproducibility package.

Remaining limitations:

- OS version was inferred from installation context but should be formally recorded from terminal output.
- CPU and RAM were stated but not independently logged from the system.
- No Dockerfile or container image exists yet.
- No Conda lockfile or fully pinned system-level environment exists yet.
- No README.md has been created yet.
- No dataset has been downloaded or documented.
- No experiment configuration system exists yet.
- No random seed policy has been implemented yet.
- No data leakage checks have been implemented yet.
- No model training pipeline has been created yet.
- No experiment tracking system has been configured yet.

### 16.2 Recommended next commands to record system state

Run and save outputs:

```bash
lsb_release -a
cat /etc/os-release
uname -a
lscpu
free -h
lsblk -f
nvidia-smi
python --version
pip --version
pip freeze > requirements.txt
```

Commit updated requirements if changed:

```bash
git add requirements.txt
git commit -m "update locked Python dependencies"
git status
```

### 16.3 Recommended next repository structure

Create additional folders before real experiments:

```bash
mkdir -p experiments configs logs models reports scripts

touch experiments/.gitkeep configs/.gitkeep logs/.gitkeep models/.gitkeep reports/.gitkeep scripts/.gitkeep
```

Recommended structure:

```text
research/
├── configs/
├── data/
├── experiments/
├── logs/
├── models/
├── notebooks/
├── reports/
├── results/
├── scripts/
├── src/
├── requirements.txt
├── README.md
└── test_gpu.py
```

### 16.4 Recommended README.md

A repository-level README should be created next and should include:

- project purpose;
- hardware specification;
- OS and Python version;
- setup commands;
- GPU verification commands;
- dependency installation instructions;
- dataset instructions;
- experiment execution instructions;
- reproducibility checklist.

### 16.5 Recommended environment setup script

A future script such as `scripts/setup_environment.sh` should automate non-destructive setup steps:

```bash
#!/usr/bin/env bash
set -e

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python test_gpu.py
```

The script should avoid destructive disk commands and should not install GPU drivers without explicit user review.

### 16.6 Recommended future reproducibility upgrades

For stronger publication-grade reproducibility, consider:

- Dockerfile with CUDA-compatible base image;
- Conda environment file or lockfile;
- DVC or Git LFS for large datasets and model weights;
- MLflow, Weights & Biases, or CSV-based experiment tracking;
- configuration files in YAML;
- fixed random seeds across Python, NumPy, and PyTorch;
- clean train/validation/test split scripts;
- dataset checksum validation;
- model checkpoint metadata;
- automated smoke test for GPU and training loop;
- final repository archive using Zenodo DOI.

---

## 17. Concluding Statement

The environment was successfully configured to support GPU-accelerated deep learning research on Ubuntu with an isolated Python virtual environment, Git-based version control, a documented project structure, a committed dependency snapshot, and verified PyTorch-CUDA execution on an NVIDIA GeForce RTX 3060.

The final verified state is suitable as a starting point for controlled machine learning experiments. However, publication-grade reproducibility will require further documentation of OS and hardware metadata, dataset provenance, deterministic training settings, experiment configuration files, leakage controls, and clean end-to-end reproduction instructions.
