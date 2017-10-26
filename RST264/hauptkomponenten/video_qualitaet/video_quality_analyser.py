import cv2
import pylab
import imageio

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import skimage.measure as skim
import threading


def compare_images(imageA, imageB):
    skmse = skim.compare_mse(imageA, imageB)
    sknrmse = skim.compare_nrmse(imageA, imageB)
    skssim = skim.compare_ssim(imageA, imageB)

    # psnr is calculated:
    # err = compare_mse(im_true, im_test)
    # return 10 * np.log10((data_range ** 2) / err)
    if skmse == 0:
        skpsnr = 50
    else:
        skpsnr = skim.compare_psnr(imageA, imageB)

    return (skmse,sknrmse,skpsnr,skssim)

def compare_video_to_ref(ref_video_filepath,compare_video_filepath,dir_path_for_save):
    capA = imageio.get_reader(ref_video_filepath,  'ffmpeg')
    capB = imageio.get_reader(compare_video_filepath,  'ffmpeg')

    frameA_gray = None
    frameB_gray = None


    # Datei anlegen in der gespecihert wird
    filename = create_filename_for_save(compare_video_filepath)
    header = ['frame_num','MSE','NRSME','PSNR','SSIM']

    csv_file_path = dir_path_for_save + filename + '.csv'

    csv_file = open(csv_file_path, 'w')
    csv_file.write("comparison of the two following files" + "\n")
    csv_file.write("reference video: " + ref_video_filepath + "\n")
    csv_file.write("video to be compared to reference: " + compare_video_filepath + "\n")
    csv_file.write(str(header) + "\n")
    csv_file.close()


    mse_sum = 0
    nrsme_sum = 0
    psnr_sum = 0
    ssim_sum = 0

    i = 1
    no_more_frames = False

    i = 0
    last_frame_could_be_read = True
    while(last_frame_could_be_read and i <= 600):
        try:
            frameA = capA.get_data(i)
            frameB = capB.get_data(i)

            frameA_gray = cv2.cvtColor(frameA, cv2.COLOR_RGB2GRAY)
            frameB_gray = cv2.cvtColor(frameB, cv2.COLOR_RGB2GRAY)

            (mse,nrsme,psnr,ssim) = compare_images(frameA_gray, frameB_gray)

            df = pd.DataFrame([i, mse, nrsme, psnr, ssim]).T
            df.to_csv(csv_file_path, mode='a', header=False)

            mse_sum += mse
            nrsme_sum += nrsme
            psnr_sum += psnr
            ssim_sum += ssim

            if (i % 50 == 0):
                print(i)

            i += 1

        except:
            last_frame_could_be_read = False



    # write average values to beginning of file

    number_of_frames = i-1

    mse_avg = mse_sum / number_of_frames
    nrsme_avg = nrsme_sum / number_of_frames
    psnr_avg = psnr_sum / number_of_frames
    ssim_avg = ssim_sum / number_of_frames

    csv_file = open(csv_file_path, "r")
    contents = csv_file.readlines()
    csv_file.close()

    info_lines_end = 3

    contents.insert(info_lines_end, "mse_avg: " + str(mse_avg) + "\n")
    contents.insert(info_lines_end + 1, "nrsme_avg: " + str(nrsme_avg) + "\n")
    contents.insert(info_lines_end + 2, "psnr_avg: " + str(psnr_avg) + "\n")
    contents.insert(info_lines_end + 3, "ssim_avg: " + str(ssim_avg) + "\n")
    contents.insert(info_lines_end + 4, "last frame which could be compared: " + str(number_of_frames) + "\n")

    csv_file = open(csv_file_path, "w")
    contents = "".join(contents)
    csv_file.write(contents)
    csv_file.close()



def compare_single_frame_with_visualisation(ref_file, compare_file, frame_num):
    capA = cv2.VideoCapture(ref_file)
    capB = cv2.VideoCapture(compare_file)

    frameA_gray = None
    # frameB_gray = None

    if capA.isOpened():
        capA.set(1, frame_num)
        ret, frameA = capA.read()
        frameA_gray = cv2.cvtColor(frameA, cv2.COLOR_BGR2GRAY)

    # length = int(capA.get(cv2.CAP_PROP_FRAME_COUNT))
    # print(length)

    if capB.isOpened():
        capB.set(1, frame_num)
        ret, frameB = capB.read()
        frameB_gray = cv2.cvtColor(frameB, cv2.COLOR_BGR2GRAY)

    # length = int(capB.get(cv2.CAP_PROP_FRAME_COUNT))
    # print(length)

    skmse = skim.compare_mse(frameA_gray, frameB_gray)
    sknrmse = skim.compare_nrmse(frameA_gray, frameB_gray)
    skpsnr = skim.compare_psnr(frameA_gray, frameB_gray)
    skssim = skim.compare_ssim(frameA_gray, frameB_gray)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 4))
    plt.suptitle("Compare_Frames" + " |  MSE: %.2f, NRSME: %.2f, PSNR: %.2f, SSIM: %.2f" % (skmse, sknrmse, skpsnr, skssim))

    ax1.imshow(frameA_gray, cmap=plt.cm.gray, interpolation='nearest', aspect='equal')
    ax1.axis("off")

    ax2.imshow(frameB_gray, cmap=plt.cm.gray, interpolation='nearest', aspect='equal')
    ax2.axis("off")

    # plt.show()

    capA.release()
    capB.release()

def create_filename_for_save(compare_video_filepath):
    filename = compare_video_filepath.rpartition("/")[2]
    filename_without_ending = filename.rpartition(".")[0]

    return "compare_" + filename_without_ending