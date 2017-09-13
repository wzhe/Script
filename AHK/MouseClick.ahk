#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
;#NoTrayIcon
Gui, Color, EEAA99
Gui +LastFound ; Make the GUI window the last found window for use by the line below.
WinSet, TransColor, EEAA99 
gui, font,, Arial
gui, font, s30 
Gui, Add, Text, ,Please select the area,F10 Exit!
Gui, Add, Button, ,OK
Gui +Resize
Gui, Show, AutoSize Center
return

ButtonOK:
	WinGetPos, X, Y, Width, Height, 
	MsgBox, Will Click in %X%`,%Y%`,%Width%`,%Height%
	WinMinimize 
	;MsgBox,  % "Click on " . X + Width . "."
	loop {
	Random, time1, 500, 1000
	Sleep %time1%
	Random, m1, % X , % X + Width 
	Random, m2, % Y , % Y + Height
	CoordMode, Mouse, Screen  ; Place ToolTips at absolute screen coordinates:
	MouseMove, %m1%, %m2%
	Sleep 10
	Click 2
	;MsgBox, Click on %m1%, %m2%
	}
	return
F10::
	msgbox,4000,退出成功,你已退出鼠标点击器！,1
	ExitApp
GuiClose:
ExitApp