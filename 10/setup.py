from distutils.core import setup, Extension

def main():
    setup(name="cjson",
          version="0.1",
          description="json C library",
          author="Maks",
          author_email="my_email@gmail.com",
          ext_modules=[Extension("cjson", ["json.c"])])

if __name__ == "__main__":
    main()
