import os
import random
import shutil

def split_dataset(input_dir, output_dir, ratio=(0.8, 0.2)):
    """Splits dataset into train/validation sets with error handling"""
    
    try:
        # Verify input directory exists
        if not os.path.exists(input_dir):
            raise FileNotFoundError(f"Input directory '{input_dir}' not found")
        
        # Create output directories
        train_dir = os.path.join(output_dir, 'train')
        val_dir = os.path.join(output_dir, 'val')
        os.makedirs(train_dir, exist_ok=True)
        os.makedirs(val_dir, exist_ok=True)
        
        # Process each class
        for class_name in os.listdir(input_dir):
            class_path = os.path.join(input_dir, class_name)
            
            if os.path.isdir(class_path):
                # Create class subdirectories
                os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)
                os.makedirs(os.path.join(val_dir, class_name), exist_ok=True)
                
                # Get image files
                files = [f for f in os.listdir(class_path) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                
                if not files:
                    print(f"Warning: No images found in {class_path}")
                    continue
                
                random.shuffle(files)
                split_idx = int(len(files) * ratio[0])
                
                # Copy files
                for f in files[:split_idx]:
                    shutil.copy2(os.path.join(class_path, f),
                                os.path.join(train_dir, class_name, f))
                
                for f in files[split_idx:]:
                    shutil.copy2(os.path.join(class_path, f),
                                os.path.join(val_dir, class_name, f))
        
        print(f"Successfully split dataset to {output_dir}")
        return True
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    input_folder = 'CNN_data_48x48'
    output_folder = 'splitdataset148x48'
    
    # Verify paths
    print(f"Current working directory: {os.getcwd()}")
    print(f"Looking for input folder at: {os.path.abspath(input_folder)}")
    
    if not os.path.exists(input_folder):
        print("\nERROR: Input folder not found. Please:")
        print(f"1. Create a folder named '{input_folder}'")
        print(f"2. Put it in: {os.getcwd()}")
        print("3. Inside it, create subfolders for each class (A/, B/, etc.)")
        print("4. Place corresponding images in each class folder")
    else:
        success = split_dataset(input_folder, output_folder)
        if success:
            print("Operation completed successfully!")