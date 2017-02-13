::for %%i in (1,2,3,4,5,6,7,8,9,10,11,12) do (
::set /p a=
::echo %%i
::)


:start
cls
scrapy crawl ershoufang
set /p ans=
goto  start

:end
pause
exit