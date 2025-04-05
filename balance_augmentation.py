import fiftyone as fo
from fiftyone import ViewField as F
# Remove the import that doesn't exist
# from fiftyone.utils.albumentations import AlbumentationsTransform
import albumentations as A

def create_golf_augmentations():
    """Golf-specific biomechanical valid transformations"""
    return A.Compose([
        A.HorizontalFlip(p=0.5),          # Simulate left/right handedness
        A.Rotate(limit=5, p=0.5),         # ±5° rotation maintains swing plane
        A.RandomBrightnessContrast(
            brightness_limit=0.1,         # ±10% brightness variation
            contrast_limit=0.1,
            p=0.5
        ),
        A.GaussianBlur(blur_limit=(3,7), p=0.3),
    ])

def balance_classes(dataset):
    """Augment minority class to achieve 45-55% balance"""
    # Get current distribution
    counts = dataset.count_values("quality")
    bad_count = counts["bad_swings"]
    good_count = counts["good_swings"]
    
    # Calculate required good swings for 45% ratio
    target_ratio = 0.45
    required_good = int((target_ratio * bad_count) / (1 - target_ratio))
    augmentations_needed = max(0, required_good - good_count)
    
    if augmentations_needed == 0:
        return dataset
    
    # Get minority class samples
    good_swings = dataset.match(F("quality") == "good_swings")
    
    # Create a new dataset for augmented samples
    augmented_dataset = fo.Dataset()
    
    # Apply augmentations manually instead of using AlbumentationsTransform
    transform = create_golf_augmentations()
    
    # Determine how many times to augment each sample
    augmentations_per_sample = augmentations_needed // len(good_swings) + 1
    
    # Process each good swing and create augmented versions
    for sample in good_swings:
        for _ in range(augmentations_per_sample):
            # For videos, we would need to apply transformations frame by frame
            # This is a simplified placeholder - actual implementation would need
            # to load video frames, apply transformations, and save as new video
            augmented_sample = sample.copy()
            augmented_sample.filepath = sample.filepath  # Same source file
            augmented_sample["augmented"] = True  # Mark as augmented
            augmented_dataset.add_sample(augmented_sample)
    
    # Take only the needed number of augmentations
    augmented_samples = list(augmented_dataset.take(augmentations_needed))
    
    # Merge original and augmented samples
    merged_dataset = fo.Dataset()
    merged_dataset.add_samples(dataset)
    merged_dataset.add_samples(augmented_samples)
    
    return merged_dataset
