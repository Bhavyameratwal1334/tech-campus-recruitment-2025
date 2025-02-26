import argparse
import os
import mmap
import re


def find_first_occurrence(mm, target_date):
    """
    Binary search to locate the first occurrence of a line that starts with target_date.
    Assumes each line begins with a timestamp in the format YYYY-MM-DD.
    """
    left = 0
    right = mm.size()
    first_match = None

    while left < right:
        mid = (left + right) // 2
        # move to the start of the next line
        mm.seek(mid)
        mm.readline()  # discard incomplete line
        pos = mm.tell()
        line = mm.readline()
        if not line:
            break
        try:
            # decode a bit of the line and extract the date
            line_str = line.decode('utf-8')
        except UnicodeDecodeError:
            # In case of decode issues, skip
            left = pos + len(line)
            continue

        # Compare the date at the beginning of the line
        if line_str.startswith(target_date):
            first_match = pos
            right = mid  # search further left for an earlier occurrence
        elif line_str[:10] < target_date:
            left = pos + len(line)
        else:
            right = mid

    return first_match


def extract_logs_for_date(log_file, target_date, output_file):
    with open(log_file, 'rb') as f:
        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_READ) as mm:
            start_pos = find_first_occurrence(mm, target_date)
            if start_pos is None:
                print(f"No logs found for {target_date}")
                return

            mm.seek(start_pos)
            with open(output_file, 'w', encoding='utf-8') as out:
                while True:
                    pos = mm.tell()
                    line = mm.readline()
                    if not line:
                        break  # End of file reached
                    try:
                        line_str = line.decode('utf-8')
                    except UnicodeDecodeError:
                        continue  # Skip problematic lines

                    # Since each log entry starts with a timestamp, compare the date
                    if not line_str.startswith(target_date):
                        # Because file is sorted, once the date changes, we can stop.
                        break
                    out.write(line_str)
    print(f"Log entries for {target_date} written to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract logs for a given date from a large log file.")
    parser.add_argument("date", help="Date in format YYYY-MM-DD")
    parser.add_argument("--logfile", default="filepath",
                        help="Path to the log file (default: logs.log)")
    args = parser.parse_args()

    # Basic validation of date format
    if not re.match(r"\d{4}-\d{2}-\d{2}", args.date):
        print("Date must be in the format YYYY-MM-DD")
        return

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"output_{args.date}.txt")

    extract_logs_for_date(args.logfile, args.date, output_file)


if __name__ == "__main__":
    main()
