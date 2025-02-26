import sys
import os


def extract_logs(log_file, date):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists
    output_file = f"{output_dir}/output_{date}.txt"

    try:
        with open(log_file, "r") as f_in, open(output_file, "w") as f_out:
            for line in f_in:
                if line.startswith(date):  # Efficient check at the beginning of the line
                    f_out.write(line)

        print(f"Logs for {date} have been saved to {output_file}")

    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python extract_logs.py <YYYY-MM-DD>")
        sys.exit(1)

    log_file = "filepath"
    date = sys.argv[1]

    extract_logs(log_file, date)
