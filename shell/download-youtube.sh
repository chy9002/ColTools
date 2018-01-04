youtube-dl -F "$*"
read -p "Please enter the desired quality # " FORMAT
youtube-dl -f $FORMAT "$*"
