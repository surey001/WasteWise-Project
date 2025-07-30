import os
import shutil
import random

# Source and destination folders
source_dir = r'D:\WasteWise\dataset\Garbage classification\Garbage classification'
dest_dir = r'D:\WasteWise\dataset\processed'
train_split = 0.8  # 80% for training

# Loop through all class folders
categories = os.listdir(source_dir)

for category in categories:
    category_path = os.path.join(source_dir, category)
    images = os.listdir(category_path)
    random.shuffle(images)

    split_idx = int(len(images) * train_split)
    train_images = images[:split_idx]
    val_images = images[split_idx:]

    # Move images to train/ and val/ folders
    for mode, image_list in [('train', train_images), ('val', val_images)]:
        dest_folder = os.path.join(dest_dir, mode, category)
        os.makedirs(dest_folder, exist_ok=True)
        for img_name in image_list:
            src = os.path.join(category_path, img_name)
            dst = os.path.join(dest_folder, img_name)
            shutil.copy(src, dst)

print("✅ Dataset successfully split into train and val folders!")
