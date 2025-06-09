import os
import subprocess

DATASET_DIR = 'data/input'
OUTPUT_DIR = 'data/output'


def preprocess_dataset():
    os.makedirs(DATASET_DIR, exist_ok=True)
    sample_path = os.path.join(DATASET_DIR, 'sample.mp4')
    if not os.path.exists(sample_path):
        # Generate a 2 second color test video
        cmd = [
            'ffmpeg', '-y', '-f', 'lavfi', '-i', 'testsrc=size=128x128:rate=30',
            '-t', '2', sample_path
        ]
        subprocess.run(cmd, check=True)
    return [sample_path]


def transcode_videos(video_paths):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_paths = []
    for path in video_paths:
        filename = os.path.basename(path)
        out_path = os.path.join(OUTPUT_DIR, os.path.splitext(filename)[0] + '.avi')
        cmd = [
            'ffmpeg', '-y', '-i', path,
            '-c:v', 'mpeg4', '-b:v', '1M',
            out_path
        ]
        subprocess.run(cmd, check=True)
        output_paths.append(out_path)
    return output_paths


def extract_results(output_paths):
    results = []
    for path in output_paths:
        size = os.path.getsize(path)
        results.append({'file': path, 'size_bytes': size})
    return results


def run_pipeline():
    input_videos = preprocess_dataset()
    transcoded = transcode_videos(input_videos)
    results = extract_results(transcoded)
    for r in results:
        print(f"{r['file']}: {r['size_bytes']} bytes")


if __name__ == '__main__':
    run_pipeline()
