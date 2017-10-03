#!/bin/bash

user_id=1008
declare -a users=( "v.bugaevsky" "r.shavalieva" "d.zlochevskaya" )
for user in ${users[*]}; do
    groupadd --gid $user_id $user 
    useradd -m --gid $user_id --uid $user_id $user
    adduser $user sudo
    user_id=$(($user_id+1))
done

echo "===============DON'T FORGET TO RUN VISUDO==================="

for user in ${users[*]}; do
    echo 'export PATH="/opt/anaconda2/bin:$PATH"' >> /home/$user/.bashrc
    echo "$user ALL=(ALL) NOPASSWD: ALL"
done

echo 'Defaults        secure_path="/opt/anaconda2/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"'
