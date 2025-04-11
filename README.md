# Linkedin Search Scraper App

This application allows you to search for profiles on LinkedIn based on specific keywords and automatically export the collected profile information into an Excel file.

![Linkedin_Scraper](https://github.com/user-attachments/assets/3e1c72c6-466f-4a90-a467-ab92c8857e85)

## Installation

1. Install Git and clone the repository:
   ```bash
   git clone https://github.com/username/Linkedin_Search_Scraper_App.git
   cd Linkedin_Search_Scraper_App
   ```
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv myenv
   # For Windows
   .\myenv\Scripts\activate
   # For Linux/Mac
   source myenv/bin/activate
   ```
3. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Install Firefox browser and Geckodriver:
   - Geckodriver is required for Selenium to manage Firefox automatically.

## Usage

### Using the GUI

1. Launch the application:
   ```bash
   python gui.py
   ```
2. Enter your LinkedIn account details:
   - Your email and password will be saved in the .env file.
   - Cookies will be automatically saved for subsequent logins.

3. To search:
   - Enter the search keyword.
   - Specify the number of profiles to collect.
   - Click the "Search" button.

4. The results will automatically be saved as an Excel file in the "exports" folder.

### Using Command Line (main.py)

1. Run the application from the command line:
   ```bash
   python main.py "search term" number_of_profiles
   ```
   Example:
   ```bash
   python main.py "Data Scientist" 50
   ```

## Technical Details

### Project Structure

- `gui.py`: Graphical user interface
- `main.py`: Core application logic
- `login.py`: LinkedIn session management
- `linkedin_profile_search.py`: Profile search and data collection
- `excel_creator.py`: Excel file creation and data export
- `requirements.txt`: Required Python libraries

### Collected Profile Information

- Name
- Job Title
- Location
- Number of Connections
- Profile Summary
- Profile Link

## Notes

- The application runs on the Firefox browser.
- It is recommended to use the application in accordance with LinkedIn's terms of service.
