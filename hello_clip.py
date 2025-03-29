from scenedetect import detect, AdaptiveDetector, split_video_ffmpeg
output_dir='./clip_output'
scene_list = detect('tik.mp4', AdaptiveDetector())
split_video_ffmpeg('tik.mp4', scene_list,output_dir=output_dir)
