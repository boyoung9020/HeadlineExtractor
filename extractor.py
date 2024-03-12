import os
import time
import pyautogui
from PIL import ImageGrab
from PIL import Image
import easyocr
from datetime import datetime

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

def capture_and_save_screen(screenshot_path, reference_image_path):

    _, file = os.path.split(reference_image_path)

    # Compare the captured screen with the reference image
    try:
        location = pyautogui.locateOnScreen(reference_image_path, confidence=0.8)
        left, top, width, height = location

        # korean_news
        if file == "korean_news.png":
            pyautogui.screenshot(screenshot_path).crop((left + width + 10, top, left + 1530, top + 130 )).save(screenshot_path)
        # press_briefing, major_news
        elif file == "press_briefing.png" or file == "major_news.png":
            pyautogui.screenshot(screenshot_path).crop((left + width, top, left + 1530, top + 130 )).save(screenshot_path)
        else:
            pass

        # extract text from image
        if (os.path.exists(screenshot_path)):
            print(f"Screenshot saved at {screenshot_path}")
            return True
        else:
            print("Reference image matching failed.")
            return False
            
    except pyautogui.ImageNotFoundException as e:
        print("Reference image matching failed.")
        return False

# Set the path for the reference image and where to save the screenshots
# reference_image_path_list = ["korean_news.png", "major_news.png", "press_briefing.png"]
reference_image_path_list = os.listdir("reference")
save_directory = "temp\\"
temp_text_list = []
reader = easyocr.Reader(['ko', 'en'])


# Capture and save the screen every 10 seconds
while True:
    now = datetime.now()
    # screenshot_path = save_directory + now.strftime("%m%d%H%M%S") + ".png"

    for reference_image_path in reference_image_path_list:
        name, ext = os.path.splitext(reference_image_path)
        screenshot_path = os.path.join(save_directory, name, name + now.strftime("%m%d%H%M%S") + ext)

        dir, _ = os.path.split(screenshot_path)

        if not (os.path.exists(dir)):
            os.makedirs(dir)
        if capture_and_save_screen(screenshot_path, os.path.join("reference",reference_image_path)):
            text = is_text_present(screenshot_path)

            # 같은 텍스트가 추출된 사진 삭제 (중복 방지)
            if not text or text in temp_text_list:
                if os.path.exists(screenshot_path):
                    print("Image that has already extracted subtitles.")
                    os.remove(screenshot_path)
                    print("Remove ", screenshot_path)

            # 추출한 텍스트 리스트에 저장
            if len(temp_text_list) > 3:
                temp_text_list.pop(0)
            if text:
                temp_text_list.append(text)
        
    time.sleep(5)