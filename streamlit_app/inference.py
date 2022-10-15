import base64
from io import BytesIO
from PIL import Image
import cv2
import torch
import os

model = torch.hub.load('ultralytics/yolov5', 'custom', path=os.path.join(os.getcwd(), 'best.pt'),
                       force_reload=False, skip_validation=True, trust_repo=True)


def getArea(box):
    return (box[2] - box[0]) * (box[3] - box[1])


def get_class(diagonal):
    if diagonal < 61.725399958201976: return 1
    if 61.72994897130565 < diagonal < 75.27996081295473: return 2
    if 75.28040648136805 < diagonal < 87.44412901962029: return 3
    if 87.45661781706401 < diagonal < 101.22358075073218: return 4
    if 101.23022868688976 < diagonal < 118.53381374105871: return 5
    if 118.53510028679268 < diagonal < 144.4311600728873: return 6
    if diagonal > 144.4464208625468: return 7


def get_diagonal(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


def rud_class(width, height):
    dev = max(width, height) * 0.0017857142857143 * 1000
    if dev <= 40:
        return 7
    elif dev <= 70:
        return 6
    elif dev <= 80:
        return 5
    elif dev <= 100:
        return 4
    elif dev <= 150:
        return 3
    elif dev <= 250:
        return 2
    else:
        return 1


def encode_result(result):
    result.ims
    result.render()
    for img in result.ims:
        buffered = BytesIO()
        im_base64 = Image.fromarray(img)
        im_base64.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')  # base64 encoded image with results


def get_results(video_path):
    count = 0
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    while success:
        success, image = vidcap.read()
        if success:
            result = model(image, size=640)
            yield {"data": detect(result, count), "photo": result}
            count += 1


def detect(result, count):
    df = result.pandas().xyxy[0]  # dataframe

    areas_list = [getArea([df['xmin'][ind], df['ymin'][ind], df['xmax'][ind], df['ymax'][ind]]) for ind in df.index]
    df = df.assign(area=areas_list)
    diagonals_list = [get_diagonal(df['xmin'][ind], df['ymin'][ind], df['xmax'][ind], df['ymax'][ind]) for ind in
                      df.index]
    df = df.assign(diagonal=diagonals_list)

    classes = [rud_class(df['xmax'][ind]-df['xmin'][ind], df['ymax'][ind]-df['ymin'][ind] )for ind in
               df.index]

    df = df.assign(classes=classes)

    df.drop(['confidence', 'class', 'name'], axis=1, inplace=True)
    return {f'frame_id': count, 'class': list(df['classes'].values)}