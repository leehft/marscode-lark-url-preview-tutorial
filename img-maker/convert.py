from PIL import Image

def map_color_to_transparency(image_path):
    # 打开图像
    img = Image.open(image_path).convert("RGBA")
    
    # 获取图像数据
    data = img.getdata()
    
    # 创建一个新的图像数据列表
    new_data = []
    
    # 遍历每个像素
    for item in data:
        # 计算灰度值
        gray = int(0.2989 * item[0] + 0.5870 * item[1] + 0.1140 * item[2])
        
        # 将灰度值映射到透明度（255 - 灰度值）
        new_data.append((255, 255, 255, 255 - gray))
    
    # 更新图像数据
    img.putdata(new_data)
    
    # 保存处理后的图像
    img.save("output.png")

# 使用示例
map_color_to_transparency("input.png")
