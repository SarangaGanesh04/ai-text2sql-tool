from dotenv import load_dotenv
import os
import streamlit as st
import google.generativeai as genai
import sqlite3
import pandas as pd
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Model and Generate Response
def get_response(question, prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([prompt, question])
    return response.text

# Create database from description
def create_database_from_description(description):
    create_prompt = """
    You are an expert database designer. Given a description of what the user wants to track, create a SQL CREATE TABLE statement.
    
    Rules:
    1. Use appropriate data types (TEXT, INTEGER, REAL, DATE, etc.)
    2. Make column names clear and descriptive
    3. Use UPPERCASE for SQL keywords
    4. Return ONLY the SQL statement, no explanations
    5. Use a descriptive table name based on the content (e.g., BASKETBALL_PLAYERS, STUDENTS, EXPENSES)
    6. Include an ID column as INTEGER PRIMARY KEY
    7. Use consistent naming: NAME for names, POINTS for points, etc.
    
    Examples:
    - "basketball players with points, assists, rebounds": 
      CREATE TABLE BASKETBALL_PLAYERS (ID INTEGER PRIMARY KEY, NAME TEXT, POINTS REAL, ASSISTS REAL, REBOUNDS REAL);
    
    - "students with grades": 
      CREATE TABLE STUDENTS (ID INTEGER PRIMARY KEY, NAME TEXT, CLASS TEXT, GRADE REAL);
    
    - "expenses with date, category, amount": 
      CREATE TABLE EXPENSES (ID INTEGER PRIMARY KEY, DATE TEXT, CATEGORY TEXT, AMOUNT REAL);
    """
    
    try:
        sql_statement = get_response(description, create_prompt)
        # Clean up the response
        sql_statement = sql_statement.strip()
        if sql_statement.startswith("```sql"):
            sql_statement = sql_statement[6:]
        if sql_statement.endswith("```"):
            sql_statement = sql_statement[:-3]
        sql_statement = sql_statement.strip()
        
        return sql_statement
    except Exception as e:
        st.error(f"Error creating database: {str(e)}")
        return None

# Execute SQL query
def execute_sql(sql, db_path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(sql)
        
        # Check if it's a SELECT query
        if sql.strip().upper().startswith('SELECT'):
            data = cur.fetchall()
            conn.close()
            return data, None
        else:
            # For INSERT, UPDATE, DELETE, CREATE
            conn.commit()
            conn.close()
            return None, f"Query executed successfully: {sql}"
    except Exception as e:
        return None, f"Database error: {str(e)}"

# Get table schema
def get_table_schema(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()
        
        schema_info = {}
        for table in tables:
            table_name = table[0]
            cur.execute(f"PRAGMA table_info({table_name});")
            columns = cur.fetchall()
            schema_info[table_name] = columns
        
        conn.close()
        return schema_info
    except Exception as e:
        return {}

# Generate SQL for natural language queries
def generate_query_sql(question, schema_info):
    # Create a description of the database structure
    schema_description = "Database structure:\n"
    for table_name, columns in schema_info.items():
        schema_description += f"Table: {table_name}\n"
        for col in columns:
            schema_description += f"  - {col[1]} ({col[2]})\n"
    
    # Get the actual column names for INSERT statements
    table_name = list(schema_info.keys())[0]
    column_names = [col[1] for col in schema_info[table_name] if col[1] != 'ID']  # Exclude ID column
    
    query_prompt = f"""
    {schema_description}
    
    You are an expert in converting natural language questions into SQL queries.
    Return ONLY the SQL statement, no explanations.
    
    IMPORTANT: 
    - Use the exact table name: {table_name}
    - For INSERT statements, use these exact column names: {', '.join(column_names)}
    - Do NOT include the ID column in INSERT statements (it's auto-generated)
    
    Examples:
    - "Show all players": SELECT * FROM {table_name};
    - "Add a player named John with 20 points, 5 assists, 3 rebounds": INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ('John', 20, 5, 3);
    - "Update John's points to 25": UPDATE {table_name} SET POINTS = 25 WHERE NAME = 'John';
    - "Delete player John": DELETE FROM {table_name} WHERE NAME = 'John';
    - "Show all data": SELECT * FROM {table_name};
    - "Display everything": SELECT * FROM {table_name};
    """
    
    try:
        sql = get_response(question, query_prompt)
        # Clean up the response
        sql = sql.strip()
        if sql.startswith("```sql"):
            sql = sql[6:]
        if sql.endswith("```"):
            sql = sql[:-3]
        sql = sql.strip()
        
        return sql
    except Exception as e:
        st.error(f"Error generating query: {str(e)}")
        return None

# Streamlit app
st.set_page_config(page_title="AI Database Creator & Query Tool", page_icon="🗄️", layout="wide")

st.title("🗄️ AI Database Creator & Query Tool")
st.markdown("Create databases by describing what you want to track, then query them using natural language!")

# Sidebar for database management
with st.sidebar:
    st.header("Database Management")
    
    # Database creation
    st.subheader("Create New Database")
    db_description = st.text_area(
        "Describe what you want to track:",
        placeholder="e.g., I want to track basketball players with their points, assists, and rebounds averages",
        height=100
    )
    
    if st.button("Create Database"):
        if db_description:
            with st.spinner("Creating database..."):
                sql_statement = create_database_from_description(db_description)
                if sql_statement:
                    st.success("Database created!")
                    st.code(sql_statement, language="sql")
                    
                    # Execute the CREATE statement
                    result, error = execute_sql(sql_statement, "dynamic.db")
                    if error:
                        st.error(error)
                    else:
                        st.success("Database structure created successfully!")
                        
                        # Show the new schema
                        schema = get_table_schema("dynamic.db")
                        st.subheader("Database Schema:")
                        for table_name, columns in schema.items():
                            st.write(f"**Table: {table_name}**")
                            for col in columns:
                                st.write(f"  - {col[1]} ({col[2]})")
        else:
            st.warning("Please describe what you want to track.")

# Main area for querying
st.header("Query Your Database")

# Check if database exists and show current schema
schema_info = get_table_schema("dynamic.db")
if schema_info:
    st.subheader("Current Database Schema:")
    for table_name, columns in schema_info.items():
        with st.expander(f"Table: {table_name}"):
            df_schema = pd.DataFrame(columns, columns=['ID', 'Name', 'Type', 'NotNull', 'Default', 'PrimaryKey'])
            st.dataframe(df_schema, use_container_width=True)
    
    # Query interface
    st.subheader("Ask Questions or Add Data")
    query_input = st.text_input(
        "What would you like to know or do?",
        placeholder="e.g., Show all players, Add a player named LeBron with 25 points, Update LeBron's assists to 8"
    )
    
    if st.button("Execute"):
        if query_input:
            with st.spinner("Processing..."):
                # Generate SQL from natural language
                sql_query = generate_query_sql(query_input, schema_info)
                
                if sql_query:
                    st.subheader("Generated SQL:")
                    st.code(sql_query, language="sql")
                    
                    # Debug: Show what we're about to execute
                    #st.write(f"**Debug:** About to execute: `{sql_query}`")
                    
                    # Execute the query
                    data, message = execute_sql(sql_query, "dynamic.db")
                    
                    # Debug: Show what we got back
                    #st.write(f"**Debug:** Data returned: {data}")
                    #st.write(f"**Debug:** Message: {message}")
                    
                    if data is not None:
                        # Display results
                        st.subheader("Results:")
                        if len(data) > 0:
                            # Determine column names based on data structure
                            num_columns = len(data[0])
                            if num_columns == 1:
                                columns = ['Result']
                            else:
                                # Try to get column names from schema
                                table_name = list(schema_info.keys())[0]  # Assume first table
                                schema_columns = [col[1] for col in schema_info[table_name]]
                                if len(schema_columns) == num_columns:
                                    columns = schema_columns
                                else:
                                    columns = [f'Column_{i+1}' for i in range(num_columns)]
                            
                            df = pd.DataFrame(data, columns=columns)
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.info("No data found.")
                    elif message:
                        st.success(message)
                        
                        # Refresh schema display
                        st.rerun()
                else:
                    st.error("Could not generate SQL query.")
        else:
            st.warning("Please enter a question or command.")
else:
    st.info("No database found. Create one using the sidebar!")
    
    # Show example
    st.subheader("Example:")
    st.markdown("""
    **In the sidebar, try describing:**
    ```
    I want to track basketball players with their points, assists, and rebounds averages
    ```
    
    **Then you can ask questions like:**
    - "Show all players"
    - "Add a player named LeBron with 25 points, 8 assists, and 7 rebounds"
    - "Update LeBron's points to 30"
    - "Show players with more than 20 points"
    """)

# Footer
st.markdown("---")
st.markdown("**Tips:**")
st.markdown("- Use natural language to describe what you want to track")
st.markdown("- Ask questions or give commands in plain English")
st.markdown("- The AI will automatically generate the appropriate SQL")