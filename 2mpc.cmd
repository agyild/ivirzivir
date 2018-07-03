@echo off
setlocal EnableDelayedExpansion

REM 2mpc v0.1 by agyild

REM This is a wrapper for youtube-dl written in Batch
REM that allows streaming various content via MPC-HC.

REM youtube-dl should be in path in order for it to work.
REM It will prefer x64 MPC-HC and if not found will fallback to x86. (did not test)

REM It doesn't do any error checking since it is just a simple wrapper.

REM Format selection is optimized for my personal taste (i.e. 1080p60/30)
REM but can be changed if one wishes to do so.

REM Usage:
REM 2mpc.cmd URL

REM MPC-HC detection
set MPCHC="%ProgramFiles%\MPC-HC\mpc-hc64.exe"
if not exist %MPCHC% (
    set MPCHC="%ProgramFiles(x86)%\MPC-HC\mpc-hc.exe"
    if not exist !MPCHC! (
        echo Error: MPC-HC has not been found.
        pause
        exit /b 1
    )
)

REM Quote workaround otherwise positional selectors may not work
set URL="%*"

REM Format selection
REM If URL looks like YT, it will use DASH and feed MPC-HC seperate streams
REM If it doesn't look like YT, it will feed MPC-HC a single container (generic)
REM If both fails it's probably some sort of stream format like HLS or something
REM in that case youtube-dl does the muxing and pipes it to MPC-HC
echo %URL% | find /i "youtube.com" > nul
if %ErrorLevel% equ 1 echo %URL% | find /i "youtu.be" > nul
if %ErrorLevel% equ 0 (
    for /f "tokens=* usebackq" %%a in (`youtube-dl -f "bestvideo[height<=?1440]" -g %URL%`) do set VIDURL="%%a"
    if defined VIDURL (
        for /f "tokens=* usebackq" %%a in (`youtube-dl -f bestaudio -g %URL%`) do set AUDURL="%%a"
        start "" %MPCHC% !VIDURL! /dub !AUDURL! /play /close & exit /b
    )
) else (
    for /f "tokens=* usebackq" %%a in (`youtube-dl -f "1080p_60fps/1080p_30fps/720p_60fps/bestvideo+bestaudio/best[height<=?1080]" -g %URL%`) do set VIDURL="%%a"
    if defined VIDURL (start "" %MPCHC% !VIDURL! /play /close)
)
if not defined VIDURL (start "" /min cmd /c youtube-dl -f "1080p_60fps/1080p_30fps/720p_60fps/bestvideo+bestaudio/best[height<=?1080]" %URL% -o - ^| %MPCHC% - /play /close)