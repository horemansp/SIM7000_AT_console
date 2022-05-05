# SIM7000_console
Code to test AT command with SIM7000 ESP module from Thonny console<br>
uses microPython<br>
Add "<rn>" to the end of the command if you desire to send a \r\n<br>
Example: AT+COPS?<rn><br>
Enter "CTRL-START" to restart the SIM module<br>
Enter "CTRL-Z" to send the EOF \x1A character<br><br>
Tested with LilyGO TTGO T-SIM7000G<br><br>
Notes:<br>
Some commands (like +++) require a 1 sec no data before sending and a 1 sec delay before sending \r\n.<br>
Therefore there are 1 sec delays in de code before the entered command is send and 1 sec before the \r\n characters are send.<br>
