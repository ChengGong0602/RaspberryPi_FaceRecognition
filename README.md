# Auto Capture with Canon Camera on Raspberry Pi by using Face Detection

## Raspberry Pi initial configuration
````
sudo apt-get install gphoto2   
sudo apt-get install python3-pip   
sudo pip3 install sh   
gphoto2 
gphoto2 --auto-detect
gphoto2 --trigger-capture
kill number
````
## How to install mediapipe on Raspberry Pi
1. Install FFmpeg and OpenCV from official repository OR Build from sources using this Guide .
```sudo apt install ffmpeg python3-opencv python3-pip```

2. Install dependency packages   
```sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23```

3. Install package   
```sudo pip3 install mediapipe-rpi4```

````
sudo apt-get install libhdf5-dev -y 
sudo apt-get install libhdf5-serial-dev –y 
sudo apt-get install libatlas-base-dev –y 
sudo apt-get install libjasper-dev -y 
sudo apt-get install libqtgui4 –y
sudo apt-get install libqt4-test –y
````

## Gphoto2 configuration settings

Example to use: gphoto2 
````
gphoto2 --camera="Canon EOS 60D" --set-config viewfinder=1
gphoto2 --auto-detect --set-config=/main/capturesettings/shutterspeed=0
````
gphoto2 usage exmple:


gphoto2 configuration lists

- syncdatetime
- uilock
- autofocusdrive
- manualfocusdrive
- cancelautofocus
- eoszoom
- eoszoomposition
- viewfiner
- eosremoterelease
- opcode
- datetime
- reviewtime
- output
- movierecordtarget
- evfmode
- ownername
- artist
- copyright
- customfuncex
- focusinfo
- autopoweroff
- depthoffield
- capturetarget
- capture
- serialnumber
- manufacturer
- cameramodel
- deviceversion
- vendorextension
- model
- ptpversion
- batterylevel
- Battery level
- lensname
- eosserialnumber
- shuttercounter
- availableshots
- imageformat
- imageformatsd
- iso
- whitebalance
- whitebalanceadjusta
- whitebalanceadjustb
- whitebalancexa
- whitebalancexb
- colorspace
- focusmoe
- storageid
- autoexposuremode
- drivemode
- picturestyle
- aperture
- shutterspeed
- meteringmode
- bracketmode
- aeb


