# String Art of Images

A simple algorithm designed to produce a string/thread representation of an image. 

Original idea by Petros Vrellis: [A new way to knit (2016)](http://artof01.com/vrellis/works/knit.html). 

### Examples

![ScreenShot](https://github.com/kristapratico/string_art_of_images/blob/master/images/johnm_cropped.png)
![ScreenShot](https://github.com/kristapratico/string_art_of_images/blob/master/images/johnm_results.png)

![ScreenShot](https://github.com/kristapratico/string_art_of_images/blob/master/images/dad_cropped.png)
![ScreenShot](https://github.com/kristapratico/string_art_of_images/blob/master/images/dad_results.png)

![ScreenShot](https://github.com/kristapratico/string_art_of_images/blob/master/images/dan_cropped.png)
![ScreenShot](https://github.com/kristapratico/string_art_of_images/blob/master/images/dan_results.png)

![ScreenShot](https://github.com/kristapratico/string_art_of_images/blob/master/images/heart_cropped.png)
![ScreenShot](https://github.com/kristapratico/string_art_of_images/blob/master/images/heart_results.png)

![ScreenShot](https://github.com/kristapratico/string_art_of_images/blob/master/images/kitty_cropped.png)
![ScreenShot](https://github.com/kristapratico/string_art_of_images/blob/master/images/kitty_results.png)

### Prerequisites

* Numpy

* OpenCV

### Running

**Usage:** ./string_line.py [ image_name ] [ number_lines (optional) ]

If number_lines not included in command line arguments, it will default to 1000 lines.

```
./string_line.py image.jpg
```
or

```
./string_line.py image.png 500
```
Image must be in same directory. Result file will be appended with "_results".

## Acknowledgments

* Petros Vrellis: [A new way to knit (2016)](http://artof01.com/vrellis/works/knit.html)
* Inspired by GoldPlatedGoof's [video](https://www.youtube.com/watch?v=-S_l8GGxOhU)
