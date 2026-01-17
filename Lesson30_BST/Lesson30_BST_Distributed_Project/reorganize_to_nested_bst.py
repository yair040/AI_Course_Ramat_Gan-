#!/usr/bin/env python3
"""
Reorganize flat BST structure into proper nested hierarchy
"""
import shutil
from pathlib import Path

def reorganize_bst():
    """Create proper nested BST structure"""

    base = Path(".")
    backup = base / "temp_bst_backup"

    print("Creating nested BST structure...\n")

    # Create 5_01 (root) with its files and shared_level_4
    print("Level 1: Creating root 5_01/")
    root = base / "5_01"
    root.mkdir(exist_ok=True)

    # Copy 5_01 files
    for file in (backup / "5_01").iterdir():
        shutil.copy2(file, root / file.name)

    # Copy shared_level_5 to root level (shared by entire system)
    print("  Copying shared_level_5/ to root level")
    shutil.copytree(backup / "shared_level_5", base / "shared_level_5", dirs_exist_ok=True)

    # Copy shared_level_4 inside 5_01 (shared by 4_xx nodes)
    print("  Copying shared_level_4/ to 5_01/")
    shutil.copytree(backup / "shared_level_4", root / "shared_level_4", dirs_exist_ok=True)

    # Create 4_01 and 4_02 inside 5_01
    print("\nLevel 2: Creating 4_01/ and 4_02/ inside 5_01/")

    for node_4 in ["4_01", "4_02"]:
        node_4_path = root / node_4
        node_4_path.mkdir(exist_ok=True)

        # Copy node files
        for file in (backup / node_4).iterdir():
            shutil.copy2(file, node_4_path / file.name)

        # Copy shared_level_3 inside each 4_xx (shared by 3_xx nodes)
        print(f"  Copying shared_level_3/ to 5_01/{node_4}/")
        shutil.copytree(backup / "shared_level_3", node_4_path / "shared_level_3", dirs_exist_ok=True)

    # Create 3_01, 3_02 inside 4_01
    # Create 3_03, 3_04 inside 4_02
    print("\nLevel 3: Creating 3_xx nodes")

    level_3_mapping = {
        "4_01": ["3_01", "3_02"],
        "4_02": ["3_03", "3_04"]
    }

    for parent_4, children_3 in level_3_mapping.items():
        parent_path = root / parent_4
        for node_3 in children_3:
            node_3_path = parent_path / node_3
            node_3_path.mkdir(exist_ok=True)

            print(f"  Creating 5_01/{parent_4}/{node_3}/")

            # Copy node files
            for file in (backup / node_3).iterdir():
                shutil.copy2(file, node_3_path / file.name)

            # Copy shared_level_2 inside each 3_xx (shared by 2_xx nodes)
            shutil.copytree(backup / "shared_level_2", node_3_path / "shared_level_2", dirs_exist_ok=True)

    # Create 2_xx nodes inside 3_xx
    print("\nLevel 4: Creating 2_xx nodes")

    level_4_mapping = {
        ("4_01", "3_01"): ["2_01", "2_02"],
        ("4_01", "3_02"): ["2_03", "2_04"],
        ("4_02", "3_03"): ["2_05", "2_06"],
        ("4_02", "3_04"): ["2_07", "2_08"]
    }

    for (parent_4, parent_3), children_2 in level_4_mapping.items():
        parent_path = root / parent_4 / parent_3
        for node_2 in children_2:
            node_2_path = parent_path / node_2
            node_2_path.mkdir(exist_ok=True)

            print(f"  Creating 5_01/{parent_4}/{parent_3}/{node_2}/")

            # Copy node files
            for file in (backup / node_2).iterdir():
                shutil.copy2(file, node_2_path / file.name)

            # Copy shared_level_1 inside each 2_xx (shared by 1_xx leaf nodes)
            shutil.copytree(backup / "shared_level_1", node_2_path / "shared_level_1", dirs_exist_ok=True)

    # Create 1_xx leaf nodes inside 2_xx
    print("\nLevel 5: Creating 1_xx leaf nodes")

    level_5_mapping = {
        ("4_01", "3_01", "2_01"): ["1_01", "1_02"],
        ("4_01", "3_01", "2_02"): ["1_03", "1_04"],
        ("4_01", "3_02", "2_03"): ["1_05", "1_06"],
        ("4_01", "3_02", "2_04"): ["1_07", "1_08"],
        ("4_02", "3_03", "2_05"): ["1_09", "1_10"],
        ("4_02", "3_03", "2_06"): ["1_11", "1_12"],
        ("4_02", "3_04", "2_07"): ["1_13", "1_14"],
        ("4_02", "3_04", "2_08"): ["1_15", "1_16"]
    }

    for (parent_4, parent_3, parent_2), children_1 in level_5_mapping.items():
        parent_path = root / parent_4 / parent_3 / parent_2
        for node_1 in children_1:
            node_1_path = parent_path / node_1
            node_1_path.mkdir(exist_ok=True)

            print(f"  Creating 5_01/{parent_4}/{parent_3}/{parent_2}/{node_1}/")

            # Copy node files
            for file in (backup / node_1).iterdir():
                shutil.copy2(file, node_1_path / file.name)

    print("\n✓ Nested BST structure created successfully!")
    print("\nStructure:")
    print("5_01/                           (Root)")
    print("├── shared_level_4/")
    print("├── 4_01/                       (Left subtree - Analysis)")
    print("│   ├── shared_level_3/")
    print("│   ├── 3_01/")
    print("│   │   ├── shared_level_2/")
    print("│   │   ├── 2_01/")
    print("│   │   │   ├── shared_level_1/")
    print("│   │   │   ├── 1_01/           (Leaf)")
    print("│   │   │   └── 1_02/           (Leaf)")
    print("│   │   └── 2_02/")
    print("│   │       ├── shared_level_1/")
    print("│   │       ├── 1_03/           (Leaf)")
    print("│   │       └── 1_04/           (Leaf)")
    print("│   └── 3_02/")
    print("│       ├── shared_level_2/")
    print("│       ├── 2_03/")
    print("│       │   ├── shared_level_1/")
    print("│       │   ├── 1_05/           (Leaf)")
    print("│       │   └── 1_06/           (Leaf)")
    print("│       └── 2_04/")
    print("│           ├── shared_level_1/")
    print("│           ├── 1_07/           (Leaf)")
    print("│           └── 1_08/           (Leaf)")
    print("└── 4_02/                       (Right subtree - Infrastructure)")
    print("    ├── shared_level_3/")
    print("    ├── 3_03/")
    print("    │   ├── shared_level_2/")
    print("    │   ├── 2_05/")
    print("    │   │   ├── shared_level_1/")
    print("    │   │   ├── 1_09/           (Leaf)")
    print("    │   │   └── 1_10/           (Leaf)")
    print("    │   └── 2_06/")
    print("    │       ├── shared_level_1/")
    print("    │       ├── 1_11/           (Leaf)")
    print("    │       └── 1_12/           (Leaf)")
    print("    └── 3_04/")
    print("        ├── shared_level_2/")
    print("        ├── 2_07/")
    print("        │   ├── shared_level_1/")
    print("        │   ├── 1_13/           (Leaf)")
    print("        │   └── 1_14/           (Leaf)")
    print("        └── 2_08/")
    print("            ├── shared_level_1/")
    print("            ├── 1_15/           (Leaf)")
    print("            └── 1_16/           (Leaf)")

if __name__ == "__main__":
    reorganize_bst()
