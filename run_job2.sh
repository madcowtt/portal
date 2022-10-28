#!/bin/bash

wechat=$1
email=$2
filecode=$3
pass=$4
docker=$5
notes="portal submission start"
output=""

case "$docker" in
	"tf_2.8") formal_docker_image="tensorflow/tensorflow:2.8.0-gpu-jupyter"
	;;
	"tf_2.7") formal_docker_image="tensorflow/tensorflow:2.7.0-gpu-jupyter"
	;;
	"tf_2.5") formal_docker_image="tensorflow/tensorflow:2.5.0-gpu-jupyter"
	;;
	"tf_2.0") formal_docker_image="tensorflow/tensorflow:2.0.0-gpu-jupyter"
	;;
	"tf_1.15") formal_docker_image="tensorflow/tensorflow:1.15.5-gpu-jupyter"
	;;
esac

#>>>>>>>>>>>>Manage docker>>>>>>>>>>>>>>>>>
docker container stop portalcont
docker container rm portalcont
docker run -it -d --gpus device=all --name portalcont -v /home/$4:/workspace/ $formal_docker_image
docker cp ~/dkr/client_code_wrapper3.py portalcont:/client_code_wrapper3.py
docker exec portalcont apt update
docker exec portalcont apt install -y python3-pip
docker exec portalcont pip install --no-cache-dir --upgrade pip

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

#execute a hello file
#docker exec test python3 /workspace/test.py

#log into portal table that submission was created
psqlcommand=$(arg1=$wechat;arg2=$email;arg3=$filecode;arg4=$pass;arg5=$notes;arg6=$output;echo "psql  -h 10.1.1.10 -p 5432 -d orweb -U portaladmin -c \"INSERT INTO portal_portalsubmitinfo(wechat_id,email,file_code,passphrase,str_notes,str_output,time) VALUES ('$arg1', '$arg2', '$arg3', '$arg4','$arg5','$arg6', (now() at time zone 'utc'));\"")
eval $psqlcommand

start=`date +%s`
#replace import statement for client code in wrapper file
filecode_nameonly=$(echo $filecode | sed -e 's/\.py//g')

docker exec portalcont cp /client_code_wrapper3.py /temp_client_code_wrapper3.py
docker exec portalcont sed -i "s/__clientfile__/$filecode_nameonly/g" /temp_client_code_wrapper3.py

filecode_path=/home/$pass/$filecode
if ! ( test -f "$filecode_path" ) ; then
    echo "$filecode_path does not exist."
    python3 sendEmail4.py $email error $filecode 0
    #docker exec test bash -c "echo '$filecode_path does not exist.' > /workspace/error.txt"
    notes="portal submission error, file $filecode_path not found"
    psqlcommand=$(arg1=$wechat;arg2=$email;arg3=$filecode;arg4=$pass;arg5=$notes;arg6=$output;echo "psql  -h 10.1.1.10 -p 5432 -d orweb -U portaladmin -c \"INSERT INTO portal_portalsubmitinfo(wechat_id,email,file_code,passphrase,str_notes,str_output,time) VALUES ('$arg1', '$arg2', '$arg3', '$arg4','$arg5','$arg6', (now() at time zone 'utc'));\"")
    eval $psqlcommand
    exit 0
fi

#>>>>>>>>>>>>Execute customer code>>>>>>>>>>>>>>>>>

docker exec portalcont python3 -m pip install -r /workspace/requirements.txt --log /workspace/python_package_install_log.txt

#docker exec portalcont sh /workspace/aibench.sh
docker exec portalcont python3 /temp_client_code_wrapper3.py 
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

end=`date +%s`

duration=$((end-start))
#output=$(printf '%dh:%dm:%ds\n' $((duration/3600)) $((duration%3600/60)) $((duration%60)))
output=$(printf '%dh:%dm\n' $((duration/3600)) $(((duration%3600 + 59)/60)) )
#output=$(printf '%dh\n' $(((duration+3599)/3600)) )

notes="portal submission end"

psqlcommand=$(arg1=$wechat;arg2=$email;arg3=$filecode;arg4=$pass;arg5=$notes;arg6=$output;echo "psql  -h 10.1.1.10 -p 5432 -d orweb -U portaladmin -c \"INSERT INTO portal_portalsubmitinfo(wechat_id,email,file_code,passphrase,str_notes,str_output,time) VALUES ('$arg1', '$arg2', '$arg3', '$arg4','$arg5','$arg6', (now() at time zone 'utc'));\"")
eval $psqlcommand


python3 sendEmail4.py $email finish $filecode $output

