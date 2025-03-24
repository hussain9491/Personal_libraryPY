This is the personal library management project04 
Explain full code 

python
Copy
import streamlit as st
import pandas as pd
import os
streamlit: App banane ka framework

pandas: Data ko table ki form mein manage karne ke liye

os: File system check karne ke liye

2. Data File Setup:

python
Copy
DATA_FILE = "library.csv"
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Title","Author","Pages","Genre","Read Status"])
    df.to_csv(DATA_FILE, index=False)
Agar "library.csv" file nahi hai tou yeh ek nayi CSV file create karega khali columns ke saath

3. Data Load/Save Functions:

python
Copy
def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)
load_data(): CSV se data pandas dataframe mein load karta hai

save_data(): Updated dataframe ko wapas CSV mein save karta hai

4. Main App Structure:

python
Copy
def main():
    st.title("📚 Personal Library Manager")
    operation = st.sidebar.selectbox("Choose Operation", ["Add Book", "View Library", "Edit Book", "Delete Book"])
Sidebar mein 4 options show hoti hain: Naya book add karna, library dekhna, edit karna ya delete karna

5. Add Book Section:

python
Copy
with st.form("add_form"):
    title = st.text_input("Title")
    author = st.text_input("Author")
    pages = st.number_input("Number of Pages", min_value=1)
    genre = st.selectbox("Genre", ["Fiction","Non-Fiction",...])
    read_status = st.selectbox("Reading Status", ["Not Started","Reading","Completed"])
    
    if st.form_submit_button("Add Book"):
        new_book = pd.DataFrame([[title, author,...]])
        df = pd.concat([df, new_book])
        save_data(df)
Form se user input leta hai

Submit hone par nayi entry CSV file mein add ho jati hai

6. View Library Section:

python
Copy
search_term = st.text_input("Search...")
df = df[df.apply(lambda row: any(search_term.lower() in str(row[col]).lower()...)]
Search bar se keyword search karta hai (title, author ya genre mein)

python
Copy
st.metric("Total Books", len(df))
st.metric("Most Common Genre", df["Genre"].mode()[0])
st.metric("Average Pages", df['Pages'].mean())
Library ke statistics show karta hai (total books, sabse common genre, average pages)

7. Edit Book Section:

python
Copy
book_to_edit = st.selectbox("Select Book", df["Title"])
book_index = df[df["Title"] == book_to_edit].index[0]
book_data = df.loc[book_index]
Dropdown se book select karta hai

Purana data form mein pre-fill karta hai

Changes save hone par CSV update hoti hai

8. Delete Book Section:

python
Copy
book_to_delete = st.selectbox("Select Book", df["Title"])
df = df[df["Title"] != book_to_delete]
save_data(df)
Selected book ko CSV se remove karta hai

9. How to Run:

python
Copy
if __name__ == "__main__":
    main()
Yeh last line app ko run karne mein help karti hai

Key Features:

1/Har bar app run karte waqt CSV check hoti hai

2/ Data hamesha CSV mein save rehta hai

3/ Search aur statistics real-time update hote hain

4/ CRUD operations (Create, Read, Update, Delete) sab available hain
