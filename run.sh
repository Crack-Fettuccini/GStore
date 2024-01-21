#!/bin/bash

#coloring format is \hex_for_esc[ text_type; text_color letter_m
BoldCyanBlack='\033[1;36;40m\033[K'
Normalize='\033[0;0;40m\033[K'
Green='\033[1;32;40m\033[K'
Full='\033[K'
UserInfo() {
    echo -e "${BoldCyanBlack}$1${Normalize}" | pv -qL 40
}
#on macos install pv using
#brew install pv
#on macos install setsid using
#brew install util-linux
if [ -f "credentials.txt" ]; then
    source "credentials.txt"
else
  echo "Write your helper email credentials to credentials.txt"
fi
export signed_cookie="thisisthesecretkey"
export PYTHONDONTWRITEBYTECODE=1
UserInfo "Creating virtual environment..."
python3 -m venv GStorevenv
UserInfo "Virtual environment created"

echo -e "\n${BoldCyanBlack}Activating virtual environment...${Normalize}" | pv -qL 40
source ./Gstorevenv/bin/activate
echo -e "${Green}Virtual environment activated${Normalize}" | pv -qL 40

echo -e "\n${BoldCyanBlack}Installing project dependecies for Flask API...${Normalize}" | pv -qL 40
pip3 install -r requirements.txt -q -q -q
echo -e "${Green}Flask API dependencies installed${Normalize}" | pv -qL 40

echo -e "\n${BoldCyanBlack}Installing dependencies for Vue...${Normalize}" | pv -qL 40
npm --prefix gstorefront install
echo -e "${Green}Vue dependencies installed${Normalize}" | pv -qL 40

echo -e "\n${BoldCyanBlack}Starting redis server...${Normalize}" | pv -qL 40
redis-server --daemonize yes &
sleep 3

echo -e "\n${BoldCyanBlack}Changing directory to 'Grocery Store'...${Normalize}" | pv -qL 40
cd "$(dirname "$0")"
echo -e "${Green}Current directory changed to $(pwd)${Normalize}" | pv -qL 40

#echo -e "\n${BoldCyanBlack}Checking for registered files...${Normalize}" | pv -qL 40
#celery -A GStore.CeleryTasks.celery inspect registered
#sleep 3

echo -e "\n${BoldCyanBlack}Starting Celery worker and Beat scheduler for CronJobs...${Normalize}" | pv -qL 40
celery -A GStore.CeleryTasks.celery worker -B &
sleep 3

echo -e "\n${BoldCyanBlack}Starting Flask API Backend Server...${Normalize}" | pv -qL 40
python3 app.py &
sleep 3

echo -e "\n${BoldCyanBlack}Starting Vue application...${Normalize}" | pv -qL 40
npm --prefix gstorefront run serve

#use the next two lines if you are planning on using production server for application instead of the line above
#npm --prefix gstorefront run build
#serve -s gstorefront/dist

echo -e "\n${BoldCyanBlack}Termination signal received...${Normalize}" | pv -qL 40

#ps aux|grep 'celery worker'
#ps auxww | grep 'celery worker' | awk '{print $2}' | xargs kill -9
#find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

#this kills only in macos, unverified for linux systems
echo -e "\n${BoldCyanBlack}Killing Celery Workers...${Normalize}" | pv -qL 40
pkill -f "celery worker"
while pgrep -f "celery worker" > /dev/null; do
    sleep 1
done
echo "${Green}Killed Celery Workers${Normalize}" | pv -qL 40

echo -e "\n${BoldCyanBlack}Killing Flask processes...${Normalize}" | pv -qL 40
pkill -9 -f "app.py"
while pgrep -f "app.py" > /dev/null; do
    sleep 1
done
echo "${Green}Killed Flask processes${Normalize}" | pv -qL 40

echo -e "\n${BoldCyanBlack}Shutting down redis server...${Normalize}" | pv -qL 40
redis-cli shutdown
echo "${Green}Redis server shut down${Normalize}" | pv -qL 40
echo "${Green}Application terminated successfully${Normalize}" | pv -qL 40