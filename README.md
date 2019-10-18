# dynamic-wallpaper
A python script made to emulate Mojave dynamic wallpapers on KDE. 

<p align="center">
<img src="https://media.giphy.com/media/hW9hfkGAbfMcN4LXoU/giphy.gif">
</p>

### How to use
- Find some images
- Store those images inside a folder with a file named **image.xml**
- Modify the XML file stating a name and time for each image (the time indicates when the image swap will occur)
#### Example
```xml
<images>
	<image>
		<name>image1.png</name>
		<time>01:00</time>
	</image>
  <image>
		<name>image2.png</name>
		<time>18:00</time>
	</image>
<images>
```
*(Use this exact sintax for each image)*
 - Then execute dynwall.sh script using the **folder path** as an argument
 #### Example
 ```bash
   ./dynwall.sh /home/username/Picture/Wallpapers
 ```
 
 
### Disclaimer
The images used in the preview GIF are from https://www.artstation.com/dakadibuja. You can find them here https://www.artstation.com/artwork/1VBvq
