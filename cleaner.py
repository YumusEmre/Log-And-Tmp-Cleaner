import os
import hashlib
import re
import json
from exceptions import CriticalFileAccessError
from utils import safe_execution, format_size_logarithmic


class BaseScanner:

    def __init__(self):
        self.files_manifest = {}

    def get_temp_path(self):
        return os.environ.get('TEMP') or os.environ.get('TMP')

    def scan_directory_generator(self, directory_path):
        try:
            for root, _, files in os.walk(directory_path):
                for file in files:
                    yield os.path.join(root, file)
        except Exception as e:
            print(f"Scan allocation error: {e}")

    def calculate_size_density(self, target_path):

        ranges = {
            "Tiny (< 1KB)": (0, 1024),
            "Small (1KB - 1MB)": (1024, 1024 * 1024),
            "Medium (1MB - 10MB)": (1024 * 1024, 10 * 1024 * 1024),
            "Large (> 10MB)": (10 * 1024 * 1024, float('inf'))
        }

        distribution = {k: {"count": 0, "total_bytes": 0} for k in ranges}
        global_total_bytes = 0

        for file_path in self.scan_directory_generator(target_path):
            try:
                if os.path.exists(file_path):
                    f_size = os.path.getsize(file_path)
                    global_total_bytes += f_size

                    for label, (low, high) in ranges.items():
                        if low <= f_size < high:
                            distribution[label]["count"] += 1
                            distribution[label]["total_bytes"] += f_size
                            break
            except Exception:
                continue

        report_metrics = {}
        for label, metrics in distribution.items():
            if global_total_bytes > 0:
                percentage = (metrics["total_bytes"] / global_total_bytes) * 100
            else:
                percentage = 0.0

            report_metrics[label] = {
                "file_count": metrics["count"],
                "percentage_of_disk": round(percentage, 2)
            }

        return report_metrics, global_total_bytes

    def clean_files(self, files_to_delete):
        deleted, space = 0, 0

        for path in files_to_delete:
            try:
                if os.path.exists(path) and (not os.path.isdir(path)):
                    space += os.path.getsize(path)
                    os.remove(path)
                    deleted += 1
            except Exception as e:
                print(f" Failed to delete target {path}: {e} ")

        if deleted > 0:
            print(f" -> Execution Motor: Erased {deleted} file elements successfully.")

        return deleted, space

    def save_report_json(self, count, space, deleted_files_list, error_count, target_path, report_path="report.json"):
        import datetime

        report_data = {
            "metadata": {
                "application_name": "Storage Optimizer CLI",
                "execution_timestamp": datetime.datetime.now().isoformat(),
                "target_directory_scanned": target_path
            },
            "performance_metrics": {
                "total_items_erased": count,
                "space_recovered": format_size_logarithmic(space)
            },
            "execution_telemetry": {
                "operation_status": "COMPLETED" if error_count == 0 else "PARTIALLY_COMPLETED",
                "critical_access_errors_encountered": error_count
            },
            "deleted_items": deleted_files_list
        }

        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=4, ensure_ascii=False)
            print(f" Extended audit report securely saved to '{report_path}'.")
        except IOError as e:
            print(f" Failed to export structured json database report: {e}")


class DuplicateDetector(BaseScanner):
    def calculate_sha1(self, file_path):
        sha1 = hashlib.sha1()
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha1.update(chunk)
            return sha1.hexdigest()
        except (PermissionError, FileNotFoundError):
            raise CriticalFileAccessError(f"Cannot read: {file_path}")
        except OSError:
            raise CriticalFileAccessError(f"Socket/System channel skipped: {file_path}")

    @safe_execution
    def analyze_duplicates(self, path):
        self.files_manifest.clear()
        print(f"Analyzing Duplicates inside: {path}...")

        for file_path in self.scan_directory_generator(path):
            try:
                f_hash = self.calculate_sha1(file_path)
                self.files_manifest.setdefault(f_hash, []).append(file_path)
            except CriticalFileAccessError:
                continue

        duplicates = {k: v for k, v in self.files_manifest.items() if len(v) > 1}

        for f_hash in duplicates:
            duplicates[f_hash].sort(key=lambda path_str: path_str.count(os.sep))

        return duplicates


class TempCleaner(BaseScanner):

    def __init__(self):
        super().__init__()
        self.suspicious_pattern = re.compile(r'(^~.*\.tmp$|^.*\.log$)', re.IGNORECASE)

    @safe_execution
    def analyze_temp_files(self, path):
        suspicious_files = []
        print(f"Analyzing Volatile/Temp Caches inside: {path}...")

        for file_path in self.scan_directory_generator(path):
            if self.suspicious_pattern.match(os.path.basename(file_path)) is not None:
                suspicious_files.append(file_path)

        return suspicious_files