"""
Name: Latice Jordan
Date: August 9, 2026
Assignment: MongoDB CRUD Application
Purpose: This program performs CRUD operations on the Amazon
         ReviewData collection using the PyMongo library.
"""

# Import the PyMongo library.
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Import re so user-entered search words can be safely
# used with MongoDB regular expression searches.
import re


# =========================================================
# CONNECT TO MONGODB
# =========================================================

print("Connecting to local Mongo database...")

# Connect to the local MongoDB server.
client = MongoClient("mongodb://localhost:27017/")

# Select the Amazon database.
db = client["Amazon"]

# Select the ReviewData collection.
collection = db["ReviewData"]

print("Connected successfully!")


# =========================================================
# DISPLAY DOCUMENTS
# =========================================================

def display_documents(documents):
    """
    Display documents returned by a MongoDB query.
    """

    documents = list(documents)

    if len(documents) == 0:
        print("No documents found.")
        return

    print()

    for document in documents:
        print(document)


# =========================================================
# QUERY DOCUMENTS
# =========================================================

def query_documents():
    """
    Allows the user to query documents from the ReviewData
    collection using find_one() and find().
    """

    while True:

        print()
        print("Please type in a number and press enter to execute the menu option")
        print("1. Query by reviewID")
        print("2. Filter for a number of stars and greater")
        print("3. Filter for less than a number of stars")
        print("4. Filter for a word in the title")
        print("5. Filter for a word in the review body content")
        print("6. Return to main menu")

        choice = input().strip()

        # -------------------------------------------------
        # Query by ReviewID using find_one()
        # -------------------------------------------------

        if choice == "1":

            review_id = input(
                "\nSearch for the ReviewID: "
            ).strip()

            try:

                # Use find_one() to retrieve one document.
                document = collection.find_one(
                    {"review_id": review_id}
                )

                if document:
                    print(document)
                else:
                    print("No document found.")

            except PyMongoError as error:

                print("Database error:", error)

        # -------------------------------------------------
        # Stars greater than or equal to a value
        # -------------------------------------------------

        elif choice == "2":

            try:

                stars = int(
                    input(
                        "\nEnter the number of stars and greater: "
                    )
                )

                # $gte means greater than or equal to.
                query = {
                    "stars": {
                        "$gte": stars
                    }
                }

                # Use find() to retrieve matching documents.
                results = collection.find(query)

                display_documents(results)

            except ValueError:

                print("Please enter a valid number.")

            except PyMongoError as error:

                print("Database error:", error)

        # -------------------------------------------------
        # Stars less than a value
        # -------------------------------------------------

        elif choice == "3":

            try:

                stars = int(
                    input(
                        "\nEnter the number of stars: "
                    )
                )

                # $lt means less than.
                query = {
                    "stars": {
                        "$lt": stars
                    }
                }

                # Use find() to retrieve matching documents.
                results = collection.find(query)

                display_documents(results)

            except ValueError:

                print("Please enter a valid number.")

            except PyMongoError as error:

                print("Database error:", error)

        # -------------------------------------------------
        # Search for a word in the review title
        # -------------------------------------------------

        elif choice == "4":

            word = input(
                "\nSearch the title for: "
            ).strip()

            try:

                # Escape special characters in the search term.
                search_word = re.escape(word)

                # Search anywhere within review_title.
                # The i option makes the search case-insensitive.
                query = {
                    "review_title": {
                        "$regex": search_word,
                        "$options": "i"
                    }
                }

                results = collection.find(query)

                display_documents(results)

            except PyMongoError as error:

                print("Database error:", error)

        # -------------------------------------------------
        # Search for a word in the review body
        # -------------------------------------------------

        elif choice == "5":

            word = input(
                "\nSearch the review body for: "
            ).strip()

            try:

                # Escape special characters in the search term.
                search_word = re.escape(word)

                # Search anywhere within review_body.
                # The i option makes the search case-insensitive.
                query = {
                    "review_body": {
                        "$regex": search_word,
                        "$options": "i"
                    }
                }

                results = collection.find(query)

                display_documents(results)

            except PyMongoError as error:

                print("Database error:", error)

        # -------------------------------------------------
        # Return to main menu
        # -------------------------------------------------

        elif choice == "6":

            break

        else:

            print("Invalid menu option. Please try again.")


# =========================================================
# CREATE DOCUMENT
# =========================================================

def add_document():
    """
    Create a new review document in the ReviewData collection.
    """

    print()
    print("Add a new document")

    # Get all required fields from the user.
    review_id = input(
        "Enter the ReviewID: "
    ).strip()

    product_id = input(
        "Enter the ProductID: "
    ).strip()

    reviewer_id = input(
        "Enter the ReviewerID: "
    ).strip()

    # Get the number of stars.
    try:

        stars = int(
            input(
                "Enter the number of stars: "
            )
        )

    except ValueError:

        print("Stars must be entered as a number.")
        return

    review_body = input(
        "Enter the review body: "
    ).strip()

    review_title = input(
        "Enter the review title: "
    ).strip()

    language = input(
        "Enter the language: "
    ).strip()

    product_category = input(
        "Enter the product category: "
    ).strip()

    # Create the new MongoDB document.
    new_document = {
        "review_id": review_id,
        "product_id": product_id,
        "reviewer_id": reviewer_id,
        "stars": stars,
        "review_body": review_body,
        "review_title": review_title,
        "language": language,
        "product_category": product_category
    }

    try:

        # Insert the new document.
        result = collection.insert_one(new_document)

        print()
        print("New document has been added:")
        print(new_document)

        print()
        print("MongoDB document ID:")
        print(result.inserted_id)

    except PyMongoError as error:

        print("Database error:", error)


# =========================================================
# UPDATE DOCUMENT
# =========================================================

def update_document():
    """
    Allow the user to update a field within an existing document.
    """

    print()
    print("Update fields of a document")

    # Ask which document should be updated.
    review_id = input(
        "What is the ReviewID you wish to update? "
    ).strip()

    try:

        # Find the document before attempting to update it.
        document = collection.find_one(
            {"review_id": review_id}
        )

        if document is None:

            print(
                "No document was found with that ReviewID."
            )

            return

        print()
        print("Which field would you like to update?")
        print()
        print("review_id")
        print("product_id")
        print("reviewer_id")
        print("stars")
        print("review_body")
        print("review_title")
        print("language")
        print("product_category")

        # Ask which field to change.
        field = input(
            "\nEnter the field name: "
        ).strip()

        # List of fields the user is allowed to update.
        allowed_fields = [
            "review_id",
            "product_id",
            "reviewer_id",
            "stars",
            "review_body",
            "review_title",
            "language",
            "product_category"
        ]

        # Check whether the field is valid.
        if field not in allowed_fields:

            print("That is not a valid field.")
            return

        # Ask the user for the new value.
        new_value = input(
            "What would you like to change the value to? "
        ).strip()

        # Stars should be stored as an integer.
        if field == "stars":

            try:

                new_value = int(new_value)

            except ValueError:

                print(
                    "Stars must be entered as a number."
                )

                return

        # Update the selected field.
        result = collection.update_one(
            {"review_id": review_id},
            {
                "$set": {
                    field: new_value
                }
            }
        )

        if result.modified_count > 0:

            print()
            print("New document has been updated to:")

            # If ReviewID itself was changed, search using
            # the new ReviewID.
            if field == "review_id":

                updated_document = collection.find_one(
                    {"review_id": new_value}
                )

            else:

                updated_document = collection.find_one(
                    {"review_id": review_id}
                )

            print(updated_document)

        else:

            print()
            print(
                "The document was found, but no changes were made."
            )

    except PyMongoError as error:

        print("Database error:", error)


# =========================================================
# DELETE ONE DOCUMENT
# =========================================================

def delete_document():
    """
    Delete one specific document from the ReviewData collection.
    """

    print()
    print("Delete a document")

    # Ask for the ReviewID.
    review_id = input(
        "What is the ReviewID you wish to delete? "
    ).strip()

    try:

        # Delete the document matching the ReviewID.
        result = collection.delete_one(
            {"review_id": review_id}
        )

        if result.deleted_count > 0:

            print(
                "Document has been deleted."
            )

        else:

            print(
                "No document was found with that ReviewID."
            )

    except PyMongoError as error:

        print("Database error:", error)


# =========================================================
# DELETE ALL DOCUMENTS
# =========================================================

def delete_all_documents():
    """
    Delete all documents from the ReviewData collection.
    """

    print()
    print("Delete all documents from the collection")

    confirmation = input(
        "Are you sure you want to delete all documents? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":

        print("Operation cancelled.")
        return

    try:

        # An empty filter matches every document.
        result = collection.delete_many({})

        print()
        print(
            result.deleted_count,
            "document(s) have been deleted."
        )

    except PyMongoError as error:

        print("Database error:", error)


# =========================================================
# DELETE COLLECTION
# =========================================================

def delete_collection():
    """
    Delete the ReviewData collection from the Amazon database.
    """

    print()
    print("Delete a collection")

    confirmation = input(
        "Are you sure you want to delete the ReviewData "
        "collection? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":

        print("Operation cancelled.")
        return

    try:

        # Drop the entire collection.
        collection.drop()

        print()
        print(
            "The ReviewData collection has been deleted."
        )

    except PyMongoError as error:

        print("Database error:", error)


# =========================================================
# MAIN MENU
# =========================================================

def main():
    """
    Display the main menu and allow the user to select
    a MongoDB operation.
    """

    while True:

        print()
        print(
            "Please type in a number and press enter "
            "to execute the menu option"
        )

        print("1. Query for documents")
        print("2. Add a new document")
        print("3. Update fields of a document")
        print("4. Delete a document")
        print("5. Delete all documents from the collection")
        print("6. Delete a collection")
        print("7. Exit the program")

        choice = input().strip()

        # Query documents.
        if choice == "1":

            query_documents()

        # Create a document.
        elif choice == "2":

            add_document()

        # Update a document.
        elif choice == "3":

            update_document()

        # Delete one document.
        elif choice == "4":

            delete_document()

        # Delete all documents.
        elif choice == "5":

            delete_all_documents()

        # Delete the collection.
        elif choice == "6":

            delete_collection()

        # Exit.
        elif choice == "7":

            print()
            print("Exit the program.")
            break

        else:

            print(
                "Invalid menu option. Please try again."
            )


# =========================================================
# START PROGRAM
# =========================================================

if __name__ == "__main__":

    try:

        # Run the application.
        main()

    except PyMongoError as error:

        print()
        print("MongoDB error:")
        print(error)

    finally:

        # Close the MongoDB connection when the program ends.
        client.close()
