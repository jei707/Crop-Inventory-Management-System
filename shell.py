from datetime import datetime
from enum import Enum
# Crop Inventory System with Shell Sort
crop_inventory = []

# Enums categorical sorting
CATEGORY_ORDER = ["Vegetables", "Fruits", "Fibre Crop", "Nut", "Root and Tuber", "Stimulant", "Tobacco", "Pulse", "Oil Crop"]
SEASONALITY_ORDER = ["Wet", "Dry", "Wet and Dry"]
FLAG_DESCRIPTION_ORDER = ["Organic", "Non-GMO", "Hybrid", "Heirloom"]

# Shell Sort
def shell_sort(arr, key, custom_order=None, is_date=False, is_descending=False):
    n = len(arr)
    gap = n // 2

    # Inner helper function for comparing values
    def compare(val1, val2):
        # Date comparison
        if is_date:
            val1 = datetime.strptime(val1, "%Y-%m-%d")
            val2 = datetime.strptime(val2, "%Y-%m-%d")
        # Custom order comparison
        elif custom_order:
            if val1 not in custom_order:
                val1 = float('inf')
            if val2 not in custom_order:
                val2 = float('inf')
            val1 = custom_order.index(val1)
            val2 = custom_order.index(val2)
        # Integer comparison
        elif isinstance(val1, int) and isinstance(val2, int):
            pass
        else:
            # Fallback for string comparison (e.g., Local Name)
            val1, val2 = str(val1), str(val2)
        
        # Compare based on descending order
        return (val1 < val2) if not is_descending else (val1 > val2)

    # Sorting logic with Shell Sort
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and compare(arr[j - gap][key], temp[key]):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr


# Wrapper functions for specific sorting needs
def shell_sort_local_name(arr, is_descending):
    return shell_sort(arr, "Local Name", is_descending=is_descending)

def shell_sort_category(arr, is_descending):
    return shell_sort(arr, "Category", custom_order=CATEGORY_ORDER, is_descending=is_descending)

def shell_sort_seasonality(arr, is_descending):
    return shell_sort(arr, "Seasonality", custom_order=SEASONALITY_ORDER, is_descending=is_descending)

def shell_sort_item_code(arr, is_descending):
    return shell_sort(arr, "Item Code", is_descending=is_descending)

def shell_sort_year(arr, is_descending):
    return shell_sort(arr, "Year", is_date=True, is_descending=is_descending)

def shell_sort_flag_description(arr, is_descending):
    return shell_sort(arr, "Flag Description", custom_order=FLAG_DESCRIPTION_ORDER, is_descending=is_descending)

def shell_sort_harvest_date(arr, is_descending):
    return shell_sort(arr, "Harvest Date", is_date=True, is_descending=is_descending)

def shell_sort_quantity(arr, is_descending):
    return shell_sort(arr, "Quantity", is_descending=is_descending)

# Add a new crop entry
def add_crop():
    local_name = input("Enter local name: ")

    print("Choose category:")
    for idx, category in enumerate(CATEGORY_ORDER, start=1):
        print(f"{idx}. {category}")
    category_choice = int(input("Enter category number: "))
    category = CATEGORY_ORDER[category_choice - 1] if 1 <= category_choice <= len(CATEGORY_ORDER) else "Unknown"

    print("Choose seasonality:")
    for idx, season in enumerate(SEASONALITY_ORDER, start=1):
        print(f"{idx}. {season}")
    season_choice = int(input("Enter seasonality number: "))
    seasonality = SEASONALITY_ORDER[season_choice - 1] if 1 <= season_choice <= len(SEASONALITY_ORDER) else "Unknown"

    print("Choose flag description:")
    for idx, flag in enumerate(FLAG_DESCRIPTION_ORDER, start=1):
        print(f"{idx}. {flag}")
    flag_choice = int(input("Enter flag description number: "))
    flag_description = FLAG_DESCRIPTION_ORDER[flag_choice - 1] if 1 <= flag_choice <= len(FLAG_DESCRIPTION_ORDER) else "Unknown"

    crop = {
        "Local Name": local_name,
        "Category": category,
        "Seasonality": seasonality,
        "Item Code": int(input("Enter item code (integer): ")),
        "Year": input("Enter year (YYYY): "),
        "Flag Description": flag_description,
        "Harvest Date": input("Enter harvest date (YYYY-MM-DD): "),
        "Quantity": int(input("Enter quantity: "))
    }
    crop_inventory.append(crop)
    print("Crop added successfully!")

# Display all crops with sorting option
def display_crops():
    if not crop_inventory:
        print("No crops in inventory.")
        return

    print("\n--- Sort By ---")
    print("1. Local Name (Alphabetical)")
    print("2. Category (Enum Order)")
    print("3. Seasonality (Enum Order)")
    print("4. Item Code (Integer)")
    print("5. Year (Date)")
    print("6. Flag Description (Enum Order)")
    print("7. Harvest Date (Date)")
    print("8. Quantity (Integer)")

    choice = input("Choose sorting option (1-8): ")

    print("\n--- Sort Order ---")
    print("1. Ascending")
    print("2. Descending")
    order_choice = input("Choose sort order (1 for Ascending, 2 for Descending): ")

    # Determine sorting order
    is_descending = order_choice == "2"

    if choice == "1":
        sorted_crops = shell_sort_local_name(crop_inventory, is_descending)
    elif choice == "2":
        sorted_crops = shell_sort_category(crop_inventory, is_descending)
    elif choice == "3":
        sorted_crops = shell_sort_seasonality(crop_inventory, is_descending)
    elif choice == "4":
        sorted_crops = shell_sort_item_code(crop_inventory, is_descending)
    elif choice == "5":
        sorted_crops = shell_sort_year(crop_inventory, is_descending)
    elif choice == "6":
        sorted_crops = shell_sort_flag_description(crop_inventory, is_descending)
    elif choice == "7":
        sorted_crops = shell_sort_harvest_date(crop_inventory, is_descending)
    elif choice == "8":
        sorted_crops = shell_sort_quantity(crop_inventory, is_descending)
    else:
        print("Invalid choice. Displaying unsorted crops.")
        sorted_crops = crop_inventory

    for i, crop in enumerate(sorted_crops, start=1):
        print(f"\nCrop {i}:")
        for key, value in crop.items():
            print(f"{key}: {value}")

# Edit a crop entry
def edit_crop():
    display_crops()
    index = int(input("\nEnter the crop number you want to edit: ")) - 1
    if 0 <= index < len(crop_inventory):
        crop = crop_inventory[index]
        print("Enter new values (leave blank to keep current value):")
        for key in crop:
            new_value = input(f"{key} ({crop[key]}): ")
            if new_value:
                if key in ["Item Code", "Quantity"]:
                    crop[key] = int(new_value)
                elif key in ["Year", "Harvest Date"]:
                    crop[key] = new_value
                else:
                    crop[key] = new_value
        print("Crop updated successfully!")
    else:
        print("Invalid crop number.")

# Delete a crop entry
def delete_crop():
    display_crops()
    index = int(input("\nEnter the crop number you want to delete: ")) - 1
    if 0 <= index < len(crop_inventory):
        crop_inventory.pop(index)
        print("Crop deleted successfully!")
    else:
        print("Invalid crop number.")

# Main menu function
def main_menu():
    while True:
        print("\n--- Crop Inventory System ---")
        print("1. Add Crop")
        print("2. Display Crops")
        print("3. Edit Crop")
        print("4. Delete Crop")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_crop()
        elif choice == "2":
            display_crops()
        elif choice == "3":
            edit_crop()
        elif choice == "4":
            delete_crop()
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

# Main menu
if __name__ == "__main__":
    main_menu()