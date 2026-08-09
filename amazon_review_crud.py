"""
Name: Latice Jordan
Date: August 9, 2026
Assignment: MongoDB CRUD Application
Purpose: This program demonstrates CRUD operations on the Amazon ReviewData
         MongoDB collection using the PyMongo library.
"""

from pymongo import MongoClient
from pymongo.errors import PyMongoError


# Connect to the local MongoDB server and select the database/collection.
client = MongoClient("mongodb://localhost:27017/")
db = client["Amazon"]
collection = db["ReviewData"]


def create_document():
    """Create a new review document."""
    print("\n--- Create New Review ---")

    document = {
        "review_id": input("Enter review_id: ").strip(),
        "product_id": input("Enter product_id: ").strip(),
        "reviewer_id": input("Enter reviewer_id: ").strip(),
        "stars": int(input("Enter stars (1-5): ").strip()),
        "review_body": input("Enter review_body: ").strip(),
        "review_title": input("Enter review_title: ").strip(),
        "language": input("Enter language: ").strip(),
        "product_category": input("Enter product_category: ").strip()
    }

    result = collection.insert_one(document)
    print(f"Document created successfully. ID: {result.inserted_id}")


def find_one_document():
    """Retrieve one document using find_one()."""
    print("\n--- Find One Review ---")
    review_id = input("Enter review_id to find: ").strip()

    document = collection.find_one({"review_id": review_id})

    if document:
        print("\nDocument found:")
        print(document)
    else:
        print("No document was found with that review_id.")


def find_documents():
    """Retrieve documents using find() with advanced query options."""
    while True:
        print("\n--- Find Reviews ---")
        print("1. Stars greater than or equal to")
        print("2. Stars less than")
        print("3. Word within review_title")
        print("4. Word within review_body")
        print("5. Return to main menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            try:
                stars = int(input("Enter minimum number of stars: ").strip())
                query = {"stars": {"$gte": stars}}
                display_results(collection.find(query))
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "2":
            try:
                stars = int(input("Enter maximum number of stars (exclusive): ").strip())
                query = {"stars": {"$lt": stars}}
                display_results(collection.find(query))
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "3":
            word = input("Enter a word to search for in review_title: ").strip()
            query = {"review_title": {"$regex": word, "$options": "i"}}
            display_results(collection.find(query))

        elif choice == "4":
            word = input("Enter a word to search for in review_body: ").strip()
            query = {"review_body": {"$regex": word, "$options": "i"}}
            display_results(collection.find(query))

        elif choice == "5":
            break

        else:
            print("Invalid selection. Please try again.")


def display_results(results):
    """Display documents returned by a find() query."""
    documents = list(results)

    if not documents:
        print("No matching documents were found.")
        return

    print(f"\nFound {len(documents)} document(s):")
    for document in documents:
        print(document)


def update_document():
    """Allow the user to select a document field and update its value."""
    print("\n--- Update Review ---")
    review_id = input("Enter review_id of the document to update: ").strip()

    document = collection.find_one({"review_id": review_id})

    if not document:
        print("No document was found with that review_id.")
        return

    print("\nAvailable fields:")
    print("review_id, product_id, reviewer_id, stars, review_body,")
    print("review_title, language, product_category")

    field = input("Enter the field you want to update: ").strip()

    allowed_fields = {
        "review_id",
        "product_id",
        "reviewer_id",
        "stars",
        "review_body",
        "review_title",
        "language",
        "product_category"
    }

    if field not in allowed_fields:
        print("Invalid field.")
        return

    new_value = input(f"Enter the new value for {field}: ").strip()

    if field == "stars":
        try:
            new_value = int(new_value)
        except ValueError:
            print("Stars must be a number.")
            return

    result = collection.update_one(
        {"review_id": review_id},
        {"$set": {field: new_value}}
    )

    if result.modified_count > 0:
        print("Document updated successfully.")
    else:
        print("No changes were made.")


def delete_document():
    """Delete a specific document from the collection."""
    print("\n--- Delete Review ---")
    review_id = input("Enter review_id of the document to delete: ").strip()

    result = collection.delete_one({"review_id": review_id})

    if result.deleted_count > 0:
        print("Document deleted successfully.")
    else:
        print("No document was found with that review_id.")


def delete_all_documents():
    """Delete all documents from the ReviewData collection."""
    print("\n--- Delete All Documents ---")
    confirmation = input(
        "Are you sure you want to delete ALL documents? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        result = collection.delete_many({})
        print(f"{result.deleted_count} document(s) deleted.")
    else:
        print("Operation cancelled.")


def delete_collection():
    """Delete the ReviewData collection from the Amazon database."""
    print("\n--- Delete Collection ---")
    confirmation = input(
        "Are you sure you want to delete the ReviewData collection? (yes/no): "
    ).strip().lower()

    if confirmation == "yes":
        collection.drop()
        print("ReviewData collection deleted.")
    else:
        print("Operation cancelled.")


def main():
    """Display the menu and run the selected CRUD operation."""
    while True:
        print("\n" + "=" * 50)
        print("Amazon ReviewData - MongoDB CRUD Application")
        print("=" * 50)
        print("1. Create a new review")
        print("2. Find one review")
        print("3. Find reviews with advanced queries")
        print("4. Update a review")
        print("5. Delete a specific review")
        print("6. Delete all documents")
        print("7. Delete ReviewData collection")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                create_document()
            elif choice == "2":
                find_one_document()
            elif choice == "3":
                find_documents()
            elif choice == "4":
                update_document()
            elif choice == "5":
                delete_document()
            elif choice == "6":
                delete_all_documents()
            elif choice == "7":
                delete_collection()
            elif choice == "8":
                print("Exiting program.")
                break
            else:
                print("Invalid selection. Please choose 1-8.")

        except PyMongoError as error:
            print(f"MongoDB error: {error}")
        except ValueError:
            print("Invalid numeric value entered.")


if __name__ == "__main__":
    try:
        main()
    finally:
        client.close()
