from shredder import cross_shred


def main():
    strip_size = 32
    user_image = "test.jpg"

    cross_shred(user_image, strip_size)


if __name__ == "__main__":
    main()
