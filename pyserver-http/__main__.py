from .main import main

if __name__ == "__main__":
    from argparse import ArgumentParser
    parser = ArgumentParser(prog= "http_server", description="http server")
    parser.add_argument("-d", "--directory", action="store", default="files", type=str)
    args = parser.parse_args()
    main(args.directory)