#import sys
#这里输入需要多少视频
#num = int(sys.argv[1])

#输入视频需要多少秒
#time = int(sys.argv[2])

num=10
time=10
a=10
for i in range(0,num):
	a+=time+60
	print('ffmpeg -ss %s -t %s -y -i "${IN_DATA_DIR}/1.mp4" "${OUT_DATA_DIR}/%s.mp4"'%(a,time+1,i+1))