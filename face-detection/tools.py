from subprocess import Popen, run, CalledProcessError
import os
from pathlib import Path
import cv2
from tempfile import TemporaryDirectory
import ffmpeg
import hashlib
import disco
from shutil import rmtree

BASE_COLORS = [
    (0, 0, 0),
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (0, 255, 255),
    (255, 0, 255),
    (192, 192, 192),
    (128, 128, 128),
    (128, 0, 0),
    (128, 128, 0),
    (0, 128, 0),
    (128, 0, 128),
    (0, 128, 128),
    (0, 0, 128),

]
# Load the cascade
classifier_xmls = [
    'haarcascade_frontalcatface.xml',
    'haarcascade_frontalcatface_extended.xml',
    'haarcascade_frontalface_alt.xml',
    'haarcascade_frontalface_alt2.xml',
    'haarcascade_frontalface_alt_tree.xml',
    'haarcascade_frontalface_default.xml'
]
classefiers = [  # a tuple of color and classifier
    (BASE_COLORS[i], cv2.CascadeClassifier(classifier_xmls[i]))
    for i in range(len(classifier_xmls))
]
BUF_SIZE = 65536  # lets read stuff in 64kb chunks!
SEP = "   "


def make_empty_folder(path: Path):
    if path.exists():
        rmtree(path)
    os.makedirs(path)
    return path


def split_video(src, segement_length, outp):
    os.makedirs(outp, exist_ok=True)
    for x in Path(outp).glob("split*.mp4"):
        x.unlink()

    secs = segement_length % 60
    total_mins = segement_length // 60
    mins = total_mins % 60
    hrs = total_mins // 60
    command = [
        'ffmpeg', '-i', f'"{str(src)}"', '-c', 'copy', '-map', '0', '-segment_time', f"{hrs}:{mins}:{secs}", '-f', 'segment', f"{str(outp)}/split%03d.mp4"
    ]
    run(args=' '.join(command), cwd=os.getcwd(), shell=True, capture_output=True, check=True)
    return list(Path(outp).glob("split*.mp4"))


def join_videos(path, target_path: Path):
    target_parent_path = target_path.parent
    os.makedirs(target_parent_path, exist_ok=True)

    if target_path.exists():
        target_path.unlink()

    manifest_path = target_parent_path / "manifest.txt"
    if manifest_path.exists():
        manifest_path.unlink()

    manifest = [f"file {str(x.absolute())}" for x in sorted(Path(path).glob("*.mp4"))]
    manifest_path.write_text('\n'.join(manifest))
    command = f"ffmpeg -f concat -safe 0 -i {str(manifest_path)} -c copy {str(target_path)} -hide_banner"
    run(args=command, cwd=os.getcwd(), shell=True, capture_output=False, check=True)
    manifest_path.unlink()
    return target_path


def proc_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    for color, classifier in classefiers:
        faces = classifier.detectMultiScale(gray, 1.2, 5)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    return img


def proc_video(src_path, target_path):
    proced_frames = 0
    os.makedirs(target_path.parent, exist_ok=True)
    cap = cv2.VideoCapture(str(src_path))
    source_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    source_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    source_fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    with TemporaryDirectory() as td:
        out_p = Path(td) / 'temp.mp4'
        out = cv2.VideoWriter(str(out_p), fourcc, source_fps, (source_width, source_height))
        try:
            ok, img = cap.read()
            while ok:
                out.write(proc_image(img))
                proced_frames += 1
                ok, img = cap.read()

            print("Processed Frames: ", proced_frames)
        finally:
            cap.release()
            out.release()

        in1 = ffmpeg.input(str(out_p))
        v1 = in1.video
        out = ffmpeg.output(v1, str(target_path))
        out.run(overwrite_output=True)
        print("Exported to ", target_path)
        return target_path


def sha1(path):
    wipSha = hashlib.sha1()

    with open(path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            wipSha.update(data)
        return wipSha.hexdigest()


def _load_disco_files():
    if not disco_fids_path.exists():
        disco_fids_path.touch()
    lines = disco_fids_path.read_text().strip()
    if not lines:
        return {}
    lines = lines.split('\n')
    return {k: v for k, v in (x.split(SEP) for x in lines)}


disco_fids_path = Path('.disco.fids')
disco_files = _load_disco_files()


def get_fid(path: Path):
    sha = sha1(path)
    if sha not in disco_files:
        print(f"Uploading {path} ({sha})")
        fid = disco.upload_file(path.name, path)
        disco_files[sha] = fid
        with open(disco_fids_path, 'a') as f:
            f.write(f"{sha}{SEP}{fid}\n")

    else:
        fid = disco_files[sha]

    return fid


def get_common_file_ids():
    _self_path = Path('.')
    files = ['tools.py'] + classifier_xmls
    self_files = [_self_path / f for f in files]

    return [get_fid(x) for x in self_files]


def get_run_fid():
    return get_fid(Path('.') / 'run.py')
