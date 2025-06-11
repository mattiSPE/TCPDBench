# Basic VM (Debian-12)
# Ansible 
* ROLE::AD-Member

# Additional Packages
- git
- python3-pip
- python3-virtualenv
- python3-venv (!!!)
- libopenmpi-dev
- r-recommended
- texlive
- texlive-latex-extra
- latexmk

# Additional Installations
## [TCPD](https://github.com/alan-turing-institute/TCPD)
There's a small patch for 'build_tcpd.py' which will avoid reloading of a particular dataset, in case it's already existing:
```
def collect_dataset(name, script):
-    return run_dataset_func(name, script, "collect")
+    dir_path = os.path.join(DATASET_DIR, name)
+    dataset_path = os.path.join(dir_path, f"{name}.json")
+    if not os.path.exists(dataset_path):
+        return run_dataset_func(name, script, "collect")
+    return None
```
In addition, the file 'checksums.json' might need to be changed/extended to reflect the current MD5 checksums of the downloaded datasets.
 
- git clone https://github.com/alan-turing-institute/TCPD.git
- make export

## [TCPDBench](https://github.com/mattiSPE/TCPDBench)
- git clone git@github.com:mattiSPE/TCPDBench.git
- ln -s ../TCPD/export datasets

### Setup Python
Create 'master' venv for all further execution (make & abed), since the usage of 'pip' is blocked by Debian-12 and MacOS doesn't allow 'global' symlink for 'python' which is provided by the 'venv' in addition to symlink for 'pip' as well.

- python3 -m venv .venv && source .venv/bin/activate
- pip install -r ./analysis/requirements.txt

### Setup R
- sudo apt install apt libxml2-dev libssl-dev libcurl4-openssl-dev (some more ...)
- sudo Rscript -e "install.packages(c('argparse', 'exactRankTests'))"

## Make results
- make results

## Setup [abed](https://gjjvdburg.github.io/abed/usage/installation.html)
- pip install abed
- 

## Make venvs
- sudo apt install libfontconfig1-dev
- sudo apt install libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev  (some more ...)
- make venvs
