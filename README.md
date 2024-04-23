### Add watermark to pictures in specified folder batchly without quality loss

[中文 ZH-CN](readme/README.ZH_CN.md)

Function: You can batch add watermarks to pictures in specified folders (including subfolders) and set the **position**, **size** and **transparency** of the watermarks to meet various needs.
The storage structure of the pictures after adding watermark is the same as the original folder.

**The code can add a watermark to the image losslessly**, the size and resolution of the image after adding the watermark are almost unchanged. You can easily add watermarks to the PSed pictures to be shared.

Required dependencies: PILLOW

```
pip install pillow
```

Parameters：

- directory (str): The image folder where the watermark should be added
- logo_path (str): Folder address of the watermark image
- --position (str): The position of the watermark, you can choose:**topleft**, **topright**, **bottomleft**, **bottomright**, **center**. Default is center
- --new_directory (str): Address of the folder where the watermark will be stored. Default is None, overwrite the original image.
- --padding (int): Pixel padding around the watermark. Default is 0
- --transparency (float): Set the transparency of the watermark. Default is 1, the range is 0~1
- --scale (int): Change the size of the logo image. Default is 20

Usage:

```
python addWaterMark.py './images' 'logo.png' --pos center --new_dir './watermarked_images' --transparency 0.3
```

---

This code was improved by [teitrain/watermark](https://github.com/theitrain/watermar)
