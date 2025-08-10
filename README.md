# 🗄️ AI Database Creator & Query Tool

A powerful Streamlit application that allows you to create databases by describing what you want to track, then query them using natural language.

## 🚀 Features

- **Natural Language Database Creation**: Describe what you want to track, and the AI creates the database structure
- **Natural Language Queries**: Ask questions or give commands in plain English
- **Automatic SQL Generation**: The AI converts your natural language to SQL
- **Interactive Interface**: Clean, user-friendly Streamlit interface
- **Real-time Results**: See your data in beautiful tables

## 🛠️ Installation

1. **Clone or download this project**
2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install streamlit python-dotenv google-generativeai pandas
   ```

4. **Set up your API key:**
   - Create a `.env` file in the project directory
   - Add your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

5. **Run the application:**
   ```bash
   streamlit run sql.py
   ```

## 📖 How to Use

### Step 1: Create a Database
1. Open the application in your browser
2. In the sidebar, describe what you want to track
3. Click "Create Database"

**Examples:**
- "I want to track basketball players with their points, assists, and rebounds averages"
- "I need a database for students with their names, classes, and grades"
- "Create a database for tracking expenses with date, category, and amount"

### Step 2: Add Data and Query
Once your database is created, you can:

**Add Data:**
- "Add a player named LeBron with 25 points, 8 assists, and 7 rebounds"
- "Insert a student named John in 10th grade with 85% grade"

**Query Data:**
- "Show all players"
- "Display students with grades above 90"
- "How many players have more than 20 points?"

**Update Data:**
- "Update LeBron's points to 30"
- "Change John's grade to 88"

**Delete Data:**
- "Delete player LeBron"
- "Remove student John"

## 🎯 Example Workflow

### Basketball Players Database

1. **Create Database:**
   ```
   "I want to track basketball players with their points, assists, and rebounds averages"
   ```

2. **Add Players:**
   ```
   "Add a player named LeBron James with 25.5 points, 8.2 assists, and 7.5 rebounds"
   "Add a player named Stephen Curry with 29.8 points, 6.3 assists, and 4.4 rebounds"
   "Add a player named Kevin Durant with 26.4 points, 5.8 assists, and 6.8 rebounds"
   ```

3. **Query Data:**
   ```
   "Show all players"
   "Display players with more than 25 points"
   "Who has the most assists?"
   "Show players sorted by points"
   ```

## 🔧 Technical Details

- **Backend**: SQLite database
- **AI**: Google Gemini 2.5 Flash
- **Frontend**: Streamlit
- **Data Processing**: Pandas

## 🎨 Customization

You can easily modify the application by:

1. **Changing the AI model** in the `get_response()` function
2. **Adding new data types** in the database creation prompt
3. **Customizing the UI** using Streamlit components
4. **Adding validation** for specific data formats

## 🐛 Troubleshooting

**Common Issues:**

1. **API Key Error**: Make sure your `.env` file contains the correct Gemini API key
2. **Database Errors**: The application creates a new `dynamic.db` file for each session
3. **SQL Generation Issues**: Try rephrasing your request more clearly

**Tips:**
- Be specific in your descriptions
- Use clear, natural language
- The AI works best with concrete examples

## 🚀 Future Enhancements

Potential improvements:
- Multiple database support
- Data import/export functionality
- Advanced query capabilities
- Data visualization
- User authentication
- Cloud database integration

## 📝 License

This project is open source and available under the MIT License.

---

**Happy Database Creating! 🎉**
