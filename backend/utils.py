import cv2
import os
import numpy as np
from natsort import natsorted
from PIL import Image
from skimage.measure import compare_ssim


def create_dataset(videos_dir, output_dir, fps=24):
    all_videos = os.listdir(videos_dir)
    count = 0
    for video in all_videos:
        if os.path.isdir(os.path.join(videos_dir, video)):
            continue
        video_path = os.path.join(videos_dir, video)
        save_path = (os.path.join(output_dir, video)[
                     0:-4]+"_frame%d.jpg").replace(' ', '')
        ffmpeg_command = "ffmpeg -i "+video_path + \
            " -vf fps="+str(fps)+" "+save_path+" -hide_banner"
        print("COMMAND ", ffmpeg_command)
        os.system(ffmpeg_command)
    print("Finished splitting videos into frames!")


def create_validation_set(input_frames_dir, validation_frames_dir, validation_split=0.1, method="last"):
    random_sorted_frames = os.listdir(input_frames_dir)
    sorted_frames = natsorted(random_sorted_frames)

    if method == "random":
        validation_frames = random_sorted_frames[0:int(
            validation_split*len(random_sorted_frames))]
    if method == "first":
        validation_frames = sorted_frames[0:int(
            validation_split*len(random_sorted_frames))]
    if method == "last":
        validation_frames = sorted_frames[-(
            int(validation_split*len(random_sorted_frames))):len(random_sorted_frames)]
        print("START ", int(validation_split*len(random_sorted_frames)))
        print("END ", len(random_sorted_frames))

    for frame in validation_frames:
        os.rename(os.path.join(input_frames_dir, frame),
                  os.path.join(validation_frames_dir, frame))


def fixed_generator(generator):
    for batch in generator:
        yield (batch, batch)


def calculate_threshold(model, images_dir, image_size=224, channels=3):
    losses = []
    max_loss, min_loss, average_loss, sum_loss = 0, 999999, 0, 0
    images = os.listdir(images_dir)

    for image in images:
        bgr_img = cv2.imread(os.path.join(images_dir, image))
        bgr_img = cv2.resize(bgr_img, (image_size, image_size))
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        rgb_img = np.array(rgb_img) / 255.
        gray_img_orig = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
        rgb_img = rgb_img.reshape(1, image_size, image_size, channels)

        pred = model.predict(rgb_img)
        pred = pred.reshape(image_size, image_size, channels)
        recon_img = Image.fromarray((pred * 255.).astype(np.uint8))
        gray_img_recon = cv2.cvtColor(np.array(recon_img), cv2.COLOR_BGR2GRAY)

        ssim_loss = compare_ssim(gray_img_orig, gray_img_recon, winsize=101)
        losses.append(ssim_loss)
        print(ssim_loss)

    for loss in losses:
        sum_loss += loss
        if loss <= min_loss:
            min_loss = loss
        if loss >= max_loss:
            max_loss = loss

    average_loss = sum_loss/len(losses)

    return losses, max_loss, min_loss, average_loss
