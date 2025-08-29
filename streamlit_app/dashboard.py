import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.markdown(
    """
    <h1 style="text-align: center; color: #4CAF50; margin-bottom: 10px;">
        📊 MCP Mongo Multi-DB CRUD Dashboard
    </h1>
    <p style="text-align: center; font-size: 18px; ">
        Manage multiple <b>MongoDB databases</b> seamlessly using <b>MCP</b>.  
        Perform <span style=""><b>CRUD operations</b></span> with ease and 
        expose data via <b>FastAPI</b>.  
    </p>
    <hr style="margin-top:20px; margin-bottom:20px;">
    """,
    unsafe_allow_html=True
)

db_list = []
try:
    res = requests.get(f"{API_URL}/databases")
    if res.status_code == 200:
        db_list = res.json()
except Exception as e:
    st.error(f"Could not fetch databases: {e}")

if "selected_db" not in st.session_state:
    st.session_state.selected_db = None
if "menu" not in st.session_state:
    st.session_state.menu = None

with st.sidebar.form("sidebar_form"):
    selected_db = st.selectbox(
        "Select Database",
        ["-- Select Database --"] + db_list,
        index=0
    )
    menu = st.selectbox(
        "Select Action",
        ["-- Select Action --", "Create User", "List Users", "Update User", "Delete User"],
        index=0
    )
    sidebar_submitted = st.form_submit_button("Apply")

if st.sidebar.button("Clear Page"):
    st.session_state.selected_db = None
    st.session_state.menu = None
    st.rerun()

if sidebar_submitted:
    if selected_db != "-- Select Database --":
        st.session_state.selected_db = selected_db
    else:
        st.session_state.selected_db = None
    if menu != "-- Select Action --":
        st.session_state.menu = menu
    else:
        st.session_state.menu = None

selected_db = st.session_state.selected_db
menu = st.session_state.menu

def api_url(endpoint: str, **params):
    params_str = "&".join([f"{k}={v}" for k, v in params.items()])
    return f"{API_URL}{endpoint}?{params_str}"

if not selected_db or not menu:
    st.markdown(
        """
        <div style="text-align:center; margin-top:40px;">            
            <h2 style="font-size:32px; color:#666;">
                Please select a <b>Database</b> and an <b>Action</b>  
                from the sidebar to begin managing your data.
            </h2>
        </div>
        """,
        unsafe_allow_html=True
    )
else:

    if menu == "Create User" and selected_db:
        st.header("➕ Create User")
        with st.form("create_user_form"):
            user_id = st.text_input("User ID (optional)")
            name = st.text_input("Name")
            email = st.text_input("Email")
            age = st.number_input("Age", min_value=0, step=1)
            submitted = st.form_submit_button("Add User")
        if submitted:
            payload = {"name": name, "email": email, "age": age}
            if user_id.strip():
                payload["id"] = user_id.strip()
            response = requests.post(api_url("/users", db_name=selected_db), json=payload)
            if response.status_code == 200:
                st.success(f"✅ User added! ID: {response.json().get('id')}")
            else:
                st.error(f"❌ Failed to add user: {response.text}")

    elif menu == "List Users" and selected_db:
        st.header("📋 User List")
        response = requests.get(api_url("/users", db_name=selected_db))
        if response.status_code == 200:
            users = response.json()
            if users:
                for user in users:
                    st.json(user)
            else:
                st.info("No users found")
        else:
            st.error(f"❌ Failed to fetch users: {response.text}")

    elif menu == "Update User" and selected_db:
        st.header("✏️ Update User")
        with st.form("update_user_form"):
            user_id = st.text_input("Enter User ID to update")
            name = st.text_input("New Name")
            email = st.text_input("New Email")
            age = st.number_input("New Age", min_value=0, step=1)
            submitted = st.form_submit_button("Update User")
        if submitted and user_id:
            response = requests.put(
                api_url(f"/users/{user_id}", db_name=selected_db),
                json={"name": name, "email": email, "age": age}
            )
            if response.status_code == 200:
                st.success("✅ User updated successfully")
                st.json(response.json())
            else:
                st.error(f"❌ Failed to update user: {response.text}")

    elif menu == "Delete User" and selected_db:
        st.header("🗑️ Delete User")
        with st.form("delete_user_form"):
            user_id = st.text_input("Enter User ID to delete")
            submitted = st.form_submit_button("Delete User")
        if submitted and user_id:
            response = requests.delete(api_url(f"/users/{user_id}", db_name=selected_db))
            if response.status_code == 200:
                st.success("✅ User deleted successfully")
            else:
                st.error(f"❌ Failed to delete user: {response.text}")
