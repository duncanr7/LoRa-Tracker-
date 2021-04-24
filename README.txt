The folder called "previous_work" contains code that worked a older version of  
circuit python and thus had to be updated if you have questions about that 
please contact David ('fand.kanade@gmail.com'). For questions about the "new_work"
folder contact Ryan ('duncanr7@udayton.edu').

Project Goal 
- Send data from Feather M0 RFM9x to LoRa device that will be displayed on webpage 

- Use GPS receiver to begin testing range of device 


Setting up Laird system 
	
	Username - BIGDAWG
	Password - Ud4yton!

	You will need to create an account on TTN (The Things Network ) to get this 
	up and running. The quick start guide should be everything you need to get it
	started. Note that only up to page 18 is useful. 

Setting up Feather M0 RFM9x

	Project Programs  

	- For the new work being done we suggest two programs to be downloaded 
		- Mu - is a simple code editor that is designed for circuit python 
	if you want to use other code editors such as VScode this is possible but not 
	recommended 

		-Bossa- This is how we load circuit python onto the device. Since this
	feather is one of the new original ones it relies on bin files to load circuit 
	python onto the board. Bossa is the program that is used to do this, note this 
	device has the ATSAMD21 chip so the offset should be 0x2000. Please see resources 
	to find article explaining this in more detail. BE CAREFUL IF THIS IS NOT DONE 
	CORRECTLY IT WILL BRICK THE DEVICE AND NO LONGER WILL BE USEFUL !!!!!!!


Resources Used

Feather M0 RFM9x - More detail documentation around device, https://learn.adafruit.com/adafruit-feather-m0-radio-with-lora-radio-module/pinouts 

Ultimate GPS breakout - https://learn.adafruit.com/adafruit-ultimate-gps-featherwing/circuitpython-library 

Python Code to connect device to TTN - https://learn.adafruit.com/using-lorawan-and-the-things-network-with-circuitpython?view=all

In depth look into m0 RFM9x page 66,67 for communication in python - https://www.mouser.com/datasheet/2/737/adafruit-feather-m0-radio-with-lora-radio-module-1395898.pdf

Setting up the MO RFM9x - note this shouldn’t need to be done if version 6.1.0 is still
the latest version out. https://learn.adafruit.com/welcome-to-circuitpython/installing-mu-editor

Quick Start Guide for Laird system -https://assets.lairdtech.com/home/brandworld/files/Quick%20Start%20Guide%20-%20Sentrius%20RG1xx.pdf
