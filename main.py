from scan import Scan
from settings import settings
from convert import ConvertToMseed
import multiprocessing

def main():
    print("Jumlah CPU : ", multiprocessing.cpu_count())
    ConvertToMseed().convert_and_plot(use_cpu=10)

if __name__ == '__main__':
    main()