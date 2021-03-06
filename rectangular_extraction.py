import cv2
import numpy as np

class RectangularExtraction:
    def __init__(self, resizesize, offset):
        self.resize = resizesize
        self.offset = offset

    def rectangular_extraction(self, src):
        extract_feature = []
        print(src)
        src_movie = cv2.VideoCapture(src)

        ret, frame = src_movie.read()
        while ret:
            self.detect_contour(frame)
            ret, frame = src_movie.read()
            try:
                detected_image = self.detect_contour(frame)
            except:
                continue
            resizeddetected = cv2.resize(detected_image, (30,60))
            feature_frame = np.reshape(resizeddetected, (1800,))

            # cv2.imwrite("tmp_contourarea.jpg", bw)
            # cv2.imshow('output', resizeddetected)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
            extract_feature.append(feature_frame)

        print("feature generated", np.shape(extract_feature))
        extract_feature = self.use_multiple_time_frame_feature(
            feature=extract_feature,
            t=2
        )
        print("feature generated", np.shape(extract_feature))
        return extract_feature

    # n-frame feature -> one feature
    # TODO apply this code for n value
    def use_multiple_time_frame_feature(self, feature, t=2):
        if t == 2:
            multiple_feature = [np.append(feature[i-1], x) for i, x in enumerate(feature)]
            multiple_feature = np.delete(multiple_feature, 0, 0)
            return multiple_feature

        elif t==3:
            multiple_feature = [np.append(feature[i-2], feature[i-1], x) for i, x in enumerate(feature)]
            multiple_feature = np.delete(multiple_feature, [0,1], 0)
            return multiple_feature

    #TODO gray scale の時に画像が３チャネルになってしまっているのを１ちゃねるだけにしておきたい
    def detect_contour(self, src, use_gray_image=False):
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        retval, bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # print("gray", np.shape(gray))

        # cv2.imwrite("tmp_contourarea.jpg", bw)
        # cv2.imshow('output', bw)
        # cv2.waitKey()
        # cv2.destroyAllWindows()

        # 輪郭を抽出
        #   contours : [領域][Point No][0][x=0, y=1]
        #   cv2.CHAIN_APPROX_NONE: 中間点も保持する
        #   cv2.CHAIN_APPROX_SIMPLE: 中間点は保持しない
        #     print(cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE))
        # image, contours, hierarchy = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        image, contours, retval = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # 矩形検出された数（デフォルトで0を指定）
        detect_count = 0
        # 各輪郭に対する処理
        human_pixel = []
        for i in range(0, len(contours)):
            # 外接矩形
            if len(contours[i]) > 0:
                rect = contours[i]
                x, y, w, h = cv2.boundingRect(rect)
                human_pixel.append([x, y, x + w, y + h])

        x1 = np.min(np.array(human_pixel).T[0]) - self.offset
        y1 = np.min(np.array(human_pixel).T[1]) - self.offset
        x2 = np.max(np.array(human_pixel).T[2]) + self.offset
        y2 = np.max(np.array(human_pixel).T[3]) + self.offset

        # cv2.rectangle(src, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # 外接矩形毎に画像を保存
                # cv2.imwrite(str(detect_count) + '.jpg', src[y:y + h, x:x + w])
                # detect_count = detect_count + 1

        # 外接矩形された画像を表示
        # if use_gray_image is True:
        # else:
        #     cut_img = gray[y1: y2, x1: x2]
            # cut_img = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)

        cut_img = src[y1: y2, x1: x2]
        cut_img = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)

        return cut_img
