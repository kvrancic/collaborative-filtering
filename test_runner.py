#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_runner.py path_to_tests_folder")
        sys.exit(1)

    tests_folder = sys.argv[1]

    # Collect all *.in files
    in_files = [f for f in os.listdir(tests_folder) if f.endswith('.in')]
    in_files.sort()

    # We'll run CF.py for each .in, compare with the matching .out
    success_count = 0
    fail_count = 0

    for infile in in_files:
        base_name = infile[:-3]  # remove .in
        outfile = base_name + '.out'
        infile_path = os.path.join(tests_folder, infile)
        outfile_path = os.path.join(tests_folder, outfile)

        # Run CF.py < infile
        # We'll capture the output in a variable so we can compare
        try:
            with open(infile_path, 'r') as inf:
                result = subprocess.run(
                    ['python', 'CF.py'],
                    stdin=inf,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=50  # optional: avoid infinite loops
                )
        except subprocess.TimeoutExpired:
            print(f"TIMEOUT: {infile}")
            fail_count += 1
            continue

        if not os.path.exists(outfile_path):
            print(f"Missing expected output file: {outfile}")
            fail_count += 1
            continue

        with open(outfile_path, 'r') as outf:
            expected = outf.read().strip()

        actual = result.stdout.strip()
        if actual == expected:
            print(f"PASS: {infile}")
            success_count += 1
        else:
            print(f"FAIL: {infile}")
            print(" -- Expected: ")
            print(expected)
            print(" -- Got:")
            print(actual)
            fail_count += 1

    print("=================================")
    print(f"Tests passed: {success_count}")
    print(f"Tests failed: {fail_count}")
    print("=================================")

if __name__ == "__main__":
    main()
