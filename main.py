import os
import time
import sys
from cleaner import DuplicateDetector, TempCleaner
from exceptions import CriticalFileAccessError
from utils import format_size_logarithmic
import pyfiglet


def display_menu():
    width = 56
    print("\n" + "╔" + "═" * (width - 2) + "╗")
    print("║" + " ADVANCED SYSTEM CLEANER & DUPLICATE DETECTOR ".center(width - 2) + "║")
    print("╠" + "═" * (width - 2) + "╣")
    print("║" + "  [1] SCAN SYSTEM %TEMP% DIRECTORY".ljust(width - 2) + "║")
    print("║" + "  [2] SCAN CUSTOM TARGET DIRECTORY".ljust(width - 2) + "║")
    print("║" + "  [3] TERMINATE APPLICATION".ljust(width - 2) + "║")
    print("╚" + "═" * (width - 2) + "╝")


def handle_cleanup(target_path):
    if not target_path:
        print("\n Error: Absolute directory path cannot be empty.")
        return

    duplicate_detector = DuplicateDetector()
    temp_cleaner = TempCleaner()
    files_to_remove = set()

    try:

        print("\n Running Statistical Numerical Logic Analysis...")
        density_report, total_bytes = duplicate_detector.calculate_size_density(target_path)

        print("\n" + "=" * 20 + " STORAGE DENSITY REPORT " + "=" * 20)
        for category, metrics in density_report.items():
            print(
                f" • {category.ljust(20)} : {metrics['file_count']} files ({metrics['percentage_of_disk']}% of total storage)")
        print("=" * 64)

        suspicious = temp_cleaner.analyze_temp_files(path=target_path)
        if suspicious:
            print(f"\n Analysis: Detected {len(suspicious)} volatile system files (.log/.tmp).")
            if input("» Queue these files for erase permanently? (y/n): ").lower() == 'y':
                files_to_remove.update(suspicious)

        duplicates = duplicate_detector.analyze_duplicates(path=target_path)
        if duplicates:
            print(f"\n Analysis: Identified {len(duplicates)} redundant duplicate groups.")
            all_dupes = []

            print("-" * 56)
            for f_hash, paths in duplicates.items():
                print(f"Hash {f_hash[:8]}... Original: {paths[0]}")
                for dupe in paths[1:]:
                    print(f"  └─ Duplicate: {dupe}")
                    all_dupes.append(dupe)
            print("-" * 56)

            all_dupes.sort(key=lambda x: os.path.getsize(x) if os.path.exists(x) else 0, reverse=True)

            if input(f"» Queue all {len(all_dupes)} duplicate replicas? (y/n): ").lower() == 'y':
                files_to_remove.update(all_dupes)

        if files_to_remove:
            print(f"\n Warning: You are about to permanently erase {len(files_to_remove)} queued items.")
            confirm = input("» Type 'yes' to execute data destruction protocol: ").strip().lower()

            if confirm in ['yes', 'y', 'evet']:
                files_snapshot = list(files_to_remove)
                deleted, space = duplicate_detector.clean_files(files_to_remove)

                print("\n" + "-" * 56)
                print(f" Clean-up operation completed successfully.")
                print(f"   • Files Permanently Erased: {deleted}")
                print(f"   • Total Space Recovered: {format_size_logarithmic(space)}")
                print("-" * 56)

                failed_count = len(files_snapshot) - deleted

                duplicate_detector.save_report_json(
                    count=deleted,
                    space=space,
                    deleted_files_list=files_snapshot,
                    error_count=failed_count,
                    target_path=target_path
                )
            else:
                print("\n Aborted: Operation cancelled by user. Safe state maintained.")
        else:
            print("\n Info: Scan finished. Storage optimization queue is empty.")

    except CriticalFileAccessError as e:
        print(f"\n[SECURITY ALERT] {e}")
        print("Operation aborted by safety decorator layer.")


def main():
    base_finder = DuplicateDetector()
    while True:
        display_menu()
        choice = input("Select operation code (1-3): ").strip()
        if choice == '1':
            handle_cleanup(base_finder.get_temp_path())
        elif choice == '2':
            handle_cleanup(input("\nEnter absolute system path: ").strip())
        elif choice == '3':
            print()
            for i in range(3, 0, -1):
                print(f"Closing application safely in {i}...", end="\r")
                time.sleep(1)

            print(" " * 50, end="\r")
            ascii_art_slant = pyfiglet.figlet_format("goodbye", font="slant")
            print(ascii_art_slant)
            print()
            sys.exit(0)
        else:
            print("\n Invalid operation code. Please input 1, 2, or 3.")


if __name__ == "__main__":
    main()