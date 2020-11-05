import sys
from copy import deepcopy
import queue
from collections import deque
import csv
import torch
import cv2
import datetime
import numpy as np
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pathlib import Path

from time import time
from tqdm import tqdm
from pyKiinectv2_github import PyKinectRuntime, PyKinectV2

# KETI 제공 사항
from GUI_utils.CONSTANTS import (
    # PLAY
    PLAY_TICK_INTERVAL,
    # FILES
    RGB_FOLDER_NAME, DEP_FOLDER_NAME,
    # GUI
    EVENT_KR2ID, CAMERA_INFO_DEP, CAMERA_INFO_RGB, QImage_2D, QImage_3D, MODE_DEP, MODE_RGB, CLASSFICATION_BOX_THRESH,
    ACTION_SHOW_COUNTER, ACTION_SHOW_WITH_DETECTCOUNTER, ACTION_SHOW_KR2MAXIMUMSHOW, ACTION_SHOW_KR2ABOVEDETECT,
    ACTION_DETECT_COUNTER, ACTION_SHOW_WITH_SHOWCOUNTER,
    # Flags
    TICKWISE_FLAG_KEYS, FLAG_PEOPLE_CHANGED, FLAG_DIM_LIGHT, FLAG_DANGER_ZONE, FLAG_CNN_DETECTED,
    VIDEOWISE_KEYVAL_LIST, LAST_YOLO_DET, LAST_BOX_APPEAR,
    DIM_LIGHT_THRESH,

    # RULE people counting
    PEOPLE_HISTOGRAM, PEOPLE_HISTOGRAM_BINS, MAX_HISTOGRAM, OLD_N_AVERAGE_PEOPLE, NEW_N_AVERAGE_PEOPLE,
    EVENT_KR_apper, EVENT_KR_disappear, EVENT_KR_videosignalout,
    EVENT_KR_roam, EVENT_KR_dispose, EVENT_KR_punch, EVENT_KR_kick, EVENT_KR_fall, EVENT_KR_gather, EVENT_KR_gatherbeat, EVENT_KR_destruct,
    # RULE danger zone
    EVENT_KR_dangerzone
)
from GUI_utils.miscs import make_DEP_colormap, get_matched_file_in_dir
from GUI_utils.switch_widget import SwitchButton


SHOW_PBAR = True
_DEBUG = False


def dprint(*args, **kwargs):
    if _DEBUG:
        print(*args, **kwargs)


class MyWindow(QWidget):
    tickwise_flagdict = None

    def _tick_video(self):
        curtime = time()
        tickcwise_flagdict = self.get_tickwise_flagdict()

        if curtime < self.timerNextTick:
            return

        if self.live_or_stored == "live" and not self.kinect.has_new_color_frame():
            return

        self.timerNextTick = curtime + PLAY_TICK_INTERVAL

        if self.live_or_stored == "stored":
            _, depfrm_raw = self.vidcap_dep.read()
            _, rgbfrm_raw = self.vidcap_rgb.read()
            dep_ubyte1 = depfrm_raw[..., 0]
        else:
            depfrm_bytes = self.kinect.get_last_depth_frame()
            rgbfrm_bytes = self.kinect.get_last_color_frame()
            dep_ubyte2 = np.array(depfrm_bytes, np.uint16,
                                  copy=False).reshape((424, 512))
            dep_ubyte1 = (dep_ubyte2 / 256).astype(np.uint8)
            rgbfrm_raw = np.array(rgbfrm_bytes, np.uint8, copy=False).reshape(
                (1080, 1920, 4))[..., :3]
            rgbfrm_raw = cv2.resize(rgbfrm_raw, (640, 360))
            depfrm_raw = np.stack((dep_ubyte1, dep_ubyte1, dep_ubyte1), -1)

        dep_colormap = make_DEP_colormap(dep_ubyte1).copy()
        rgbfrm_half = cv2.resize(rgbfrm_raw, (640, 360))
        self._tick_setPixmap(dep_colormap, rgbfrm_half)

        if SHOW_PBAR:
            self.pbar.update()

        if self.live_or_stored == "stored":
            time_now = datetime.datetime.now()
            time_span = datetime.timedelta(seconds=5)
            time_bef = time_now - time_span
            if self.frm_cnt >= self.n_frames:
                self.editor2.appendPlainText("[{start} ~ {end}]   Event : {act_name}".format(
                    start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                    act_name=EVENT_KR_videosignalout))
                self.textedit.setText(EVENT_KR_videosignalout)
                self.tick_video_timer.stop()
                self.btnFileLoad.setEnabled(True)
                self.color_depth_switch.setEnabled(True)
                if SHOW_PBAR:
                    self.pbar.close()

            else:
                pass

        # KETI 알고리즘과 연결 부분
        tickcwise_flagdict[FLAG_CNN_DETECTED] = True
        action_kr_name = '나타남'

        if (
                tickcwise_flagdict[FLAG_CNN_DETECTED] or
                tickcwise_flagdict[FLAG_PEOPLE_CHANGED] or
                tickcwise_flagdict[FLAG_DANGER_ZONE]):

            show_action = self.manage_action_show(action_kr_name)

            if show_action:

                if (('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_roam or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_dispose or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_punch or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_kick or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_fall or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_dangerzone or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_gather or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_gatherbeat or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_destruct or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_dangerzone or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_videosignalout or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_apper or
                        ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_disappear):
                    self.videowise_values[LAST_BOX_APPEAR] = self.frm_cnt
                    self.textedit.clear()
                    textFont2 = QtGui.QFont()
                    textFont2.setPointSize(30)
                    textFont2.setFamily("맑은고딕")
                    self.textedit.setFont(textFont2)
                    self.textedit.setStyleSheet("font-weight: bold;"
                                                "color:red;"
                                                "background-color:rgb(242,242,242);")

                    self.textedit.setText(
                        '위장\n' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name)
                    self.textedit.setAlignment(QtCore.Qt.AlignCenter)

                time_now = datetime.datetime.now()
                time_span = datetime.timedelta(seconds=5)
                time_bef = time_now - time_span

                if self.m_CNN == MODE_DEP:
                    cam_info_template = CAMERA_INFO_DEP
                else:
                    cam_info_template = CAMERA_INFO_RGB

                if (('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_roam or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_dispose or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_punch or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_kick or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_fall or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_dangerzone or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_gather or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_gatherbeat or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_destruct or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_dangerzone or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_videosignalout or
                    ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_apper or
                        ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_disappear):
                    self.editor1.appendPlainText(cam_info_template.format(
                        start_time=time_bef.strftime("%Y:%m:%d:%H:%M:%S"),
                        end_time=time_now.strftime("%Y:%m:%d:%H:%M:%S"),
                        eventid=EVENT_KR2ID[action_kr_name]))

                global results
                results = (cam_info_template.format(
                    start_time=time_bef.strftime("%Y:%m:%d:%H:%M:%S"),
                    end_time=time_now.strftime("%Y:%m:%d:%H:%M:%S"),
                    eventid=EVENT_KR2ID[action_kr_name]) + "\n")
                f = open("./ActionRecognition.txt", 'a')
                f.write(results)
                f.close()

                if ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_roam:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_dispose:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_punch:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_kick:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_fall:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_gather:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_gatherbeat:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_destruct:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_dangerzone:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_videosignalout:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_apper:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))
                elif ('위장_' + action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name) == EVENT_KR_disappear:
                    self.editor2.appendPlainText("[{start}~{end}] Event : [{act_name}] R_Frame: [{frame_number}] GT_Frame: [{gt_number}]".format(
                        start=time_bef.strftime("%H:%M:%S"), end=time_now.strftime("%H:%M:%S"),
                        act_name='위장_' +
                        action_kr_name if tickcwise_flagdict[FLAG_DIM_LIGHT] else action_kr_name,
                        frame_number=self.frm_cnt, gt_number=" "))

    def manage_action_show(self, action_kr_name):
        if action_kr_name is None:
            return False

        action_detect_counter = self.videowise_values[ACTION_DETECT_COUNTER]
        action_show_counter = self.videowise_values[ACTION_SHOW_COUNTER]
        action_detect_counter[action_kr_name] += 1
        action_detect_count = action_detect_counter[action_kr_name]
        action_show_count = action_show_counter[action_kr_name]
        show_action = True
        if ACTION_SHOW_WITH_DETECTCOUNTER:
            tmp_show_flag = False
            if action_detect_count >= ACTION_SHOW_KR2ABOVEDETECT[action_kr_name]:
                tmp_show_flag = True
            show_action = show_action and tmp_show_flag
        if ACTION_SHOW_WITH_SHOWCOUNTER:
            tmp_show_flag = False
            if ACTION_SHOW_KR2MAXIMUMSHOW[action_kr_name] < 0 or action_show_count < ACTION_SHOW_KR2MAXIMUMSHOW[
                    action_kr_name]:
                tmp_show_flag = True
            show_action = show_action and tmp_show_flag
        if show_action:
            action_show_counter[action_kr_name] += 1
        return show_action

    def _tick_setPixmap(self, dep_colormap, rgbfrm_raw):
        dep_colormap = dep_colormap[..., ::-1].copy()
        dep_qimage = QImage(dep_colormap, dep_colormap.shape[1], dep_colormap.shape[0],
                            QImage.Format_RGB888)
        dep_pixmap = QPixmap(dep_qimage)
        dep_pixmap = dep_pixmap.scaled(800, 550)
        dep_pixmap = dep_pixmap.transformed(QTransform().scale(-1, 1))
        self.label_depth.setPixmap(dep_pixmap)
        rgbfrm_raw = rgbfrm_raw[..., ::-1].copy()
        rgb_qimage = QImage(rgbfrm_raw, rgbfrm_raw.shape[1], rgbfrm_raw.shape[0],
                            QImage.Format_RGB888)
        rgb_pixmap = QPixmap(rgb_qimage)
        rgb_pixmap = rgb_pixmap.scaled(800, 550)
        rgb_pixmap = rgb_pixmap.transformed(QTransform().scale(-1, 1))
        self.label_color.setPixmap(rgb_pixmap)

    def btnclicked_stopVideo(self):
        self.tick_video_timer.stop()
        self.btnFileLoad.setEnabled(True)
        self.color_depth_switch.setEnabled(True)
        if SHOW_PBAR:
            self.pbar.close()

        if self.live_or_stored == "live":
            self.kinect.close()

    def __init__(self):
        super().__init__()
        self.setupUI()
        self.tick_video_timer = QTimer()
        self.tick_video_timer.timeout.connect(self._tick_video)

        self.show()

    def exam_dep_or_rgb_mode(self):
        cond1 = self.color_depth_switch.value is False and self.color_depth_switch.offtxt == 'Depth Map Image'
        cond2 = self.color_depth_switch.value is True and self.color_depth_switch.ontxt == 'Depth Map Image'
        if cond1 or cond2:
            self.m_YOLO = self.m_CNN = MODE_DEP
            self.mode = MODE_DEP
        else:
            self.m_CNN = self.m_YOLO = MODE_RGB
            self.mode = MODE_RGB

    def setupUI(self):
        # window 생성되는 위치 및 크기 설정
        self.setGeometry(40, 40, 1920, 1080)

        # background color 설정
        bkPal = QPalette()
        bkPal.setColor(QPalette.Background, Qt.white)
        self.setPalette(bkPal)

        # 전체 레이아웃 선언
        dlgLayout = QVBoxLayout()

        # 위쪽 레이아웃 선언
        topLayout = QHBoxLayout()
        topTmpLayout = QVBoxLayout()

        # 중간 비디오 레이아웃 선언
        colorLayout = QVBoxLayout()
        depthLayout = QVBoxLayout()
        videoLayout = QHBoxLayout()

        # 중간 에디터 레이아웃 선언
        metadataLayout = QVBoxLayout()
        historyLayout = QVBoxLayout()
        editLayout = QHBoxLayout()

        # 중간 커버(비디오+에디터) 레이아웃 선언
        corverLayout = QVBoxLayout()

        # 메뉴 레이아웃 선언
        menuLayount = QHBoxLayout()
        menubtnVLayout = QVBoxLayout()
        menubtnHLayout = QHBoxLayout()
        menubtnVLayout2 = QVBoxLayout()
        menubtnHLayout2 = QHBoxLayout()

        # 메뉴 서브 레이아웃 선언
        menuSubLayount = QVBoxLayout()

        # 위쪽 로고 및 제F/B출금이체목
        oImage = QImage("_image/logo2.png")
        logo = QLabel()
        logo.setPixmap(QPixmap(oImage))
        topLayout.addWidget(logo)
        topTmpLayout.addLayout(topLayout)

        # 위쪽 제목
        d2Image = QImage("_image/3D.png")
        self.d2 = QLabel()
        self.d2.setPixmap(QPixmap(d2Image))
        self.d2.setFixedHeight(35)
        topTmpLayout.addWidget(self.d2)

        # 중간 컬러 및 뎁스 영상 제목 선언
        ltImage = QImage("_image/LTSubject.png")
        LTsub = QLabel()
        LTsub.setPixmap(QPixmap(ltImage))
        LTsub.setFixedHeight(35)

        rtImage = QImage("_image/RTSubject.png")
        RTsub = QLabel()
        RTsub.setPixmap(QPixmap(rtImage))
        RTsub.setFixedHeight(35)

        # 중간 컬러 및 뎁스 영상 윈도우 선언
        self.label_color = QLabel()
        self.label_depth = QLabel()
        self.label_color.setScaledContents(True)
        self.label_depth.setScaledContents(True)

        im_np_color = np.ones((1080, 1920, 3), dtype=np.uint8)
        im_np_depth = np.ones((424, 512, 3), dtype=np.uint8)

        qimage_color = QImage(
            im_np_color, im_np_color.shape[1], im_np_color.shape[0], QImage.Format_RGB888)
        pixmap_color = QPixmap(qimage_color)
        pixmap_color = pixmap_color.scaled(800, 550)
        self.label_color.setPixmap(pixmap_color)

        qimage_depth = QImage(
            im_np_depth, im_np_depth.shape[1], im_np_depth.shape[0], QImage.Format_RGB888)
        pixmap_depth = QPixmap(qimage_depth)
        pixmap_depth = pixmap_depth.scaled(800, 550)
        self.label_depth.setPixmap(pixmap_depth)

        # 비디오 레이아웃에 컬러,뎁스 윈도우 및 제목 추가
        colorLayout.addWidget(LTsub)
        colorLayout.addWidget(self.label_color)
        depthLayout.addWidget(RTsub)
        depthLayout.addWidget(self.label_depth)

        videoLayout.addLayout(colorLayout)
        videoLayout.addLayout(depthLayout)

        # 메타데이터, 액션 히스토리 에디터 제목 선언

        lbImage = QImage("_image/LBSubject.png")
        LBsub = QLabel()
        LBsub.setPixmap(QPixmap(lbImage))
        LBsub.setFixedHeight(35)

        rbImage = QImage("_image/RBSubject.png")
        RBsub = QLabel()
        RBsub.setPixmap(QPixmap(rbImage))
        RBsub.setFixedHeight(35)

        # 메타데이터, 액션 히스토리 에디터 선언
        self.editor1 = QPlainTextEdit()
        self.editor2 = QPlainTextEdit()
        self.editor1.setReadOnly(True)
        self.editor2.setReadOnly(True)
        self.editor1.setFixedHeight(400)
        self.editor2.setFixedHeight(400)

        editor1Font = QtGui.QFont()
        editor1Font.setPointSize(14)
        self.editor1.setFont(editor1Font)

        editor2Font = QtGui.QFont()
        editor2Font.setPointSize(14)
        editor2Font.setFamily("돋움")
        self.editor2.setFont(editor2Font)

        # 에디터 레이아웃에 에디터 및 제목 추가
        metadataLayout.addWidget(LBsub)
        metadataLayout.addWidget(self.editor1)
        historyLayout.addWidget(RBsub)
        historyLayout.addWidget(self.editor2)

        editLayout.addLayout(metadataLayout)
        editLayout.addLayout(historyLayout)

        # 커버 레이아웃에 [2D/3D]제목, 비디오, 에디터 레이아웃 추가
        corverLayout.addLayout(videoLayout)
        corverLayout.addLayout(editLayout)

        # 메뉴 콘텐츠 폰트 정의
        menuFont = QtGui.QFont()
        menuFont.setPointSize(12)
        menuFont.setFamily("맑은고딕")

        # 메뉴 이름 1
        cpImage = QImage("_image/ControlPanel.png")
        cpMenu = QLabel()
        cpMenu.setPixmap(QPixmap(cpImage))
        cpMenu.setFixedHeight(35)

        # 메뉴 시스템 연결 버튼
        self.btnSysConn = QPushButton('System Connection')
        self.btnSysConn.setFont(menuFont)
        self.btnSysConn.setFixedHeight(40)
        self.btnSysConn.setFixedWidth(220)
        self.btnSysConn.setStyleSheet("font-weight: bold;")

        # 메뉴 프로그램 초기화 버튼
        self.btnInit = QPushButton('Initialization')
        self.btnInit.setFont(menuFont)
        self.btnInit.setFixedHeight(40)
        self.btnInit.setFixedWidth(220)
        self.btnInit.setStyleSheet("font-weight: bold;")

        # 메뉴 버튼 추가 1
        menubtnVLayout2.addWidget(self.btnSysConn)
        menubtnVLayout2.addWidget(self.btnInit)
        btnTmp3 = QLabel(" ")
        menubtnHLayout2.addWidget(btnTmp3, 0)
        menubtnHLayout2.addLayout(menubtnVLayout2)

        # 메뉴 이름 2
        stImage = QImage("_image/InputType.png")
        txtMenu = QLabel()
        txtMenu.setPixmap(QPixmap(stImage))
        txtMenu.setFixedHeight(35)

        # 메뉴 제목 이미지 (LiveVideo)
        lvImage = QImage("_image/LiveVideo.png")
        lvMenu = QLabel()
        lvMenu.setPixmap(QPixmap(lvImage))
        lvMenu.setFixedHeight(35)

        # 메뉴 제목 이미지 (StoredVideo)
        svImage = QImage("_image/StoredVideo.png")
        svMenu = QLabel()
        svMenu.setPixmap(QPixmap(svImage))
        svMenu.setFixedHeight(35)

        # 메뉴 체크박스1
        checkBox_livevideo = QCheckBox("Live Video")
        checkBox_livevideo.setFont(menuFont)
        ckTmp1 = QLabel(" ")
        ckTmp3 = QLabel(" ")
        checkBox_livevideo.setStyleSheet("font-weight: bold;")
        self.checkBox_livevideo = checkBox_livevideo

        # 메뉴 체크박스2
        checkBox_storedvideo = QCheckBox("Stored Video")
        checkBox_storedvideo.setFont(menuFont)
        ckTmp4 = QLabel(" ")
        checkBox_storedvideo.setStyleSheet("font-weight: bold;")
        self.checkBox_storedvideo = checkBox_storedvideo

        # 메뉴 컬러 뎁스 스위치
        self.color_depth_switch = SwitchButton(
            self, "2D Image", 15, "Depth Map Image", 165 - 75, 218)
        swTmp1 = QLabel(" ")

        # 메뉴 영상불러오기 버튼
        btnTmp1 = QLabel(" ")
        self.btnFileLoad = QPushButton('Video Selection')
        self.btnFileLoad.setFont(menuFont)
        self.btnFileLoad.clicked.connect(self.btnclicked_load_storedVideo)
        self.btnFileLoad.setFixedHeight(40)
        self.btnFileLoad.setFixedWidth(220)
        self.btnFileLoad.setStyleSheet("font-weight: bold;")

        # 메뉴 영상 멈추기 버튼
        self.btnStop = QPushButton('Video Stop')
        self.btnStop.clicked.connect(self.btnclicked_stopVideo)
        self.btnStop.setFont(menuFont)
        self.btnStop.setFixedHeight(40)
        self.btnStop.setFixedWidth(220)
        self.btnStop.setStyleSheet("font-weight: bold;")

        # 메뉴 영상 플레이 버튼
        self.btnPlay = QPushButton('Live Play')
        self.btnPlay.clicked.connect(self.btnclicked_load_liveVideo)
        self.btnPlay.setFont(menuFont)
        self.btnPlay.setFixedHeight(40)
        self.btnPlay.setFixedWidth(220)
        self.btnPlay.setStyleSheet("font-weight: bold;")

        # 메뉴 버튼 추가 2
        menubtnVLayout.addWidget(self.color_depth_switch)
        menubtnVLayout.addWidget(swTmp1, 0)
        menubtnVLayout.addWidget(self.btnFileLoad)
        menubtnVLayout.addWidget(self.btnStop)
        menubtnVLayout.addWidget(self.btnPlay)

        btnTmp2 = QLabel(" ")
        menubtnHLayout.addWidget(btnTmp2, 0)
        menubtnHLayout.addLayout(menubtnVLayout)

        # 메뉴 이름 2
        arImage = QImage("_image/ActionEvent.png")
        txtAct = QLabel()
        txtAct.setPixmap(QPixmap(arImage))
        txtAct.setFixedHeight(35)

        # 메뉴 액션 예측 에디터 (액션 예측 결과 표출하는 곳)
        self.textedit = QLabel(self)
        self.textedit.setFrameShape(QFrame.Panel)
        self.textedit.setFixedHeight(190)
        self.textedit.setFixedWidth(235)
        text_font = QtGui.QFont()
        text_font.setPointSize(25)
        text_font.setFamily("맑은고딕")
        self.textedit.setFont(text_font)
        self.textedit.setAlignment(QtCore.Qt.AlignCenter)
        self.textedit.setStyleSheet(
            "font-weight: bold;"
            "color:red;"
            "border: 1px solid gray;"
            "background-color:rgb(242,242,242);")

        # 메뉴 분석 결과 반출 이미지
        areImage = QImage("_image/AnalysisExport.png")
        areMenu = QLabel()
        areMenu.setPixmap(QPixmap(areImage))
        areMenu.setFixedHeight(35)

        # 메뉴 분석 결과 반출 버튼
        self.btnAE = QPushButton('Video Analysis \nResult Export')
        self.btnAE.setFont(menuFont)
        self.btnAE.setFixedHeight(80)
        self.btnAE.setFixedWidth(235)
        self.btnAE.setStyleSheet("font-weight: bold;")

        # tmp 위젯
        txtTmp1 = QLabel(" ")
        txtTmp2 = QLabel(" ")
        # 메뉴 콘텐츠 추가

        menuSubLayount.addWidget(cpMenu, Qt.AlignTop)  # fixed

        menuSubLayount.addWidget(ckTmp3, 0)
        menuSubLayount.addLayout(menubtnHLayout2, Qt.AlignTop)  # fixed
        menuSubLayount.addWidget(ckTmp3, 0)

        menuSubLayount.addWidget(txtMenu, Qt.AlignTop)  # fixed

        menuSubLayount.addWidget(lvMenu, Qt.AlignTop)  # fixed
        menuSubLayount.addWidget(ckTmp3, 0)
        menuSubLayount.addWidget(checkBox_livevideo, Qt.AlignTop)  # fixed
        menuSubLayount.addWidget(ckTmp1, 0)
        menuSubLayount.addWidget(svMenu, Qt.AlignTop)  # fixed
        menuSubLayount.addWidget(ckTmp4, 0)
        menuSubLayount.addWidget(checkBox_storedvideo, Qt.AlignTop)  # fixed

        menuSubLayount.addWidget(btnTmp1, 0)

        menuSubLayount.addLayout(menubtnHLayout, Qt.AlignTop)  # fixed

        menuSubLayount.addWidget(txtTmp1, 26)  # 26

        menuSubLayount.addWidget(txtAct, Qt.AlignTop)
        menuSubLayount.addWidget(self.textedit, Qt.AlignTop)  # fixed

        menuSubLayount.addWidget(txtTmp2, 2)

        menuSubLayount.addWidget(areMenu, Qt.AlignBottom)
        menuSubLayount.addWidget(self.btnAE, Qt.AlignBottom)

        # 메뉴 레이아웃에 추가
        menuLayount.addLayout(corverLayout)
        menuLayount.addLayout(menuSubLayount)

        # 앞에서 설정된 레이아웃을 메인 레이아웃(dlgLayout)에 추가
        dlgLayout.addLayout(topTmpLayout)
        dlgLayout.addLayout(menuLayount)
        self.setLayout(dlgLayout)

    def btnclicked_load_liveVideo(self):
        self.exam_dep_or_rgb_mode()
        self.reset_videowise_values()
        self.live_or_stored = "live"

        # 제목 바꾸기
        if not self.color_depth_switch.value:
            self.d2.setPixmap(QPixmap(QImage_3D))
        else:
            self.d2.setPixmap(QPixmap(QImage_2D))

        kinect_sources = PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Depth
        self.kinect = PyKinectRuntime.PyKinectRuntime(kinect_sources)

        self.n_frames = None
        self.reset_values()
        self.tick_video_timer.start()
        self.checkBox_storedvideo.setChecked(False)
        self.checkBox_livevideo.setChecked(True)
        if SHOW_PBAR:
            self.pbar = tqdm()

    def btnclicked_load_storedVideo(self):
        self.exam_dep_or_rgb_mode()
        self.reset_videowise_values()
        self.live_or_stored = "stored"
        dialog = QFileDialog(self, 'Select a videofile', r'.\DEP')
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog_ret = dialog.exec_()
        if dialog_ret == QDialog.Rejected:
            return

        avipath = Path(dialog.selectedFiles()[0])
        # 제목 바꾸기
        if not self.color_depth_switch.value:
            self.d2.setPixmap(QPixmap(QImage_3D))
        else:
            self.d2.setPixmap(QPixmap(QImage_2D))

        if "DEP" in str(avipath).upper():
            vidpath_dep = avipath
            vidpath_rgb = Path(str(avipath).replace(
                DEP_FOLDER_NAME, RGB_FOLDER_NAME))

        elif "RGB" in str(avipath).upper():
            vidpath_rgb = avipath
            vidpath_dep = Path(str(avipath).replace(
                RGB_FOLDER_NAME, DEP_FOLDER_NAME))
        else:
            self.n_frames = 0
            return

        dprint('Load: {} and {}'.format(vidpath_rgb, vidpath_dep))
        self.vidcap_rgb = cv2.VideoCapture(str(vidpath_rgb))
        self.vidcap_dep = cv2.VideoCapture(str(vidpath_dep))

        n_frames_rgb = self.vidcap_rgb.get(cv2.CAP_PROP_FRAME_COUNT)
        n_frames_dep = self.vidcap_dep.get(cv2.CAP_PROP_FRAME_COUNT)

        assert n_frames_dep == n_frames_rgb, "{} vs. {} n_frames_dep={}, n_frames_rgb={}".format(vidpath_rgb, vidpath_dep,
                                                                                                 n_frames_dep, n_frames_rgb)

        self.n_frames = n_frames_dep

        dprint('self.n_frames', self.n_frames)
        self.reset_values()
        self.tick_video_timer.start()
        self.checkBox_storedvideo.setChecked(True)
        self.checkBox_livevideo.setChecked(False)
        if SHOW_PBAR:
            self.pbar = tqdm(total=self.n_frames)

    def get_tickwise_flagdict(self):
        if self.tickwise_flagdict is None:
            self.tickwise_flagdict = dict(
                zip(TICKWISE_FLAG_KEYS, [False, ] * len(TICKWISE_FLAG_KEYS)))
        return deepcopy(self.tickwise_flagdict)

    def reset_videowise_values(self):
        self.videowise_values = {}
        for keyval in VIDEOWISE_KEYVAL_LIST:
            key, val = keyval
            self.videowise_values[key] = deepcopy(val)

    def reset_values(self):
        self.timerNextTick = -999.

        self.frm_cnt = 0
        self.btnFileLoad.setEnabled(False)
        self.color_depth_switch.setEnabled(False)

        self.editor2.clear()
        self.editor1.clear()
        self.textedit.setText('')


def main():

    app = QApplication(sys.argv)
    mywindow = MyWindow()
    mywindow.setWindowTitle('2D/3D Action Recognition System')
    mywindow.setWindowIcon(QIcon('_image/keti_icon.ico'))

   # 윈도우 크기 최대화
    mywindow.showMaximized()
    app.exec_()


if __name__ == "__main__":
    main()
