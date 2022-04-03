from PIL import Image, ImageOps
def image_filling(mother_path,son_path,save_path,box_size,stretch = False):
    """
    :param mother_path: 被填充的原图路径
    :param son_path: 用来填充的子图路径
    :param save_path: 填充后的图片保存的路径
    :param box_size: 字典，填充区域的左上角坐标和右下角坐标
    :param stretch: 是否拉伸填充，默认为否
    :return: None
    """
    mother_img = Image.open(mother_path)
    son_img = Image.open(son_path)
    #原图尺寸
    mother_size = mother_img.size
    #子图尺寸
    son_size = son_img.size

    box_top_left = box_size['left_top']
    box_right_bottom = box_size['right_bottom']
    #填充区域的宽高
    box_width = box_right_bottom[0] - box_top_left[0]
    box_height = box_right_bottom[1] - box_top_left[1]
    #若box尺寸输入不合理，则报错
    # if box_width > mother_size[0] or box_height > mother_size[1]:
    if box_top_left[0] > box_right_bottom[0] or box_top_left[1] > box_right_bottom[1] or \
            box_top_left[0] < 0 or box_top_left[1] < 0 or box_right_bottom[0] > mother_size[0] or \
            box_right_bottom[1] > mother_size[1]:
        print('error:The box_size is wrong!')

    # box的尺寸长和宽都完全大于子图
    # 若使用拉伸填充，则将子图拉伸后填充到指定位置
    # 若不使用拉升填充，则保持子图大小不变，在其四周填充黑色色使其变为与box尺寸一致后再填充
    else:
        if box_width > son_size[0] or box_height > son_size[1]:
            # 使用拉伸
            if stretch:
                # 拉伸子图的形状
                icon = son_img.resize((box_width, box_height))
                mother_img.paste(icon, box_top_left)
                mother_img.save(save_path)
            # 不使用拉伸
            else:
                # 子图四周填充黑色的尺寸
                left = int((box_width - son_size[0]) / 2)
                right = box_width - left - son_size[0]
                top = int((box_height - son_size[1]) / 2)
                botton = box_height - top - son_size[1]
                # print(left, top, right, botton)
                icon = ImageOps.expand(son_img, border=(left, top, right, botton), fill=(0, 0, 0))
                mother_img.paste(icon, box_top_left)
                mother_img.save(save_path)
        else:
            # 使用拉伸
            if stretch:
                icon = son_img.resize((box_width, box_height))
                mother_img.paste(icon, box_top_left)
                mother_img.save(save_path)
            else:
                # 判断子图宽度是否超过box的宽度，若超过则居中裁剪
                if son_size[0] > box_width:
                    crop_left = int((son_size[0] - box_width) / 2)
                    # crop_right = son_size[0] - crop_left - box_width
                    crop_right = crop_left + box_width
                else:
                    crop_left = 0
                    crop_right = son_size[0]

                # 判断子图高度是否超过box的高度，若超过则居中裁剪
                if son_size[1] > box_height:
                    crop_top = int((son_size[1] - box_height) / 2)
                    crop_botton = crop_top + box_height
                else:
                    crop_top = 0
                    crop_botton = son_size[1]

                new_icon = son_img.crop((crop_left, crop_top, crop_right, crop_botton))
                # 将裁剪后的子图插入原图
                new_icon_size = new_icon.size
                # 新的子图四周填充黑色的尺寸
                left = int((box_width - new_icon_size[0]) / 2)
                right = box_width - left - new_icon_size[0]
                top = int((box_height - new_icon_size[1]) / 2)
                botton = box_height - top - new_icon_size[1]

                new_icon = ImageOps.expand(new_icon, border=(left, top, right, botton), fill=(0, 0, 0))
                mother_img.paste(new_icon, box_top_left)
                mother_img.save(save_path)

if __name__ == "__main__":
    mother_path = 'mother.png'
    son_path = 'son.png'
    save_path = 'last.png'
    box_size = {'left_top':[0,200],'right_bottom':[50,600]}
    image_filling(mother_path = mother_path,son_path = son_path,save_path = save_path,box_size = box_size,stretch=False)


