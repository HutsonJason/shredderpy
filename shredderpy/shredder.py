import math
from dataclasses import dataclass, field

from PIL import Image


def cross_shred(image: str, strip_size: int):
    user_image = Image.open(image)
    original_width = user_image.size[0]
    original_height = user_image.size[1]
    new_image_data = ImageSizes(
        strip_size=strip_size, image_width=original_width, image_height=original_height
    )
    new_width = new_image_data.new_width
    new_height = new_image_data.new_height
    strip_amount_width = new_image_data.strip_amount_width
    strip_width = new_image_data.strip_width
    strip_amount_height = new_image_data.strip_amount_height
    strip_height = new_image_data.strip_height

    # Perform vertical shredding
    vertical_image_shred1 = Image.new("RGBA", (new_width, original_height))
    vertical_image_shred2 = Image.new("RGBA", (new_width, original_height))
    image1_count = 0
    image2_count = 0

    for i in range(strip_amount_width):
        # Get the strip (region) to copy from the original image
        strip = (i * strip_width, 0, (i * strip_width) + strip_width, original_height)
        region = user_image.crop(strip)

        # We create 2 different images with the strips, pasting every other one to them.
        # Even counts
        if i % 2 == 0:
            vertical_image_shred1.paste(region, (image1_count * strip_width, 0))
            image1_count += 1
        # Odd counts
        else:
            vertical_image_shred2.paste(region, (image2_count * strip_width, 0))
            image2_count += 1

    # Perform horizontal shredding
    output_image1 = Image.new("RGBA", (new_width, new_height))
    output_image2 = Image.new("RGBA", (new_width, new_height))
    output_image3 = Image.new("RGBA", (new_width, new_height))
    output_image4 = Image.new("RGBA", (new_width, new_height))

    image1_count = 0
    image2_count = 0

    for i in range(strip_amount_height):
        # Get the strip (region) to copy from the vertical_image_shred.
        strip = (0, i * strip_height, new_width, (i * strip_height) + strip_height)
        region1 = vertical_image_shred1.crop(strip)
        region2 = vertical_image_shred2.crop(strip)

        # We create 4 different images with the strips, pasting every other one to them.
        # Even counts
        if i % 2 == 0:
            output_image1.paste(region1, (0, image1_count * strip_height))
            output_image2.paste(region2, (0, image1_count * strip_height))
            image1_count += 1
        else:
            output_image3.paste(region1, (0, image1_count * strip_height))
            output_image4.paste(region2, (0, image1_count * strip_height))

    # Save the images.
    # !! This should be returned or done better.
    output_image1.save(f"image1.png", format="PNG")
    output_image2.save(f"image2.png", format="PNG")
    output_image3.save(f"image3.png", format="PNG")
    output_image4.save(f"image4.png", format="PNG")


@dataclass
class ImageSizes:
    strip_size: int
    image_width: int
    image_height: int

    # Image width vars
    new_width: int = field(init=False)
    _even_image_width: int = field(init=False)
    strip_amount_width: int = field(init=False)
    strip_width: int = field(init=False)

    # Image height vars
    new_height: int = field(init=False)
    _even_image_height: int = field(init=False)
    strip_amount_height: int = field(init=False)
    strip_height: int = field(init=False)

    def __post_init__(self) -> None:
        # Image width
        if self.image_width % 2 != 0:
            self._even_image_width = self.image_width - 1
        else:
            self._even_image_width = self.image_width
        self.new_width = int(self._even_image_width / 2)
        self.strip_amount_width = math.floor(self._even_image_width / self.strip_size)
        self.strip_width = int(self._even_image_width / self.strip_amount_width)
        # Image height
        if self.image_height % 2 != 0:
            self._even_image_height = self.image_height - 1
        else:
            self._even_image_height = self.image_height
        self.new_height = int(self._even_image_height / 2)
        self.strip_amount_height = math.floor(self._even_image_height / self.strip_size)
        self.strip_height = int(self._even_image_height / self.strip_amount_height)
