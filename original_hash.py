import os
from PIL import Image
import imagehash
import csv

# 이미지 해시 생성 함수
def generate_image_hash(image):
    image_hash = imagehash.average_hash(image)
    return str(image_hash)

# 이미지 필터링 및 리사이즈 함수
def image_filter(f):
    OUT_SIZE = 512
    (width, height) = f.size
    return (width >= OUT_SIZE) and (height >= OUT_SIZE)

def image_process(f):
    OUT_SIZE = 512
    return f.crop(calc_center(f.size)).resize((OUT_SIZE, OUT_SIZE))

# 이미지를 중앙에서 크롭하여 리사이즈하기 위한 계산 함수
def calc_center(size):
    (width, height) = size
    if width > height:
        left = (width - height) / 2
        right = (width + height) / 2
        return (left, 0, right, height)
    else:
        top = (height - width) / 2
        bottom = (height + width) / 2
        return (0, top, width, bottom)

# 해시 값을 CSV 파일에 저장하는 함수
def save_hashes_to_csv(hashes, csv_filename):
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for filename, img_hash in hashes.items():
            writer.writerow([filename, img_hash])

# 원본 이미지 디렉토리 설정
original_base_dir = "./original_images"

# 원본 이미지의 해시 값을 저장할 딕셔너리
original_hashes = {}

# 원본 이미지 해시 생성 및 저장 (모든 하위 폴더 포함)
print("Generating hashes for original images...")
for root, dirs, files in os.walk(original_base_dir):
    for filename in files:
        if filename.endswith(".jpeg") or filename.endswith(".png"):  # JPEG와 PNG 둘 다 처리
            file_path = os.path.join(root, filename)
            try:
                with Image.open(file_path, 'r') as f:
                    if image_filter(f):
                        # 이미지가 512x512 이상인 경우 리사이즈 후 해시 생성
                        processed_image = image_process(f)
                        original_hashes[file_path] = generate_image_hash(processed_image)
                    else:
                        # 리사이즈되지 않은 원본 이미지의 해시 생성
                        original_hashes[file_path] = generate_image_hash(f)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# 해시 값을 CSV 파일로 저장 (UTF-8 인코딩 사용)
save_hashes_to_csv(original_hashes, "original_hashes.csv")

print("Original image hashes have been generated and saved to original_hashes.csv")