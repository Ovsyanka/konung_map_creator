# Захват изображения с экрана и сохранение в файлы с определенным периодом.
# частота
# задержка перед стартом
# количество
# Путь к папке
# стартовый номер
# маска имени

# TODO:
# Вынести все эти объявления куда-нибудь в хорошее правильное место.

# ------------------- Парсинг аргументов ----------------------------

import argparse

parser = argparse.ArgumentParser(description='Захват изображения с экрана.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')

parser.add_argument('screensPath', nargs='?', help='path to store captured screens',
					default='.\\testScreens')
parser.add_argument('filesMask', nargs='?', help='mask to name saved files',
					default='screen_')
parser.add_argument('delay', nargs='?', help='delay between screen grabs in ms',
					default=1500, type=int)

args = parser.parse_args()
# print(args.accumulate(args.integers))

# -------------------  end Парсинг аргументов ----------------------------

# -------------------  Функция для рекурсивного создания директории. -----
import os, errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

# -------------------  end Функция для рекурсивного создания директории. -

# import os
# import sys
import time
# import Image
# import ImageGrab
from PIL import ImageGrab, ImageChops

print('test')

screensPath, filesMask, delay = args.screensPath, args.filesMask, args.delay / 1000
mkdir_p(screensPath)
# os.path.join(os.path.dirname(path), result) - слепление директорий.
print(str(delay))
time.sleep(1)
# img.show()
# img0 = None
for i in range(1,3):
	img = ImageGrab.grab(bbox=(140,0,660,486))
	
	saveas = os.path.join(screensPath, filesMask + str(i) + '.png')
	
	# if (img0 == img):
	# 	print(' equal')
	# 	imgDiff = ImageChops.difference(img0, img)
	# 	saveasDiff = os.path.join(screensPath, filesMask + str(i) + '_diff.png')
	# 	imgDiff.save(saveasDiff)
	# 	imgDiff.show()

	img.save(saveas)
	print(saveas + ' saved')
	time.sleep(delay)
	img0 = img



