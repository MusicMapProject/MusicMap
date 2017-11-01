FROM nvidia/cuda:8.0-cudnn7-devel-ubuntu16.04
MAINTAINER Vladimir Bugaevsky <bugaevsky@mail.ru>

# install common dependencies
RUN apt-get update -y && apt-get install -y sudo vim less python wget git screen liblua5.2 \
    libgconf-2-4 fontconfig libglu1-mesa

# install anaconda
RUN . ~/.bashrc && wget https://repo.continuum.io/archive/Anaconda2-4.4.0-Linux-x86_64.sh -O ~/Anaconda2.sh && \
    bash ~/Anaconda2.sh -b -p "/opt/anaconda2" && \
    echo 'export PATH="/opt/anaconda2/bin:$PATH"' >> ~/.bashrc && \
    rm ~/Anaconda2.sh

# install avbin
RUN . ~/.bashrc && wget https://github.com/downloads/AVbin/AVbin/install-avbin-linux-x86-64-v10 -O ~/avbin.sh && \
    bash ~/avbin.sh && rm ~/avbin.sh

# install python packages
ADD requirements.txt .
RUN apt-get update -y && apt-get install -y python-cffi libfontconfig1-dev libfreetype6-dev
RUN . ~/.bashrc && pip install -r requirements.txt && rm requirements.txt

# install pytorch
RUN . ~/.bashrc && conda install pytorch torchvision cuda80 -c soumith
RUN . ~/.bashrc && conda install -c conda-forge ffmpeg

# Set normal TZ (mostly for logs)
RUN ln -sf /usr/share/zoneinfo/Europe/Moscow /etc/localtime 
