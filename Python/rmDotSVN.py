import os
rootdir="D:\Users\wangzhe\Desktop\临时文件夹\2017.03.01_svn344_解决有时IP设不进eth2的问题"
for parent,dirnames,filenames in os.walk(rootdir):
    for filename in dirnames:  
        filepath = os.path.join(parent, filename)
        if os.path.isdir(filepath) and (not filepath.find('.svn') == -1):
            commnd = 'rd /S /Q ' + filepath
            os.system(commnd)
        #os.chmod(filepath, stat.S_IWRITE)
        #shutil.rmtree(filepath)
            print "dir "+filepath+" removed!"
