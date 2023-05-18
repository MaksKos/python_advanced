# pylint: disable=missing-docstring


from distutils.core import setup, Extension


def main():
    setup(name="cjson",
          version="0.1",
          description="json C library",
          author="Maks",
          author_email="my_email@gmail.com",
          ext_modules=[Extension("cjson", ["json.c"],
                                 extra_compile_args=['-Wall', '-Werror'])])


if __name__ == "__main__":
    main()
