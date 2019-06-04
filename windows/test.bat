@echo off
echo Operating system:
ver|findstr /r /i " [版本 5.0.*]" > NUL && goto Windows2000
ver|findstr /r /i " [版本 5.1.*]" > NUL && goto WindowsXP
ver|findstr /r /i " [版本 6.1.*]" > NUL && goto Windows7
ver|findstr /r /i " [版本 10.0.*]" > NUL && goto Windows10
goto Unknow

:Windows2000
echo Windows 2000
REM clear RECYCLER.Bin
for %%p in (C D E F) do (
    if exist %%p:\RECYCLER (
        rd /s /q %%p:\RECYCLER
        echo %%p:\RECYCLER cleared!
    ) else (
        echo %%p:\RECYCLER not exist!
    )
    if exist %%p:\Recycled (
        rd /s /q %%p:\Recycled
        echo %%p:\Recycled cleared!
    ) else (
        echo %%p:\Recycled not exist!
    )
)
for %%u in (sd xsd casco stpc) do (
    net user %%u /del
)
net user Guest /active:no
echo.
echo confirm user deleted or disabled 禁用用户
pause
start lusrmgr.msc
echo.
echo set default username and password 设置默认用户
pause
start control userpasswords
echo.
echo running port disabled vb script 封闭端口
pause
start .\PortDisabled.vbs
pause
exit

:WindowsXP
echo Windows XP
pause
exit

:Windows7
echo Windows 7
pause
exit

:Windows10
echo Windows 10
pause
exit

:Unknow
echo Unknow
pause
exit