def calculate_bmp(message_combination_string, userName):
    from PIL import Image, ImageDraw, ImageFont
    # import os
    # from .printer_class import thermoPrinter
    #message_combination_string = ['feeling', 'feeling_comment', 'food', 'food_picture']

    def create_username_png(username, output_path):
        """
        创建包含用户名的透明PNG图片，文本居中显示
        """
        # 固定图片宽度和高度
        width = 570  # 固定宽度
        height = 40  # 固定高度
        
        # 创建透明背景的图片
        img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 设置字体和大小
        try:
            font = ImageFont.truetype("/home/ubuntu/fragrance_dispenser/system_integrations/font/Noto_Sans_JP/static/NotoSansJP-Regular.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        # 获取文本尺寸
        text_width, text_height = draw.textsize(username, font=font)
        
        # 计算居中位置
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # 绘制用户名
        draw.text((x, y), username, fill=(255, 255, 255, 255), font=font)  # 使用白色文字
        
        # 保存PNG
        username_path = "/home/ubuntu/fragrance_dispenser/system_integrations/media/png_dir/username.png"
        img.save(username_path, "PNG")
        return username_path

    def paste_multiple_pngs_to_bmp(base_image_path, output_image_path, overlay_images):
        """
        将多个 PNG 图片粘贴到 BMP 图片上，并输出为新的 BMP 文件。

        参数:
        - base_image_path: str, 底层 BMP 文件路径。
        - output_image_path: str, 输出 BMP 文件路径。
        - overlay_images: list of tuples, 每个元组包含要粘贴的 PNG 文件路径和粘贴位置的 (x, y) 坐标。
        """
        # 打开底层 BMP 图片
        with Image.open(base_image_path) as base_image:
            # 检查底层图像是否为 BMP 格式
            if base_image.format != 'BMP':
                raise ValueError("Base image must be in BMP format.")
            
            # 逐个处理 PNG 覆盖图像
            for overlay_image_path, position in overlay_images:
                with Image.open(overlay_image_path) as overlay_image:
                    # 将 PNG 转换为支持透明度的 RGBA 格式
                    overlay_image = overlay_image.convert("RGBA")
                    
                    # 粘贴 PNG 图像到 BMP 上
                    base_image.paste(overlay_image, position, overlay_image)  # 使用 overlay_image 作为掩码支持透明度
                    
                    print(f"Pasted {overlay_image_path} at {position}")

            # 保存合成后的 BMP 文件
            base_image.save(output_image_path, format="BMP")
            print(f"Saved final image as {output_image_path}")

    # 示例用法
    base_image_path = "/home/ubuntu/fragrance_dispenser/system_integrations/media/base/base.bmp"        # 底层 BMP 文件路径
    output_image_path = "/home/ubuntu/fragrance_dispenser/system_integrations/media/output/toprint_best.bmp"    # 输出 BMP 文件路径

    # 生成用户名PNG
    username_png_path = create_username_png(userName, "username.png")
    print(username_png_path)
    
    # 要粘贴的 PNG 文件及位置列表
    overlay_images = [
        ("/home/ubuntu/fragrance_dispenser/system_integrations/media/png_dir/feeling/{}.png".format(message_combination_string[0]), (300, 440)),
        ("/home/ubuntu/fragrance_dispenser/system_integrations/media/png_dir/feeling_comment/{}.png".format(message_combination_string[1]), (30, 810)),
        ("/home/ubuntu/fragrance_dispenser/system_integrations/media/png_dir/food/{}.png".format(message_combination_string[2]), (20, 440)),
        ("/home/ubuntu/fragrance_dispenser/system_integrations/media/png_dir/food_picture/{}.png".format(message_combination_string[3]), (340, 730)),
        (username_png_path, (0, 340)),  # 添加用户名图片，位置可以根据需要调整
    ]
    
    paste_multiple_pngs_to_bmp(base_image_path, output_image_path, overlay_images)

calculate_bmp(['いらいら', 'いらいら', '?きのこスープ', '?きのこスープ'], 'キキ')

    # printer_port = '/dev/usb/lp0'
    # printer = thermoPrinter(printer_port, './cpp_bin')
    # printer_port = printer_port
    # script_path = os.getcwd()
    # imgPath1 = f'{script_path}/media/output/toprint.bmp'
    # imgPath2 = f'{script_path}/media/base/comment.bmp'
    # printer.PrintRasterImage(imgPath1)
    # printer.FeedAndHalfCut()
    # printer.PrintRasterImage(imgPath2)
    # printer.FeedAndFullCut()