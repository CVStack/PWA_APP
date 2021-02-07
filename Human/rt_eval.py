# -*- coding: utf-8 -*-
"""RT_eval.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/JaewonLee0217/PWA_APP/blob/AI_1/RT_eval.ipynb
"""

import torch
import torchvision
from torchvision import models
import torchvision.transforms as T

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

import glob
import os


def get_image_list(image_dir):
    if image_dir is not None:
        print("Loading images from directory : ", image_dir)
        images = glob.glob(image_dir + '/*.png')
        images += glob.glob(image_dir + '/*.jpg')
        images += glob.glob(image_dir + '/*.jpeg')

    else:
        raise RuntimeError('Either -img_dir arguments must be passed as argument')

    return images


def main():
  #이미지 사이즈 및 임계값 설정

  THRESHOLD = 0.95

  #model불러오기
  model = models.detection.keypointrcnn_resnet50_fpn(pretrained=True).eval()

  #예시(여기가 카메라-> frame (이미지) 로드 해서 동작)
  imgDir_path = 'images/'
  img = Image.open(get_image_list(imgDir_path)[0])
  print(get_image_list(imgDir_path))
  #임의의 thres 정의
  box_thres1 = img.size[0] * 0.45
  box_thres2 = img.size[0] * 0.55
  topthres_1 = img.size[1] * 0.35
  topthres_2 = img.size[1] * 0.55
  bottomthres = img.size[1] * 0.9

  

  #텐서로 변환
  trf = T.Compose([
      T.ToTensor()
  ])

  input_img = trf(img)
  out = model([input_img])[0]

  print(out)
  sen="인물 사진이 아닙니다."
  
  for box, score, keypoints in zip(out['boxes'], out['scores'], out['keypoints']):
    score = score.detach().numpy()

    if score < THRESHOLD:
      continue

    box = box.detach().numpy()

    #인물의 정가운데 지점 mid_box로 정의.
    mid_box = 0.5 * (box[0] + box[2])

    
    #y축 기준의 알고리즘
    keypoints = keypoints.detach().numpy()[:, :2]
    temp_face = keypoints[0][1]
    
    
    #keypoints[15],keypoint[16] 왼쪽 발목, 오른쪽 발목
    temp_leftfoot = keypoints[15][1]
    temp_rigthfoot = keypoints[16][1]
     
    
    if temp_face >topthres_1 and temp_face < topthres_2:
      if temp_leftfoot > bottomthres and temp_rigthfoot > bottomthres:
        sen = "좋아요!! 지금입니다 !! 사진을 찍어 주세요"
      else:
        sen = "발을 하단에 맞춰 주세요"
    else:
      sen = "얼굴을 가운데로 맞춰주세요"
    if mid_box <box_thres1:
      sen = "카메라 각도를 왼쪽으로 조금 돌려주세요"
    if mid_box >box_thres2:
      sen = "카메라 각도를 오른쪽으로 조금 돌려주세요"
      
    return sen





