# goatupdate

This script auto-update your debian distribution with `apt update` and `apt upgrade`

## Configuration

For use the script just add in the end of your bashrc  `python3 /path/to/goatupdate/goatupdate.py /path/to/goatupdate/`. 
With this line, when you start a terminal, the script run and verify if you have update your system today. Else he exec update and upgrade.
If you want add other command for update. For example pacman just add issues. 

I created this script for personal use but decided to publish it 
