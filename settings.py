import os
import sys

ROOT_DIR = os.path.dirname(__file__)  # Go two levels up from src to get the project root

# Add the project root directory to the system path
sys.path.append(ROOT_DIR)

DATASET_DIR = os.path.join(ROOT_DIR, 'resources/dataset/')
IMG_DIR = os.path.join(ROOT_DIR, 'resources/images/')
# CONFIG_DIR = os.path.join(ROOT_DIR, 'config')

# print(DATASET_DIR)