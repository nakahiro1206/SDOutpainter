import cv2

fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
video  = cv2.VideoWriter('upper.mp4', fourcc, 20.0, (1024+128, 1024+128))

init = cv2.imread("upper_input.png")
for _ in range(10):
    video.write(init)
for i in range(0,20):
    img = cv2.imread("upper"+str(i//10)+str(i%10)+".png")
    video.write(img); video.write(img)

res = cv2.imread("upper19.png")
for _ in range(10):
    video.write(res)

video.release()