from PIL import Image
import imagehash
import csv
import requests

# Supabase URL에서 이미지 해시 생성 함수
def generate_image_hash_from_url(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        image_hash = imagehash.average_hash(image)
        return str(image_hash)
    else:
        print(f"Failed to fetch image from URL: {image_url}")
        return None

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


# supabase내 이미지의 해시 값을 저장할 딕셔너리
resized_hashes = {}

# 리사이즈된 이미지 URL 해시 생성 및 저장
supabase_url_template = "https://lxziyihbxcoatqaarfur.supabase.co/storage/v1/object/public/labeled_image/images/{}.jpeg"

print("Generating hashes for resized images from Supabase...")
for i in range(1, 2034):  # 1부터 2033까지
    if i % 100 == 0:  # 100번째마다 진행 상황 출력
        print(f"Progress: {i}/2034 resized images processed")
    image_url = supabase_url_template.format(i)
    image_hash = generate_image_hash_from_url(image_url)
    if image_hash:
        resized_hashes[f"{i}.jpeg"] = image_hash
        
save_hashes_to_csv(resized_hashes, "resized_hashes.csv")

print("Resized image hashes have been generated and saved to resized_hashes.csv")