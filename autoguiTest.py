import pyautogui
import numpy as np
import cv2
import time
import os
import easyocr  # 필요한 경우 pip install easyocr 실행

temp_text_list = []
reader = easyocr.Reader(['ko', 'en'])

def is_text_present(image_path):
    # 추출한 텍스트 저장
    text = ""

    # EasyOCR 인식기 생성 (한글 언어 설정 추가)

    # 이미지에서 텍스트 추출
    results = reader.readtext(image_path)

    # 추출된 텍스트 출력
    for detection in results:
        text = detection[1]
        confidence = detection[2]

    # 텍스트 길이와 정확도로 텍스트 유무 판별
    if not text or confidence < 0.001:
        print("Text not found in image.")
        os.remove(image_path)
        print("Remove ", image_path)
        return None
    else:
        print("Extracted Text:", text)
        return text

def detect_wide_white_box():
    global temp_text_list

    # 전체 화면 크기 가져오기
    screen_width, screen_height = pyautogui.size()

    # 하단 30% 영역의 높이 계산
    bottom_height = int(screen_height * 0.3)

    # 전체 화면 캡처
    screenshot = pyautogui.screenshot(region=(0, screen_height - bottom_height, screen_width, bottom_height))
    screenshot_path = "./temp_screenshot.png"
    screenshot.save(screenshot_path)

    # 텍스트 추출
    text = is_text_present(screenshot_path)

    # 같은 텍스트가 추출된 사진 삭제 (중복 방지)
    if not text or text in temp_text_list:
        if os.path.exists(screenshot_path):
            print("Image that has already extracted subtitles.")
            os.remove(screenshot_path)
            print("Remove ", screenshot_path)
    else:
        # 추출한 텍스트 리스트에 저장
        if len(temp_text_list) > 3:
            temp_text_list.pop(0)
        if text:
            temp_text_list.append(text)

        # 하얀색 영역 찾기
        screenshot = cv2.imread(screenshot_path)
        lower_white = np.array([254, 254, 254])  # 변경된 하얀색의 RGB 값
        upper_white = np.array([255, 255, 255])
        mask = cv2.inRange(screenshot, lower_white, upper_white)

        # 하얀색 영역의 경계 찾기
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 하얀색 영역이 존재하는지 확인
        if len(contours) > 0:
            # 가장 큰 하얀색 영역 찾기
            max_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(max_contour)

            # 하얀색 영역의 가로 길이
            white_box_width = w
            white_box_height = h

            # 전체 화면 가로 길이의 70% 이상이면 감지 성공으로 처리
            if white_box_width >= 1400 and 120 < white_box_height < 135:
                # 초록색 네모로 영역 표시
                cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print("검출된 박스의 witdh:", white_box_width)
                print("검출된 박스의 높이:", white_box_height)

                # 영역이 표시된 화면 보여주기
                cv2.imshow("Detected White Box", screenshot)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                return True

    return False

if __name__ == "__main__":
    print("감지시작")
    while True:
        if detect_wide_white_box():
            print("전체 화면의 하단 30%에서 넓은 하얀색 박스를 감지하였습니다.")
