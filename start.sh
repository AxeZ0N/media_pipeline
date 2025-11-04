#!/bin/bash

. "~/.bashrc"
cd "/media/k/General/Ryan/Desktop/Other/Code/Helpful/Media_Pipeline/"
"./watcher" &
"./pipeline"

echo "Script has finished." | read
