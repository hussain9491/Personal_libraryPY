import streamlit as st # type: ignore
import pandas as pd
import os

# File path for CSV storage
DATA_FILE = "library.csv"

# Initialize the CSV file if it doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Title", "Author", "Pages", "Genre", "Read Status"])
    df.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def main():
    st.title("📚 Personal Library Manager")

    # Sidebar operations
    st.sidebar.header("Operations")
    operation = st.sidebar.selectbox("Choose Operation", 
                                   ["Add Book", "View Library", "Edit Book", "Delete Book"])

    if operation == "Add Book":
        st.header("Add New Book")
        with st.form("add_form"):
            title = st.text_input("Title")
            author = st.text_input("Author")
            pages = st.number_input("Number of Pages", min_value=1)
            genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", 
                                         "History", "Biography", "Other"])
            read_status = st.selectbox("Reading Status", ["Not Started", "Reading", "Completed"])
            
            if st.form_submit_button("Add Book"):
                new_book = pd.DataFrame([[title, author, pages, genre, read_status]],
                                       columns=["Title", "Author", "Pages", "Genre", "Read Status"])
                df = load_data()
                df = pd.concat([df, new_book], ignore_index=True)
                save_data(df)
                st.success("Book added successfully!")

    elif operation == "View Library":
        st.header("Your Library")
        df = load_data()
        
        # Search functionality
        search_term = st.text_input("Search by Title, Author, or Genre")
        if search_term:
            df = df[df.apply(lambda row: any(search_term.lower() in str(row[col]).lower() 
                                           for col in ["Title", "Author", "Genre"]), axis=1)]
        
        # Display statistics
        st.subheader("Library Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Books", len(df))
        with col2:
            st.metric("Most Common Genre", df["Genre"].mode()[0] if not df.empty else "N/A")
        with col3:
            st.metric("Average Pages", f"{df['Pages'].mean():.0f}" if not df.empty else "N/A")
        
        # Display books
        st.subheader("Book List")
        st.dataframe(df.style.applymap(lambda x: 'background-color: #e6f3ff', 
                                     subset=pd.IndexSlice[:, []]), 
                   use_container_width=True)

    elif operation == "Edit Book":
        st.header("Edit Book Details")
        df = load_data()
        
        if df.empty:
            st.warning("No books in the library to edit!")
            return
            
        book_to_edit = st.selectbox("Select Book to Edit", df["Title"])
        book_index = df[df["Title"] == book_to_edit].index[0]
        book_data = df.loc[book_index]

        with st.form("edit_form"):
            new_title = st.text_input("Title", value=book_data["Title"])
            new_author = st.text_input("Author", value=book_data["Author"])
            new_pages = st.number_input("Pages", value=book_data["Pages"])
            new_genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", 
                                            "History", "Biography", "Other"],
                                   index=["Fiction", "Non-Fiction", "Science", 
                                        "History", "Biography", "Other"].index(book_data["Genre"]))
            new_status = st.selectbox("Reading Status", ["Not Started", "Reading", "Completed"],
                                    index=["Not Started", "Reading", "Completed"].index(book_data["Read Status"]))
            
            if st.form_submit_button("Update Book"):
                df.at[book_index, "Title"] = new_title
                df.at[book_index, "Author"] = new_author
                df.at[book_index, "Pages"] = new_pages
                df.at[book_index, "Genre"] = new_genre
                df.at[book_index, "Read Status"] = new_status
                save_data(df)
                st.success("Book updated successfully!")

    elif operation == "Delete Book":
        st.header("Delete Book")
        df = load_data()
        
        if df.empty:
            st.warning("No books in the library to delete!")
            return
            
        book_to_delete = st.selectbox("Select Book to Delete", df["Title"])
        if st.button("Delete Book"):
            df = df[df["Title"] != book_to_delete]
            save_data(df)
            st.success("Book deleted successfully!")

if __name__ == "__main__":
    main()