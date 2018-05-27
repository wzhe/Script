#!/bin/bash

filePath=/home/pi/Public/TimeAudio
Time=`date +"%H"`
audioFile="$filePath/0$Time.mp3"
echo $audioFile
player=/usr/bin/mplayer

$player $audioFile
