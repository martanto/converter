from scan import Scan
from settings import settings
from convert import ConvertToMseed

def main():
    mseed = ConvertToMseed()
    mseed.convert()

if __name__ == '__main__':
    main()