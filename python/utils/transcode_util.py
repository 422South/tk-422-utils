import datetime
import os
import subprocess


def sequence_transcode(fileName, pathToImageSequence, outputFilePath, frame_rate=25):
    # pathToImageSequence example --> publishToCloudTestAsset_scene_persp.v020.%04d.png
    # Finds the start frame of the sequence based off the file path
    imageFileBaseName = os.path.basename(os.path.splitext(pathToImageSequence)[0])[:-5]
    listOfImages = os.listdir(os.path.dirname(pathToImageSequence))
    for i in sorted(listOfImages):
        if i.startswith(imageFileBaseName):
            startFrame = os.path.splitext(i)[0][-4:]
            break
    else:
        raise Exception('There was a problem transcoding')

    fontSize = 38
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ffmpegPath = os.path.join(current_dir, 'ffmpeg')
    logoPath = os.path.join(current_dir, '422Logo.png')
    fontPath = os.path.join(current_dir, 'Moderat-Regular.otf').replace('\\', '/').replace(
        ':', '\:')
    # fontPath requires some weird formatting to work inside subprocess for ffmpeg.exe
    # The : needs to be escaped, no other backslashes can be present

    subprocess.call(
        [ffmpegPath, '-r', str(frame_rate), '-start_number', startFrame, '-gamma', '2.2', '-i', pathToImageSequence,
         '-i', logoPath,
         '-filter_complex',
         "[0:v][1:v]overlay=(main_w-overlay_w)-10:10,"
         "drawtext=fontsize=" + str(
             fontSize) + ":x=10:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='" + fileName.replace(
             '_Tags.mp4', '') + "',"
                                "drawtext=fontsize=" + str(
             fontSize) + ":x=w-tw-10:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='Frame\: %{n}':start_number=1",
         '-pix_fmt', 'yuv420p',
         '-b:v', '30000k', outputFilePath, '-y', '-vsync', 'passthrough'])
    return


def video_transcode_audio(fileName, pathToImageSequence, outputFilePath, audio_file, audio_start, start_frame, duration, frame_rate=25):
    fontSize = 38
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ffmpegPath = os.path.join(current_dir, 'ffmpeg')
    logoPath = os.path.join(current_dir, '422Logo.png')
    fontPath = os.path.join(current_dir, 'Moderat-Regular.otf').replace('\\', '/').replace(
        ':', '\:')
    # fontPath requires some weird formatting to work inside subprocess for ffmpeg.exe
    # The : needs to be escaped, no other backslashes can be present
    if float(start_frame) - float(audio_start) < 0:
        audioStartTime = '-0' + str(
            datetime.timedelta(seconds=(abs(float(start_frame) - float(audio_start))) / float(frame_rate)))
    else:
        audioStartTime = '0' + str(
            datetime.timedelta(seconds=(float(start_frame) - float(audio_start)) / float(frame_rate)))

    audioDuration = '0' + str(datetime.timedelta(seconds=(duration/ float(frame_rate))))

    call_args = [ffmpegPath, '-r', str(frame_rate), '-gamma', '2.2', '-i', pathToImageSequence, '-i', logoPath,
                 '-ss', audioStartTime, '-i', audio_file,
                 '-filter_complex',
                 "[0:v][1:v]overlay=(main_w-overlay_w)-10:10,"
                 "drawtext=fontsize=" + str(
                     fontSize) + ":x=10:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='" + fileName.replace(
                     '_Tags.mp4', '') + "',"
                                        "drawtext=fontsize=" + str(
                     fontSize) + ":x=w-tw-10:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='Frame\: %{n}':start_number=1",
                 '-pix_fmt', 'yuv420p',
                 '-b:v', '30000k', '-to', audioDuration, outputFilePath, '-y', '-vsync', 'passthrough']

    extension = pathToImageSequence.split('.')[-1]
    if extension and extension.lower() in ['tif', 'tiff']:
        call_args = [ffmpegPath, '-r', str(frame_rate), '-i', pathToImageSequence, '-i', logoPath,
                     '-ss', audioStartTime, '-i', audio_file,
                     '-filter_complex',
                     "[0:v][1:v]overlay=(main_w-overlay_w)-10:10,"
                     "drawtext=fontsize=" + str(
                         fontSize) + ":x=10:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='" + fileName.replace(
                         '_Tags.mp4', '') + "',"
                                            "drawtext=fontsize=" + str(
                         fontSize) + ":x=w-tw-10:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='Frame\: %{n}':start_number=1",
                     '-pix_fmt', 'yuv420p',
                     '-b:v', '30000k', '-to', audioDuration, outputFilePath, '-y', '-vsync', 'passthrough']

    subprocess.call(call_args)
    return


def video_transcode(fileName, pathToImageSequence, outputFilePath, frame_rate=25):
    fontSize = 38
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ffmpegPath = os.path.join(current_dir, 'ffmpeg')
    logoPath = os.path.join(current_dir, '422Logo.png')
    fontPath = os.path.join(current_dir, 'Moderat-Regular.otf').replace('\\', '/').replace(
        ':', '\:')
    # fontPath requires some weird formatting to work inside subprocess for ffmpeg.exe
    # The : needs to be escaped, no other backslashes can be present
    call_args = [ffmpegPath, '-r', str(frame_rate), '-gamma', '2.2', '-i', pathToImageSequence, '-i', logoPath,
                 '-filter_complex',
                 "[0:v][1:v]overlay=(main_w-overlay_w)-10:10,"
                 "drawtext=fontsize=" + str(
                     fontSize) + ":x=10:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='" + fileName.replace(
                     '_Tags.mp4', '') + "',"
                                        "drawtext=fontsize=" + str(
                     fontSize) + ":x=w-tw-10:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='Frame\: %{n}':start_number=1",
                 '-pix_fmt', 'yuv420p',
                 '-b:v', '30000k', outputFilePath, '-y', '-vsync', 'passthrough']

    extension = pathToImageSequence.split('.')[-1]
    if extension and extension.lower() in ['tif', 'tiff']:
        call_args = [ffmpegPath, '-r', str(frame_rate), '-i', pathToImageSequence, '-i', logoPath,
                     '-filter_complex',
                     "[0:v][1:v]overlay=(main_w-overlay_w)-10:10,"
                     "drawtext=fontsize=" + str(
                         fontSize) + ":x=10:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='" + fileName.replace(
                         '_Tags.mp4', '') + "',"
                                            "drawtext=fontsize=" + str(
                         fontSize) + ":x=w-tw-10:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='Frame\: %{n}':start_number=1",
                     '-pix_fmt', 'yuv420p',
                     '-b:v', '30000k', outputFilePath, '-y', '-vsync', 'passthrough']

    subprocess.call(call_args)
    return


def sequence_transcode_withoutTags(pathToImageSequence, outputFilePath, startFrame, playblastFileName,
                                   extraMessage='',
                                   frame_rate=25):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ffmpegPath = os.path.join(current_dir, 'ffmpeg')

    fontSize = 38
    fontPath = os.path.join(current_dir, 'Moderat-Regular.otf').replace('\\', '/').replace(
        ':', '\:')
    cmdLine = [ffmpegPath, '-r', str(frame_rate), '-start_number', startFrame, '-i', pathToImageSequence,
               '-filter_complex',
               "drawtext=fontsize=" + str(
                   fontSize) + ":x=(w-text_w)/2:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='" + playblastFileName + "',"
                                                                                                                                    "drawtext=fontsize=" + str(
                   fontSize - 2) + ":x=(w-text_w)/2:y=10:fontcolor=White:fontfile='" + fontPath + "':text='" + extraMessage + "'",
               '-pix_fmt', 'yuv420p',
               '-b:v', '30000k', outputFilePath, '-y', '-vsync', 'passthrough']
    subprocess.call(cmdLine, shell=True)
    return


def sequence_transcode_withoutTags_withAudio(pathToImageSequence, outputFilePath, startFrame, endFrame, frameOffset,
                                             playblastFileName, audioFile, extraMessage='', frame_rate=25):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ffmpegPath = os.path.join(current_dir, 'ffmpeg')

    fontSize = 38
    fontPath = os.path.join(current_dir, 'Moderat-Regular.otf').replace('\\', '/').replace(
        ':', '\:')

    # Appending a '0' at the start because ffmpeg needs the format to be 00:00:00 and timedelta does 0:00:00
    # Yes this will break if someone tries to playblast something longer than 9.9 hours - Unlikely but not impossible

    # If statement with the '-0' is because timedelta doesn't support negative values and instead shows "-1 Day 23:55:59"
    # which completely breaks ffmpeg. I use abs() to make the negative time positive then add a - manually.

    if float(startFrame) - float(frameOffset) < 0:
        audioStartTime = '-0' + str(
            datetime.timedelta(seconds=(abs(float(startFrame) - float(frameOffset))) / float(frame_rate)))
    else:
        audioStartTime = '0' + str(
            datetime.timedelta(seconds=(float(startFrame) - float(frameOffset)) / float(frame_rate)))

    audioDuration = '0' + str(datetime.timedelta(seconds=(float(endFrame) - float(startFrame)) / float(frame_rate)))
    cmdLine = [ffmpegPath, '-r', str(frame_rate), '-start_number', startFrame, '-i', pathToImageSequence, '-ss',
               audioStartTime, '-i', audioFile,
               '-filter_complex',
               "drawtext=fontsize=" + str(
                   fontSize) + ":x=(w-text_w)/2:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='" + playblastFileName + "',"
                                                                                                                                    "drawtext=fontsize=" + str(
                   fontSize - 2) + ":x=(w-text_w)/2:y=10:fontcolor=White:fontfile='" + fontPath + "':text='" + extraMessage + "'",
               '-pix_fmt', 'yuv420p',
               '-b:v', '30000k', '-to', audioDuration, outputFilePath, '-y', '-vsync', 'passthrough']
    subprocess.call(cmdLine)
    return


def image_transcode_withTags(inputImage, outputImage, burnIns, extraMsg):
    current_dir = os.path.dirname(os.path.realpath(__file__))
    ffmpegPath = os.path.join(current_dir, 'ffmpeg')

    fontSize = 18
    fontPath = os.path.join(current_dir, 'Moderat-Regular.otf').replace('\\', '/').replace(
        ':', '\:')
    logoPath = os.path.join(current_dir, '422Logo.png')

    subprocess.call([ffmpegPath, '-i', inputImage, '-i', logoPath,
                     '-filter_complex',
                     "[0:v][1:v]overlay=(main_w-overlay_w)-10:10,"
                     "drawtext=fontsize=" + str(
                         fontSize - 2) + ":x=(w-text_w)/2:y=10:fontcolor=White:fontfile='" + fontPath + "':text='" + extraMsg + "',"
                                                                                                                                "drawtext=fontsize=" + str(
                         fontSize) + ":x=(w-text_w)/2:y=h-th-10:fontcolor=White:fontfile='" + fontPath + "':text='" + burnIns + "'",
                     '-pix_fmt', 'yuv420p',
                     outputImage, '-y', '-vsync', 'passthrough'])

    return
