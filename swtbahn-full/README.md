Need to install dependencies of displayIpAddress.py with a virtual environment to be able to run it.

Should work on a raspberry pi 5 (the buttons don't work though):

cd SWTbahn/swtbahn-pidisplay/swtbahn-full

sudo apt install libudev-dev vlc

// initiate virtual environment
python -m venv .venv4 --system-site-packages
// activate virtual environment
source .venv4/bin/activate

pip3 install ifaddr

#create .pythondeps folder if it does not exist yet (for a fresh install, delete it. To use the downloaded version, skip "git clone" step (but do the rest as written here))
mkdir .pythondeps && cd .pythondeps/

// install cap1xxx manually
git clone https://github.com/pimoroni/cap1xxx -b repackage
cd cap1xxx/
./install.sh --unstable // select "no" twice
cd ..

// install sn3218 manually
git clone https://github.com/pimoroni/sn3218-python
cd sn3218-python/
./install.sh --unstable // select "no" twice
cd ../../

pip3 install st7036
pip3 install python-uinput wifi spi urllib3 requests

pip3 install dot3k

// RPi.GPIO is installed when installing st7036 and dot3k -> apparently removing RPi.GPIO and installing rpi-lgpio alone does not work, even though I think the documentation says it *should* work. What does work if we just install rpi-lgpio later, i.e., here.
pip3 install rpi-lgpio

// replace file `<venv-name>/lib/python3.11/site-packages/dothat/backlight.py` with replacement file:

mv .venv4/lib/python3.11/site-packages/dothat/backlight.py .venv4/lib/python3.11/site-packages/dothat/backlight_old.py.txt

cp backlight.py .venv4/lib/python3.11/site-packages/dothat/