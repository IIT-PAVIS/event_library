import cv2
import os

from tqdm import tqdm

__all__ = ['NTU_extractor']


class NTU_extractor:
    def __init__(self, H, W):
        self.H = H
        self.W = W
        
    def _get_ntu_video_files(input_dir):
        video_files = []
        for root, dirs, files in os.walk(input_dir):
            for f in files:
                if f.endswith('.avi'):
                    video_files.append(os.path.join(root, f))
        print(f"Found n {len(video_files)} videos")
        return video_files

    def extract_frames(self, root_dir, output_dir):

        video_files = NTU_extractor._get_ntu_video_files(root_dir)

        for seq, video_file in enumerate(tqdm(video_files)):
            seq_name = os.path.basename(video_file).split(".")[0]
            seq_dir_parents = video_file.replace(video_file,
                                                 "").replace(root_dir, "")

            vcap_video = cv2.VideoCapture(video_file)

            seq_dir = os.path.join(output_dir, seq_dir_parents, seq_name)
            imgs_dir = os.path.join(seq_dir, 'imgs')
            os.makedirs(imgs_dir, exist_ok=True)

            if vcap_video.isOpened():
                fps = int(vcap_video.get(cv2.CAP_PROP_FPS))

                frame_count = int(vcap_video.get(cv2.CAP_PROP_FRAME_COUNT))
                print("Extracting")

                for id in tqdm(range(frame_count)):
                    # Capture frame-by-frame
                    _, frame = vcap_video.read()

                    frame = cv2.resize(frame, (self.H, self.W))
                    cv2.imwrite(os.path.join(imgs_dir, f'frame{id:07d}.png'),
                                frame)

                with open(os.path.join(seq_dir, 'fps.txt'), 'w') as f:
                    f.write(str(fps))

