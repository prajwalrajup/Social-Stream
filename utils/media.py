import os
import requests
from PIL import Image
import utils.directory as directory
from loggingConfig import configure_logging, logging

# Configure logging
configure_logging()


class Media():

    # initlilize all the folder structure of data
    def __init__(self, id):
        path = os.path
        self.baseDir = directory.getBaseDirectory()
        self.dataDir = directory.makeDirIfNotExists(self.baseDir, "data")
        self.imageDir = directory.makeDirIfNotExists(self.dataDir, "images")
        self.idDir = directory.makeDirIfNotExists(self.imageDir, id)

    # write contents give to a file locaion
    def writeContentToFile(self, locaion, content):
        logging.info("writing contents to file")
        with open(locaion, 'wb') as f:
            f.write(content)

    # download the content from the url and save it in the locaiton
    def getMedia(self, url, fileName):
        logging.info(f"getting media from {url}")
        request = requests.get(url)
        imagePath = directory.pathJoin(
            self.idDir, fileName)
        self.writeContentToFile(imagePath, request.content)
        return imagePath

    # resize images to given scale (with a default of 1080 X 1350)
    def resize(self, locaion, scale=(1080, 1350)):
        image = Image.open(locaion)

        ratio_w = scale[0] / image.width
        ratio_h = scale[1] / image.height
        if ratio_w < ratio_h:
            # It must be fixed by width
            resize_width = scale[0]
            resize_height = round(ratio_w * image.height)
        else:
            # Fixed by height
            resize_width = round(ratio_h * image.width)
            resize_height = scale[1]

        try:
            image_resize = image.resize(
                (resize_width, resize_height), Image.ANTIALIAS)
            image_resize.save(locaion)
            return False

        except (Exception) as e:
            raise Exception(f"something went wrong while resizing image : {e}")

    def resiseGif(self, locaion, scale, image):
        old_gif_information = {
            'loop': bool(image.info.get('loop', 1)),
            'duration': image.info.get('duration', 40),
            'background': image.info.get('background', 223),
            'extension': image.info.get('extension', (b'NETSCAPE2.0')),
            'transparency': image.info.get('transparency', 223)
        }
        new_frames = self.get_new_frames(image, scale)
        self.save_new_gif(new_frames, old_gif_information, locaion)

    # get all the frames of a gif
    def get_new_frames(gif, scale):
        new_frames = []
        actual_frames = gif.n_frames
        for frame in range(actual_frames):
            gif.seek(frame)
            new_frame = Image.new('RGBA', gif.size)
            new_frame.paste(gif)
            new_frame = new_frame.resize(scale, Image.ANTIALIAS)
            new_frames.append(new_frame)
        return new_frames

    # save the gif to a locaion
    def save_new_gif(new_frames, old_gif_information, new_path):
        new_frames[0].save(new_path,
                           save_all=True,
                           append_images=new_frames[1:],
                           duration=old_gif_information['duration'],
                           loop=old_gif_information['loop'],
                           background=old_gif_information['background'],
                           extension=old_gif_information['extension'],
                           transparency=old_gif_information['transparency'])
