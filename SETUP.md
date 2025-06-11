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
- git clone https://github.com/alan-turing-institute/TCPD.git
- make export

## [TCPDBench](https://github.com/mattiSPE/TCPDBench)
- git clone git@github.com:mattiSPE/TCPDBench.git
- ln -s ../TCPD/export datasets

### Setup Python
- create sym-link for 'python' to 'python3'

Create 'master' venv for all further execution (make & abed), since the usage of 'pip' is blocked by Debian-12

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
