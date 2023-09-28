import sys
import destinguish_colors.color_tools as ct

def main():
    if len(sys.argv) > 1:
        return ct.generate_distinguishable_colors(int(sys.argv[1]))

    else:
        return ct.generate_distinguishable_colors(10)

if __name__ == "__main__":
    main()