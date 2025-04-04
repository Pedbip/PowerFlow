# 🚀 PowerFlow - Electrical Project Management System  

PowerFlow is a **FastAPI-based** system for managing electrical projects, components, and users. It provides a secure authentication system, project and component management, and an **Excel export feature** for easy reporting.  

---

## ✨ Features  

### 🔒 **Authentication**  
- OAuth2 with JWT for secure authentication.  
- User registration and profile management.  
- Login and token-based access control.  

### 📂 **Project Management**  
- Create, update, delete, and retrieve projects.  
- Associate components with projects.  
- Export project data, including components, to Excel.  

### ⚙️ **Component Management**  
- Add, update, delete, and retrieve components.  
- Auto-complete missing electrical attributes (amperage, voltage, or wattage).  
- Prevent deletion of components linked to projects.  

### 📊 **Excel Export**  
- Export project data to Excel, including:  
  - **Component details** (code, brand, name, amperage, voltage, wattage).  
  - **Project summary** (total component quantity and total amperage).  

---

## ⚡ Technologies Used  

- **Python 3.11+**  
- **FastAPI** for API development  
- **SQLModel** for database interaction  
- **SQLite** (default, but can be replaced by another database)  
- **Pandas** and **OpenPyXL** for data manipulation and Excel export  
- **OAuth2 with JWT** for authentication  

---

## 🛠 Installation and Setup  

### **Prerequisites**  
- Python 3.11 or higher installed on your system.  

### **Steps**  

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/Pedbip/PowerFlow.git
   cd PowerFlow
   ```

2. **Create and activate a virtual environment:**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**  
   - Place your SQLite database file in the root directory and name it `db.db`.  
   - Alternatively, modify the database configuration in `database.py`:  
     ```python
     sqlite_file_name = "db.db"
     sqlite_url = f"sqlite:///./{sqlite_file_name}"
     ```

5. **Run the server:**  
   ```bash
   uvicorn main:app --reload
   ```

6. **Access the API documentation:**  
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)  

---

## 🔗 API Endpoints  

### 🔑 **Authentication**  
- `POST /login` → Authenticate and retrieve a JWT token.  
- `POST /user/` → Register a new user.  

### 📂 **Projects**  
- `POST /project/` → Create a new project.  
- `GET /project/` → Retrieve all projects.  
- `GET /project/{id}` → Retrieve a specific project.  
- `PATCH /project/{id}` → Update a project.  
- `DELETE /project/{id}` → Delete a project.  
- `PATCH /project/{project_id}/{component_id}` → Add a component to a project.  
- `DELETE /project/{project_id}/{component_id}` → Remove a component from a project.  
- `GET /project/export/{project_id}` → Export project data to Excel.  

### ⚙️ **Components**  
- `POST /component/` → Create a new component.  
- `GET /component/` → Retrieve all components.  
- `GET /component/{id}` → Retrieve a specific component.  
- `PATCH /component/{id}` → Update a component.  
- `DELETE /component/{id}` → Delete a component.  

### 👥 **Users**  
- `GET /user/` → Retrieve all users.  
- `GET /user/{id}` → Retrieve a specific user.  
- `PATCH /user/{id}` → Update a user.  
- `DELETE /user/{id}` → Delete a user.  
- `GET /user/projects` → Retrieve all projects associated with the current user.  
- `GET /user/component` → Retrieve all components associated with the current user.  

---

## 📊 Excel Export Example  

The `/project/export/{project_id}` endpoint generates an **Excel file** with the following structure:  

| Code   | Brand  | Name        | Amperage Rating | Voltage | Watts | Quantity | Total Amperage |
|--------|--------|------------|----------------|---------|-------|----------|---------------|
| COMP001 | Brand A | Component A | 10 | 220 | 2200 | 2 | 20 |
| COMP002 | Brand B | Component B | 5 | 110 | 550 | 1 | 5 |
| **TOTAL** |  |  |  |  |  | **3** | **25** |

---

## 💡 Contribution Guidelines  

1. Fork the repository.  
2. Create a new branch for your feature:  
   ```bash
   git checkout -b my-feature
   ```
3. Commit your changes:  
   ```bash
   git commit -m "Add new functionality"
   ```
4. Push to your branch:  
   ```bash
   git push origin my-feature
   ```
5. Open a pull request.  

---

## 📜 License  

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.  
