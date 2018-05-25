  #NoTrayIcon
    ; <COMPILER: v1.0.47.6>  
    ;一天 24小时，1440分，86400秒  
    ;一周 168小时，10080分，604800秒  
    ;30天  750小时，43200分，2592000秒  
    ;365天  8760小时，525600分，31536000秒    
        CustomColor =   ff3301
        Gui, +AlwaysOnTop +LastFound +Owner  
        Gui, Color, %CustomColor%  
        gui, font,, Arial
        gui, font, s30 
        Gui, Add, Text, vMyText cff3300,  w600 XXXXX YYYYY  
        WinSet, TransColor, %CustomColor% 255  
		WinSet, Bottom,, Disable 
        Gui, -Caption  
        SetTimer,UpdateOSD,3600000
        Gosub,UpdateOSD  
        Gui, Show, x1630 y980
      
        UpdateOSD: 
        time=%A_MM%月%A_DD%日%A_DDD%
        ;time2=%A_Hour%:%A_Min%:%A_Sec% 
        ;GuiControl,,MyText,%time%,time2
		GuiControl,,MyText,%time%
        
F10::
msgbox,4100,退出成功,你已退出时间！,1
exitapp
        return
;参照图片，其中① ②处为时间字体颜色代码和边缘颜色代码，根据喜好可以随意更改。
;③处为时间界面的坐标位置，根据屏幕可以自行更改。
;④处为退出时间的快捷键，这里设置按下F10，退出这个时间程序。