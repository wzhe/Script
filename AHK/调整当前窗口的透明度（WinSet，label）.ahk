;CREATER: Mzp_Drkp2017
;
;���shift+�����ֵ�������͸���ȣ�����30-255��͸���ȣ�����30�����ϾͿ������ˣ�����Ҫ�������޸ģ�2016.09.20.by M.��2017.01.11__1635 edit again.M��
;edit by wzhe 2017-10-28
;
;ʹ��˵����
;   �����shift+�����»�������͸���ȣ�һ��10
;   �����shift+�����ϻ�������͸���ȣ�һ��20
;   �����shift+�м����£��ָ�͸������255(��ȫ��͸��).
;
~LShift & WheelUp::
; ͸���ȵ��������ӡ�
WinGet, Transparent, Transparent,A
If (Transparent="")
	Transparent=255
	;Transparent_New:=Transparent+10
	Transparent_New:=Transparent+20    ;��͸���������ٶȡ�
	If (Transparent_New > 254)
					Transparent_New =255
	WinSet,Transparent,%Transparent_New%,A

	tooltip now: ��%Transparent_New%`nmae: __%Transparent%  ;�鿴��ǰ͸���ȣ�����֮��ģ���
	;sleep 1500
	SetTimer, RemoveToolTip_transparent_Lwin, 1500  ;����ͳһ�������ʽ��label�����
return

~LShift & WheelDown::
;͸���ȵ��������١�
WinGet, Transparent, Transparent,A
If (Transparent="")
	Transparent=255
	Transparent_New:=Transparent-10  ;��͸���ȼ����ٶȡ�
	;msgbox,Transparent_New=%Transparent_New%
			If (Transparent_New < 30)    ;����С͸�������ơ�
					Transparent_New = 30
	WinSet,Transparent,%Transparent_New%,A
	tooltip now: ��%Transparent_New%`nmae: __%Transparent%  ;�鿴��ǰ͸���ȣ�����֮��ģ���
	;sleep 1500
	SetTimer, RemoveToolTip_transparent_Lwin, 1500  ;����ͳһ�������ʽ��label�����
return

;����Lwin &Mbuttonֱ�ӻָ�͸���ȵ�255��
~Lshift & Mbutton::  
WinGet, Transparent, Transparent,A
WinSet,Transparent,255,A  
tooltip ��Restored ;�鿴��ǰ͸���ȣ�����֮��ģ���
;sleep 1500
SetTimer, RemoveToolTip_transparent_Lwin, 1500  ;����ͳһ�������ʽ��label�����
return


Removetooltip_transparent_Lwin:     ;LABEL
tooltip
SetTimer, RemoveToolTip_transparent_Lwin, Off
return
