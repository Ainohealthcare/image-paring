# image-paring
512x512로 resize된 이미지와 원본 이미지를 매칭

### 원본 이미지 해싱
- 코드: original_hash.py
- 방식: ./original_images 내 각 폴더를 모두 접근합니다. 각 폴더 내 원본 이미지들을 리사이즈에 사용한 코드를 이용해 리사이징 후 해시코드 csv를 생성합니다.

### 비교 대상(이전에 리사이즈된) 이미지 해싱
- 코드: resize_hash.py
- 방식: supabase 내 존재하는 이미지들을 접근하여 해시코드 csv를 생성합니다.

### 페어링
- 코드: paring.py
- 방식: original_hash.csv와 resize_hash.csv를 대상으로 각 해시코드의 차가 임계값 5이하면 매칭되었다 간주합니다.
