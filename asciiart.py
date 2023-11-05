# ASCII Art Generator

from PIL import Image
import requests
import time

# Defines the list of ASCII characters used to represent brightness levels in images
# Characters range from less dense to denser representing darker to brighter pixels
ascii_chars = [" ", ".", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]

# Sample images (licensed as creative commons) along with descriptive titles.
samples = [
  # Horizontal image, photo of a Zebra in the African savanna
  ("https://c0.wallpaperflare.com/preview/193/17/205/zebra-in-savanna.jpg", "Zebra in African savanna"),

  # Vertical image, photo of an Emperor Penguin
  ("https://images.rawpixel.com/image_800/cHJpdmF0ZS9sci9pbWFnZXMvd2Vic2l0ZS8yMDIzLTAzL2ZsMTU2MzAzMDUwMzktaW1hZ2VfMS5qcGc.jpg", "Emperor Penguin"),
]


def get_image(url):
  """Prompt the user for a URL, and load an image.
  """
  if url is None:
    url = input('Enter a URL for your own image (empty to exit): ').strip()
    print()

  if url == '':
    # The user has entered an empty URL. Indicate that by returning None.
    return None

  # Retrieve the image data from the URL, and load the image using PIL
  image_response = requests.get(url, stream = True)
  return Image.open(image_response.raw)


def print_ascii_art(image, title):
  """Takes an image and generates ASCII Art.
  """
  # Resize the image to a smaller size to make the ASCII art less detailed
  width, height = image.size
  aspect_ratio = height / width
  if width > height:
    # Landscape oriented image
    # Ensure image is 120px wide and can fit typical width of terminal windows.
    width = 120
    height = int(width * aspect_ratio * 0.55)
  else:
    # Portrait oriented image
    # Ensure image is 60px tall and can fit the typical height of terminal windows
    height = 60
    width = int(height / aspect_ratio / 0.55)

  image = image.resize((width, height), Image.BICUBIC)

  # Convert each pixel in the image to an ASCII character based on its brightness
  ascii_art = ""

  # Loop through the pixels, row by row and column by column within each row.
  pixels = image.load()
  for row in range(height):
    for column in range(width):
      r, g, b = pixels[column, row]
      brightness = sum([r, g, b]) / 3

      # Brightness ranges from 0..255. Divide by 25 and truncate to an integer to get 0..10.
      # Use this to index into the list of ASCII characters
      ascii_art += ascii_chars[int(brightness / 25)]
    ascii_art += "\n"

  # Print the ASCII art to the console
  if title is None:
    if width > height:
      print(f"Generating ASCII art for Landscape Image")
    else:
      print(f"Generating ASCII art for Portrait Image")
  else:
    print(f"Generating ASCII art for {title}")
  print()
  time.sleep(1)
  print(ascii_art)


def main():
  print("ASCII art generator.")
  print("You'll be given two samples, horizontal and vertical.")
  print("Then, you can enter a custom image!")
  print("------------------------------------------------------")

  # Generate ASCII art for sample images
  for sample in samples:
    time.sleep(3)
    print()
    print_ascii_art(get_image(sample[0]), sample[1])

  # Generate ASCII art for user's images. Keep asking and generating
  # until the user stops providing an image.
  while True:
    try:
      image = get_image(None)
      if image is None:
        break
  
      time.sleep(3)
      print_ascii_art(image, None)
    except:
      print("The image could not be loaded.")
    print()


main()
