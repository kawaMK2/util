import cv2
import numpy as np
import sys
import os


# 画像をクロマキー処理
def chroma_key(input_image, lower, upper):
    # 画像のBGRを分解
    BGR = cv2.split(input_image)

    if len(BGR) != 3:
        return 0

    # 青と赤に平均値を取る
    aveBR = cv2.addWeighted(BGR[0], 0.5, BGR[2], 0.5, 0)

    diffGB = cv2.absdiff(BGR[1], BGR[0])
    diffGR = cv2.absdiff(BGR[1], BGR[2])
    diffGBm = cv2.threshold(diffGB, lower, upper, cv2.THRESH_BINARY)[1]
    diffGRm = cv2.threshold(diffGR, lower, upper, cv2.THRESH_BINARY)[1]

    # 青と赤の平均値と緑の差を二値化
    diff = cv2.absdiff(BGR[1], aveBR)
    diffm = cv2.threshold(diff, lower, upper, cv2.THRESH_BINARY)[1]

    diff_tmp = cv2.bitwise_and(diffGRm, diffm)
    diff_final = cv2.bitwise_and(diff_tmp, diffGBm)

    # 画像のノイズ消去とマスク処理
    operator = np.ones((3, 3))
    dilate = cv2.dilate(diff_final, operator, iterations=4)
    mask = cv2.erode(dilate, operator, iterations=4)
    inv_mask = cv2.bitwise_not(mask)
    res1 = cv2.bitwise_and(input_image, input_image, mask=inv_mask)

    return cv2.bitwise_or(1, res1, mask)


if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) >= 2 else "."

    if len(sys.argv) != 2:
        print("Usage: # python %s dirname" % sys.argv[0])
        quit()

    if not os.path.exists("out"):
        os.mkdir("out")

    for filename in os.listdir(target_dir):
        path_in = os.path.join(target_dir, filename)
        img = cv2.imread(path_in, 1)

        out = chroma_key(img, 50, 255)

        if img is not None:
            cv2.imwrite("out/out_" + filename, out)

    print("done.")
