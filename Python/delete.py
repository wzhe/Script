import os

f = open("delete_file.txt", "r")
while True:  
	line = f.readline().upper().replace('\n','')
	if line:  
		print line
                cmd = "rm -rf " + line
                print cmd
                os.system(cmd)
	else:  
		break 
