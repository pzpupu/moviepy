import numpy as np
from moviepy.editor import *

# 加载 MP3 音频文件
audio_clip = AudioFileClip("./assets/f1d71e94-431e-4ef5-93c4-abacea38bf32.mp3")

# 获取音频的持续时间
audio_duration = audio_clip.duration

# 加载图片
image_clip = ImageClip("./assets/f1d71e94-431e-4ef5-93c4-abacea38bf32.jpeg", duration=audio_duration)

# 获取图片的尺寸
w, h = [330, 330]


# 创建圆形的掩码
# 定义一个遮罩函数，在遮罩区域内为1，其他地方为0
def make_circle_mask(w, h):
    """创建一个圆形遮罩，大小为w*h"""
    # 创建一个网格，x和y的值分别对应图像的像素位置
    Y, X = np.ogrid[:h, :w]
    center_x, center_y = w / 2, h / 2  # 圆心为图像中心
    radius = min(w, h) / 2  # 半径为图像的最短边的一半
    # 计算每个像素点到圆心的距离，小于半径的部分为圆形区域
    mask = (X - center_x) ** 2 + (Y - center_y) ** 2 <= radius ** 2
    return mask.astype(float)  # 返回遮罩，0表示透明，1表示不透明


# 创建一个黑色圆圈
def make_black_circle(w, h, radius):
    """在中间创建一个黑色圆圈，圆圈的大小为20*20像素，透明背景"""
    Y, X = np.ogrid[:h, :w]
    center_x, center_y = w / 2, h / 2
    circle_mask = (X - center_x) ** 2 + (Y - center_y) ** 2 <= radius ** 2
    img = np.zeros((h, w, 4), dtype=np.uint8)  # 透明背景，4通道
    img[:, :, 3] = 0  # Alpha 通道全透明
    img[circle_mask, :3] = (0, 0, 0)  # 黑色圆圈的RGB通道
    img[circle_mask, 3] = 255  # 黑色圆圈的Alpha通道，完全不透明
    return img


# 加载GIF并让其循环播放，持续到音频结束
gif_clip = VideoFileClip("./assets/disc.gif").set_position('center').loop(duration=audio_duration)

# 设置Title
txt_clip = TextClip("Lost in the Moment", fontsize=40, color='white', font='Rubik-Bold')
txt_clip = txt_clip.set_position(lambda t: ('center', 1000)).set_duration(audio_duration)

# 将掩码应用到图片
circle_mask = make_circle_mask(w, h)
image_clip = image_clip.set_position(('center', 490)).set_mask(ImageClip(circle_mask, ismask=True))

# 创建20x20黑色圆圈
black_circle = ImageClip(make_black_circle(40, 40, 16), ismask=False, duration=audio_duration,
                         transparent=True).set_position(('center', 635))

# 合并 GIF 和 JPG 剪辑（这里将两个片段叠加到一起，选择合适的剪辑方式）
video_clip = CompositeVideoClip([gif_clip, image_clip, black_circle, txt_clip, ], size=[750, 1624])

# 设置音频到视频剪辑
video_clip = video_clip.set_audio(audio_clip)

# 输出合并后的文件
video_clip.write_videofile("./output_video.mp4", fps=24)
