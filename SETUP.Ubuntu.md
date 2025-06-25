# Basic VM (Ubuntu 20.04.6 Server LTS)
* CPU: 8
* MEM: 64G (=> 32G should be enough)
* Disk: 64G

# Local integration (Optional)
* Install 'devop-tools'
* setup-host-env -I -S

# Ansible (Optional)
* ROLE::AD-Member

# Follow instruction from Dockerfile
## Generic Part (root)
### 1. "RUN"
#### Remove Python (<3)
```
	apt-get remove -y python
```
#### Install needed packages
```
	apt-get install -y --no-install-recommends \
		git \
		build-essential \
		latexmk \
		texlive-latex-extra \
		libcurl4-openssl-dev \
		libfontconfig1-dev \
		libfreetype6-dev \
		libfribidi-dev \
		libgit2-dev \
		libharfbuzz-dev \
		libharfbuzz0b \
		libjpeg-dev \
		liblzma-dev \
		libopenblas-dev \
		libopenmpi-dev \
		libpng-dev \
		libssl-dev \
		libtiff5-dev \
		libv8-dev \
		libxml2-dev

```
### 2. "RUN"
#### Setup Python-3
```
	apt-get install -y --no-install-recommends \
		python3 \
		python3-dev \
		python3-tk \
		python3-venv \
		python3-pip
```
#### Prepare installation of 'setuptools' (HACK-1)
Install via APT to avoid compatibility issues
```
	apt-get install -y python3-testresources
```
#### Install 'setuptools' via 'pip3'
```
	pip3 install --no-cache-dir --upgrade setuptools
```
#### Python Link Magic
```
	echo "alias python='python3'" >> /root/.bash_aliases && \
	echo "alias pip='pip3'" >> /root/.bash_aliases && \
	cd /usr/local/bin && ln -s /usr/bin/python3 python && \
	cd /usr/local/bin && ln -s /usr/bin/pip3 pip
```
#### Install additional Python modules
```
	pip install --upgrade virtualenv wheel
```
#### Install ABED
```
	pip install --upgrade --use-pep517 abed
```
### Set the default shell to bash (3. "RUN")
```
	mv /bin/sh /bin/sh.old && cp /bin/bash /bin/sh
```

# SCHNIPP
## R Setup
### Add 'CRAN' repository
[Ubuntu Packages For R - Brief Instructions](https://cran.r-project.org/bin/linux/ubuntu/)
```
	apt-get install -y --no-install-recommends software-properties-common dirmngr && \
	wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc && \
	add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/" && \
	apt-get install -y --no-install-recommends r-base r-base-dev
```
# SCHNAPP

## Create user environment and switch user workspace (non-root)
```
	mkdir -p ~/local/workspace
	cd ~/local/workspace
```
### Clone the dataset repo (4. "RUN")
```
	git clone https://github.com/alan-turing-institute/TCPD
```
### Build the dataset (5. "RUN")
The following files need to be patched - unless the upstream REPO is updated:
* build_tcpd.py
* checksums.json
```
	cd TCPD && make export
```
### Clone the repo (6. "RUN")
```	
#	git clone --recurse-submodules https://github.com/alan-turing-institute/TCPDBench
	git clone --recurse-submodules git@github.com:mattiSPE/TCPDBench.git
```
### Copy the datasets into the benchmark dir (7. "RUN")
Instead of copy the whole dataset, just create sym-link
```	
	cd TCPDBench && ln -s ../TCPD/export ./datasets
```
### Install Python dependencies (8. "RUN")
```	
	sudo pip install --use-pep517 -r ./analysis/requirements.txt
```	
### Install R dependencies (9. "RUN")
```	
	sudo Rscript -e "install.packages(c('argparse', 'exactRankTests'))"
	sudo Rscript -e "install.packages('RcppEigen', repos = 'https://cran.r-project.org')"
```	


*** END ***




## Dokerfile
### Remove form APT
    r-base  ==> via PPA
	r-base-dev ==> via PPA
	r-cran-rcppeigen ==> via Rscript
		

## R Setup

### As 'root'
#### Add 'CRAN' repository
[Ubuntu Packages For R - Brief Instructions](https://cran.r-project.org/bin/linux/ubuntu/)
```
# update indices
apt update -qq
# install two helper packages we need
apt install --no-install-recommends software-properties-common dirmngr
# add the signing key (by Michael Rutter) for these repos
# To verify key, run gpg --show-keys /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc 
# Fingerprint: E298A3A825C0D65DFD57CBB651716619E084DAB9
wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc | tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
# add the repo from CRAN -- lsb_release adjusts to 'noble' or 'jammy' or ... as needed
add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/"
# install R itself
sudo apt install --no-install-recommends r-base```

apt install --no-install-recommends software-properties-common dirmngr
apt install r-base r-base-dev
Rscript -e "install.packages(c('argparse', 'exactRankTests'))"
Rscript -e "install.packages('RcppEigen', repos = 'https://cran.r-project.org')"

### As 'user'

### Removed from 'Rpackages.txt'

local:../R/wbs_1.4.tar.gz
wbs==1.4

## Additional Methodes

* [changeforest](https://github.com/mlondschien/changeforest)


