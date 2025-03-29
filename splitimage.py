from scenedetect import detect, ContentDetector
from scenedetect import SceneManager, VideoManager
from scenedetect.video_splitter import split_video_ffmpeg
from scenedetect.scene_manager import save_images
import os

def detect_and_save(video_path, output_dir='./output'):
    """
    Detect scenes, save scene list and images for each scene
    
    Parameters:
    video_path (str): Path to input video
    output_dir (str): Directory to save outputs
    """
    try:
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            # If the directory exists, remove all its files but keep subdirectories
            for filename in os.listdir(output_dir):
                file_path = os.path.join(output_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)  # Remove files and symbolic links
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
                    
        # Create video manager and scene manager
        video_manager = VideoManager([video_path])
        scene_manager = SceneManager()
        
        # Add detector
        scene_manager.add_detector(ContentDetector())
        
        # Start video manager
        video_manager.start()
        
        # Detect scenes
        scene_manager.detect_scenes(frame_source=video_manager)
        
        # Get scene list
        scene_list = scene_manager.get_scene_list()
        
        # Print scene list
        print(f"\nFound {len(scene_list)} scenes:")
        for scene in scene_list:
            print(f"Scene from {scene[0].get_timecode()} to {scene[1].get_timecode()}")
        
        # Save images
        save_images(
            scene_list,
            video_manager,
            num_images=3,
            output_dir=output_dir,
            image_name_template='scene-$SCENE_NUMBER-$IMAGE_NUMBER',
            show_progress=True
        )
        
        # Optionally split video
        split_video_ffmpeg(
            video_path,
            scene_list,
            output_dir=output_dir,
            show_progress=True
        )
        
        print(f"\nImages saved to: {output_dir}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        video_manager.release()

def main():
    # Example usage
    video_path = "tik.mp4"  # 替换为你的视频路径
    output_dir = "output_scenes"  # 输出目录
    
    print(f"Processing video: {video_path}")
    detect_and_save(video_path, output_dir)

if __name__ == "__main__":
    main()
