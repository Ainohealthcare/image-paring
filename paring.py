import csv

# CSV 파일에서 해시 값을 로드하는 함수
def load_hashes_from_csv(csv_filename):
    hashes = {}
    with open(csv_filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            hashes[row[0]] = row[1]
    return hashes

# 이미지 해시를 비교하여 페어링하는 함수
def pair_images(original_hashes, resized_hashes, threshold=5):
    pairs = []
    unmatched = list(original_hashes.keys())  # 일치하지 않는 원본 이미지 추적
    total_pairs = len(original_hashes) * len(resized_hashes)
    current_pair = 0
    for orig_filename, orig_hash in original_hashes.items():
        best_match = None
        best_diff = float('inf')
        for res_filename, res_hash in resized_hashes.items():
            current_pair += 1
            if current_pair % 100 == 0:  # 100번째 비교마다 진행 상황 출력
                print(f"Progress: {current_pair}/{total_pairs} pairs compared")

            diff = abs(int(orig_hash, 16) - int(res_hash, 16))
            if diff < best_diff and diff < threshold:
                best_match = res_filename
                best_diff = diff
        if best_match:
            pairs.append((orig_filename, best_match))
            unmatched.remove(orig_filename)  # 매칭된 원본 이미지는 목록에서 제거
    return pairs, unmatched
  
# 페어링 결과를 CSV 파일로 저장하는 함수
def save_pairs_to_csv(pairs, csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Original Image", "Resized Image"])
        for orig_filename, res_filename in pairs:
            writer.writerow([orig_filename, res_filename])

# CSV 파일에서 해시 값 불러오기
original_hashes = load_hashes_from_csv("original_hashes.csv")
resized_hashes = load_hashes_from_csv("resized_hashes.csv")

# 이미지 페어링
print("Pairing images...")
image_pairs, unmatched_images = pair_images(original_hashes, resized_hashes)

# 페어링된 결과를 CSV 파일로 저장
save_pairs_to_csv(image_pairs, "paired_images.csv")

print("완료");
