import fiftyone as fo
from pathlib import Path
import os
from balance_augmentation import balance_classes

def load_golf_dataset(root_dir):
    """Structured importer for golf swing analysis dataset"""

    # Clear existing dataset
    if fo.dataset_exists("golf_swings_analysis"):
        fo.delete_dataset("golf_swings_analysis")
    # Initialize dataset
    dataset = fo.Dataset("golf_swings_analysis")
    dataset.persistent = True  # Enable persistent storage

    # Walk through directory structure
    for root, _, files in os.walk(root_dir):
        for filename in files:
            if filename.lower().endswith((".mp4", ".mov", ".avi")):
                video_path = os.path.join(root, filename)
                parts = Path(video_path).parts
                
                # Extract hierarchical labels from path structure
                try:
                    # Custom_Dataset/BACK VIEW/Bad Swings/Bad Chipping Swings/video.mp4
                    view = parts[-4].replace(" ", "_").lower()  # "back_view"
                    quality = parts[-3].replace(" ", "_").lower()  # "bad_swings"
                    subcategory = parts[-2].replace(" ", "_").lower()  # "bad_chipping_swings"
                except IndexError:
                    print(f"Skipping invalid path: {video_path}")
                    continue

                # Create sample with structured labels
                sample = fo.Sample(filepath=video_path)
                
                # Add hierarchical labels
                sample["view"] = view
                sample["quality"] = quality
                sample["subcategory"] = fo.Classification(label=subcategory)  # FIXED HERE
                
                # Add custom metadata
                sample["duration"] = get_video_duration(video_path)
                sample["fps"] = get_video_fps(video_path)
                
                dataset.add_sample(sample)

    return dataset

def get_video_duration(path):
    """Helper function to get video duration using ffmpeg"""
    import cv2
    video = cv2.VideoCapture(path)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    return frame_count / fps if fps else 0

def get_video_fps(path):
    """Helper function to get video FPS"""
    import cv2
    video = cv2.VideoCapture(path)
    return video.get(cv2.CAP_PROP_FPS)

def validate_dataset(dataset):
    """Quality checks and validation"""
    # 1. Verify sample counts
    print(f"Total samples: {len(dataset)}")
    
    # 2. Check label distribution
    print("\nView distribution:")
    print(dataset.count_values("view"))
    
    print("\nQuality distribution:")
    print(dataset.count_values("quality"))
    
    print("\nSubcategory distribution:")
    print(dataset.count_values("subcategory"))
    
    # 3. Verify video properties
    print("\nVideo durations (seconds):")
    print(dataset.bounds("duration"))
    
    print("\nFPS distribution:")
    print(dataset.bounds("fps"))
    
    # 4. Launch visual inspection
    session = fo.launch_app(dataset)
    return session

if __name__ == "__main__":
    ROOT_DIR = "/Users/jonathanmahrtguyou/Desktop/JoMaGuy Projects/MongoDB_Hackathon/CUSTOM_DATASET"
    
    # Load dataset
    dataset = load_golf_dataset(ROOT_DIR)
    
    # Add persistent fields
    dataset.add_sample_field("duration", fo.FloatField)
    dataset.add_sample_field("fps", fo.FloatField)
    
    # Apply class balancing
    balanced_dataset = balance_classes(dataset)
    
    # Validate and export
    session = validate_dataset(balanced_dataset)
    
    balanced_dataset.export(
        export_dir=os.path.join(ROOT_DIR, "balanced_dataset"),
        dataset_type=fo.types.VideoClassificationDirectoryTree,
        label_field="subcategory",
        overwrite=True
    )
    
    input("Press Enter to continue...")

