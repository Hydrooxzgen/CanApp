@echo off
echo 注意，该功能需联网。
Powershell.exe "irm https://massgrave.dev/get | iex"
exit