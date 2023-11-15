Instructions (These are not finalized, let me know what should be changed).

Create a xfa directory in home, copy xfa.service and xfa.py into that direcotry. 

NOTE: The file xfa.py and xfa.service has user definable values! You'll most likly have to updates these!
Make sure the working directory is xfa.py is correct. You might also need to update the file paths and/or names if you're not using the same ones I am.
Make sure under [Service} the user and path in xfa.service is correct. Otherwise the service will not automaticlly start when the pi is started.

Run the following commands in same directory you downloaded xfa in:
```
sudo cp xfa.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable xfa.service
sudo systemctl start xfa.service
```
All three LEDs should be lit up in a sequence. Signifying the scipt is running correctly and is waiting on user input!
The system should automaticly start this way for now on. No need to SSH into the pi anymore! (Unless you want to debug something).

* Press B1 to program an OpenXenium Chip from start to finish.
* Press B2 to program an OpenXenium Chip starting with flashing the memory chip.
* Press B3 to program an OpenXenium Chip finished programming the CPLD with the actual OpenXenium software.
* B4 initiates a safe shutdown of the pi. Once the pi's activity LED is off, it's safe to remove power.



Green LED means programming successful

Yellow LED means that it's in process of programming.

	Fast blink means Programming via JTAG.
	Slow blink means Programming via LPC.

Red LED means programming failed.

	Fast blink means JTAG Error.
	Slow blink means LPC\TSOP Error.
	

Logs can be found at /tmp/xfa.log(If you want to follow the log in realtime, run: tail -f /tmp/xfa.log)

-Andr0
Rev.6

------Change Log--------
Rev .1 - Initial Release

Rev .2 - Utilize more buttons, cleaned up code.

Rev .5 - Das Blicken Edition! 

Rev .6 - Look Ma! I'm on GitHub now!
