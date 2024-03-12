import os
import time
import pyautogui
from PIL import ImageGrab
from PIL import Image
from datetime import datetime

def is_text_present(image_path):
    # 추출한 텍스트 저장
    text = ""

    # EasyOCR 인식기 생성 (한글 언어 설정 추가)

    # 이미지에서 텍스트 추출

    # 추출된 텍스트 출력

    # 텍스트 길이와 정확도로 텍스트 유무 판별

def capture_and_save_screen(screenshot_path, x, y, width, height):
    try:
        # 캡처된 스크린 이미지를 저장합니다.
        pyautogui.screenshot(screenshot_path).crop((x, y, x + width, y + height)).save(screenshot_path)

        # 이미지가 정상적으로 저장되었는지 확인합니다.
        if (os.path.exists(screenshot_path)):
            print(f"Screenshot saved at {screenshot_path}")
            return True
        else:
            print("Failed to save the screenshot.")
            return False
            
    except Exception as e:
        print("Error occurred while capturing the screen:", e)
        return False

# 사각형 영역을 탐지하여 캡처하는 함수
def capture_rectangle_area(x, y, width, height):
    now = datetime.now()
    screenshot_path = f"temp\\{now.strftime('%Y%m%d%H%M%S')}.png"

    if capture_and_save_screen(screenshot_path, x, y, width, height):
        text = is_text_present(screenshot_path)

        # 추출한 텍스트 리스트에 저장
        if text:
            temp_text_list.append(text)

# Set the path for the reference image and where to save the screenshots
# reference_image_path_list = ["korean_news.png", "major_news.png", "press_briefing.png"]
reference_image_path_list = os.listdir("reference")
save_directory = "temp\\"
temp_text_list = []

# Capture and save the screen every 10 seconds
while True:
    for reference_image_path in reference_image_path_list:
        name, ext = os.path.splitext(reference_image_path)
        reference_image = os.path.join("reference", reference_image_path)

        # 사각형 영역의 좌표와 크기 설정
        x, y, width, height = 100, 100, 200, 200  # 예시로 설정된 값입니다. 필요에 따라 수정하세요.

        capture_rectangle_area(x, y, width, height)
        
    time.sleep(5)
