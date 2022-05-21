# SIM7000_console
Code to test AT commands with SIM7000 ESP32 module from Thonny console or command line<br>
uses microPython<br><br>
Enter the command ```CTRL-START``` to start/restart the SIM module<br><br>
By default a \r (CR) character is added at the end of your command before sending<br>
Add ```<ncr>``` to the end of the command if you desire NOT to send a \r (CR) at the end<br>
Example: ```+++<ncr>``` to send only the + characters without CR<br><br>
Enter ```<cr>``` To only send \r (CR). All other data on line will be ignored<br>
Enter ```<eof>``` to send the EOF \x1A character<br><br>


Tested with LilyGO TTGO T-SIM7000G<br><br>
Notes:<br>
Some commands (like +++) require a 1 sec no data before sending and a 1 sec delay before sending \r.<br>
Therefore there are 1 sec delays in de code before the entered command is send and 1 sec before the \r characters are send.<br>
