@echo off
TITLE 激活Windows脚本
echo 注意，该功能需联网。
pause
Powershell.exe "irm https://massgrave.dev/get | iex"
exit