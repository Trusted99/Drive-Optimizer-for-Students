
from collections import defaultdict


def analyze_files(found_files):

    statistics = defaultdict(lambda: {
        "count": 0,
        "size": 0
    })

    for file in found_files:

        category = file["category"]

        statistics[category]["count"] += 1
        statistics[category]["size"] += file["size"]

    print("\n========== STORAGE ANALYSIS ==========")

    total_files = 0
    total_size = 0

    for category, data in statistics.items():

        size_mb = data["size"] / (1024 * 1024)

        print(f"\nCategory: {category}")
        print(f"Files found: {data['count']}")
        print(f"Storage occupied: {size_mb:.2f} MB")

        total_files += data["count"]
        total_size += data["size"]

    print("\n========== OVERALL SUMMARY ==========")

    print(f"Total files: {total_files}")
    print(f"Total storage: {total_size / (1024**3):.2f} GB")

    # Identify the 20 largest files
    largest_files = sorted(
        found_files,
        key=lambda item: item["size"],
        reverse=True
    )[:20]

    print("\n========== 20 LARGEST FILES ==========")

    for index, file in enumerate(largest_files, start=1):

        size_mb = file["size"] / (1024 * 1024)

        print(
            f"{index}. {file['name']} "
            f"({size_mb:.2f} MB)"
        )

    return statistics
