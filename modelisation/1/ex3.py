t = input("Enter a time in seconds:")
def convert_time(t: int):
    hours = t // 3600
    minutes = (t % 3600) // 60
    seconds = t % 60
    print(f"{t}s correspondent à {hours} h {minutes} mn {seconds} s")

convert_time(int(t))