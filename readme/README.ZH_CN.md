### 批量给指定文件夹中的图片添加水印

功能：可以批量给指定文件夹中的图片（包括子文件夹）添加水印，并可以设置水印的**位置**、**大小**和**透明度**，满足各种需求。
添加水印后的图片存储结构和原先文件夹相同。

需要用到的依赖库： PILLOW

```
pip install pillow
```

参数：

- directory (str): 需要添加水印的文件夹
- logo_path (str): 水印图片地址
- --position (str): 水印的位置，可以选：topleft, topright, bottomleft, bottomright, center，默认为 center
- --new_directory (str): 存储添加水印后的文件夹地址，默认为 None，即覆盖掉原图
- --padding (int): logo 周围填充的像素，默认为 0
- --transparency (float): 设置 logo 的透明度，默认为 1，即不透明，设置范围为 0 ～ 1
- --scale (int): 改变 logo 图片的大小，默认为 20

使用方法：

```
python addWaterMark.py './images' 'logo.png' --pos center --new_dir './watermarked_images' --transparency 0.3
```

---

本代码由[teitrain/watermark](https://github.com/theitrain/watermar)改进而来
