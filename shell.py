from datetime import datetime

# Crop Inventory System with Shell Sort
crop_inventory = []

# Enums categorical sorting
CATEGORY_ORDER = ["Vegetables", "Fruits", "Fibre Crop", "Nut", "Root and Tuber", "Stimulant", "Tobacco", "Pulse", "Oil Crop"]
SEASONALITY_ORDER = ["Wet", "Dry", "Wet and Dry"]
FLAG_DESCRIPTION_ORDER = ["Organic", "Non-GMO", "Hybrid", "Heirloom"]

# Shell Sort
def shell_sort(arr, key, custom_order=None, is_date=False):
    n = len(arr)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i

            while j >= gap and (
                (is_date and datetime.strptime(arr[j - gap][key], "%Y-%m-%d") > datetime.strptime(temp[key], "%Y-%m-%d")) or
                (custom_order and custom_order.index(arr[j - gap][key]) > custom_order.index(temp[key])) or
                (not is_date and not custom_order and arr[j - gap][key] > temp[key])
            ):
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

# Wrapper functions for specific sorting needs
def shell_sort_local_name(arr):
    return shell_sort(arr, "Local Name")

def shell_sort_category(arr):
    return shell_sort(arr, "Category", custom_order=CATEGORY_ORDER)

def shell_sort_seasonality(arr):
    return shell_sort(arr, "Seasonality", custom_order=SEASONALITY_ORDER)

def shell_sort_item_code(arr):
    return shell_sort(arr, "Item Code")

def shell_sort_year(arr):
    return shell_sort(arr, "Year", is_date=True)

def shell_sort_flag_description(arr):
    return shell_sort(arr, "Flag Description", custom_order=FLAG_DESCRIPTION_ORDER)

def shell_sort_harvest_date(arr):
    return shell_sort(arr, "Harvest Date", is_date=True)

def shell_sort_quantity(arr):
    return shell_sort(arr, "Quantity")

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

    if choice == "1":
        sorted_crops = shell_sort_local_name(crop_inventory)
    elif choice == "2":
        sorted_crops = shell_sort_category(crop_inventory)
    elif choice == "3":
        sorted_crops = shell_sort_seasonality(crop_inventory)
    elif choice == "4":
        sorted_crops = shell_sort_item_code(crop_inventory)
    elif choice == "5":
        sorted_crops = shell_sort_year(crop_inventory)
    elif choice == "6":
        sorted_crops = shell_sort_flag_description(crop_inventory)
    elif choice == "7":
        sorted_crops = shell_sort_harvest_date(crop_inventory)
    elif choice == "8":
        sorted_crops = shell_sort_quantity(crop_inventory)
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
