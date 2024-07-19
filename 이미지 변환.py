from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import os
import random
import string

# 필터 종류 리스트
filters = ['흑백', '블러', '엣지', '가우시안', '세피아']

# 폰트 디렉토리 설정
font_dir = 'fonts'  # 폰트 파일들이 저장된 디렉토리 경로

# 필터 함수 정의
def apply_random_filter(image):
    if image.mode != 'RGB':
        image = image.convert('RGB')
    filter_type = random.choice(filters)
    if filter_type == '흑백':
        return image.convert('L')
    elif filter_type == '블러':
        return image.filter(ImageFilter.BLUR)
    elif filter_type == '엣지':
        return image.filter(ImageFilter.FIND_EDGES)
    elif filter_type == '가우시안':
        return image.filter(ImageFilter.GaussianBlur)
    elif filter_type == '세피아':
        sepia = ImageOps.colorize(image.convert('L'), '#704214', '#C0C090')
        return sepia
    else:
        return image

# 랜덤 폰트 가져오기
def get_random_font(font_size):
    fonts = [os.path.join(font_dir, f) for f in os.listdir(font_dir) if f.endswith('.ttf')]
    if not fonts:
        raise FileNotFoundError("No font files found in the font directory.")
    font_path = random.choice(fonts)
    return ImageFont.truetype(font_path, font_size)

# 텍스트 추가 함수 정의 (중앙 정렬)
def add_text(image, texts, shadow=False, outline=False):
    draw = ImageDraw.Draw(image)
    font_size = int(image.height * 0.05)
    try:
        font = get_random_font(font_size)
    except FileNotFoundError as e:
        print(e)
        return

    # 텍스트를 중앙에 정렬
    total_text_height = sum(draw.textbbox((0, 0), text, font=font)[3] - draw.textbbox((0, 0), text, font=font)[1] for text in texts) + (len(texts) - 1) * 10
    y_offset = (image.height - total_text_height) // 2

    for text in texts:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((image.width - text_width) // 2, y_offset)
        y_offset += text_height + 10

        text_color = tuple(random.randint(0, 255) for _ in range(3))
        outline_color = tuple(random.randint(0, 255) for _ in range(3))
        
        if shadow:
            shadow_color = (0, 0, 0)
            try:
                draw.text((position[0] - 1, position[1] - 1), text, font=font, fill=shadow_color)
                draw.text((position[0] + 1, position[1] - 1), text, font=font, fill=shadow_color)
                draw.text((position[0] - 1, position[1] + 1), text, font=font, fill=shadow_color)
                draw.text((position[0] + 1, position[1] + 1), text, font=font, fill=shadow_color)
            except Exception as e:
                print(f"Shadow error: {e}")
        
        if outline:
            try:
                draw.text((position[0] - 1, position[1]), text, font=font, fill=outline_color)
                draw.text((position[0] + 1, position[1]), text, font=font, fill=outline_color)
                draw.text((position[0], position[1] - 1), text, font=font, fill=outline_color)
                draw.text((position[0], position[1] + 1), text, font=font, fill=outline_color)
            except Exception as e:
                print(f"Outline error: {e}")
        
        try:
            draw.text(position, text, font=font, fill=text_color)
        except Exception as e:
            print(f"Text error: {e}")

# 랜덤 테두리 추가 함수 정의
def add_random_border(image):
    max_border_size = min(image.width, image.height) // 10
    border_size = random.randint(5, max_border_size)
    color = tuple(random.randint(0, 255) for _ in range(3))  # RGB 색상 생성

    bordered_image = Image.new('RGB', (image.width + 2*border_size, image.height + 2*border_size), color)
    bordered_image.paste(image, (border_size, border_size))

    draw = ImageDraw.Draw(bordered_image)
    shape_type = random.choice(['rectangle', 'circle', 'ellipse'])
    if shape_type == 'rectangle':
        draw.rectangle([(border_size, border_size), (bordered_image.width - border_size, bordered_image.height - border_size)], outline=color, width=border_size)
    elif shape_type == 'circle':
        draw.ellipse([(border_size, border_size), (bordered_image.width - border_size, bordered_image.height - border_size)], outline=color, width=border_size)
    elif shape_type == 'ellipse':
        draw.ellipse([(border_size, border_size), (bordered_image.width - border_size, bordered_image.height - border_size)], outline=color, width=border_size)
    
    return bordered_image

# 단색 이미지 생성 함수 정의
def create_solid_color_image(size, color):
    return Image.new('RGB', size, color)

# 파일명에서 사용할 수 없는 문자 제거 함수
def sanitize_filename(filename):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    return ''.join(c for c in filename if c in valid_chars)

# 랜덤 파일명 생성 함수
def generate_random_filename(extension):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12)) + extension

# 입력 디렉토리와 출력 디렉토리 설정
input_dir = 'input'
output_dir = 'output'

# 이미지 처리 함수
def process_images():
    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_path = os.path.join(input_dir, filename)
            image = Image.open(image_path)

            try:
                # 랜덤 필터 적용
                image = apply_random_filter(image)

                # 텍스트 추가
                add_text(image, ['롤 대리 쿠키팀', 'https://쿠키팀.com', '카카오톡 ID : COOKIETEAM9'], shadow=True, outline=True)

                # 랜덤 테두리 추가
                image = add_random_border(image)

                # 랜덤 파일명 생성
                extension = os.path.splitext(filename)[1]
                random_filename = generate_random_filename(extension)
                
                # 결과 이미지 저장
                output_path = os.path.join(output_dir, random_filename)
                image.save(output_path)
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# 단색 이미지 생성 및 처리 함수
def create_and_process_solid_images():
    colors = ['red', 'green', 'blue', 'yellow']
    for i, color in enumerate(colors):
        image = create_solid_color_image((800, 600), color)

        try:
            # 텍스트 추가
            add_text(image, ['롤 대리 쿠키팀', 'https://쿠키팀.com', '카카오톡 ID : COOKIETEAM9'], shadow=True, outline=True)

            # 랜덤 테두리 추가
            image = add_random_border(image)

            # 랜덤 파일명 생성
            random_filename = generate_random_filename('.png')
            
            # 결과 이미지 저장
            output_path = os.path.join(output_dir, random_filename)
            image.save(output_path)
        except Exception as e:
            print(f"Error processing solid color image {i+1}: {e}")

# 메인 함수
def main():
    process_images()
    create_and_process_solid_images()

if __name__ == "__main__":
    main()
