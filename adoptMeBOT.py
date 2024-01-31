import time
import os

import cv2
import numpy as np
import sys

from PIL import ImageGrab

output_code = {"Look": "#Looking# ",
               "Fail": "#No-Tasks# ",
               "Found": "#Success# ",
               "Act": " |   #Action# ",
               "Wait": "=Waiting= ",
               "Earn": "$Earning$ "}


def check_if_task_found(img_rgb, task_name, do_print=True):
    template = cv2.imread(sys.path[0] + "\\pics\\" + task_name + ".png")

    w, h = template.shape[:-1]

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = .85
    loc2 = cv2.findNonZero((res >= threshold).astype('uint8'))

    print(loc2)

    if do_print:
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):  # Switch columns and rows
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imwrite('result.png', img_rgb)

    if loc2 is not None:
        return task_name

    return "None"


def main():
    # sleep is 16 sec
    # eat/drink is 8 sec
    # shower is 13 sec
    total_earned = 0
    possible_tasks = ["drink", "eat", "shower", "play"]

    print("Time Format- 00:00:00")
    duration_str = input("How Long Do You Want The Program To Run: ")

    splited_duration = duration_str.split(':')

    seconds = int(splited_duration[2])
    mins = int(splited_duration[1])
    hours = int(splited_duration[0])

    duration = seconds + (60 * mins) + (3600 * hours)

    start_time = time.time()
    while (time.time() - start_time) < duration:
        # Define the coordinates of the region you want to capture
        x1, y1, x2, y2 = 1252, 97, 1667, 164  # Change these values as per your region of interest

        # Take a screenshot of the specified region
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

        print(output_code["Look"]+"Looking For Tasks!")
        print()
        # Save the screenshot to a file
        screenshot.save("screenshot.png")
        time.sleep(2)

        img_rgb = cv2.imread(sys.path[0] + "\screenshot.png")

        for task in possible_tasks:
            time.sleep(1)
            task_found = check_if_task_found(img_rgb, task)

            if task_found != "None":
                print(output_code["Found"] + task_found + " Task Found!")
            else:
                print(output_code["Fail"] + "Didnt Not Find "+task)

            if task_found == "drink":
                print(output_code["Act"] + "Pet Is Drinking!")
                os.startfile(sys.path[0] + "\\actions\\" + task_found + ".exe")
                time.sleep(12)
                print(output_code["Act"] + "Pet Is Done Drinking!")
                total_earned += 10

            elif task_found == "eat":
                print(output_code["Act"] + "Pet Is Eating!")
                os.startfile(sys.path[0] + "\\actions\\" + task_found + ".exe")
                time.sleep(12)
                print(output_code["Act"] + "Pet Is Done Eating!")
                total_earned += 10

            elif task_found == "shower":
                print(output_code["Act"] + "Pet Is Showering!")
                os.startfile(sys.path[0]+"\\actions\\"+task_found+".exe")
                time.sleep(19)
                print(output_code["Act"] + "Pet Is Done Showering!")
                total_earned += 12

            elif task_found == "play":
                pass  # time.sleep(21)

        print()
        print(output_code["Earn"]+"Total Bucks Earned So Far: " + str(total_earned))
        print()
        print(output_code["Wait"]+"Waiting 30 sec For New Tasks ")
        time.sleep(30)
    print(output_code["Earn"]+"Total Bucks Earned Is: " + str(total_earned))

if __name__ == "__main__":
    main()
