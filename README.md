# Lost and Found Web Application

## Video Demo 
https://youtu.be/tiYGu9tmOLc

## Description
This Lost and Found Web Application was created to help citizens of Sudan, who are suffering from the effects of war and displacement. Many people have lost their personal property, and this platform is designed to help reunite them with their belongings. Users can register, post details about lost or found items, and the system will automatically match entries. When a match is found, it displays the finder’s or owner’s phone number and username, making it easier for users to get in touch.

This platform is divided into categories like vehicles, electronics, and others to help users efficiently navigate the listings.

As my first integrated project, I’m incredibly proud of what I’ve achieved with this application. While there is a chance that some errors may occur, I’m open to feedback to make it even better. Feel free to share your thoughts at salahkki@hotmail.com.

## Features
- **Browse Without Login**: Users can browse all lost and found posts without the need to log in.
- **User Registration & Posting**: Login is only required when a user wants to publish a post about a missing or found item. Users can register to an account by providing a username, phone number, and password. No email or phone number verification is required.
- **Recent Posts on Main Page**: The main page features a collection of recently published posts from all sections (vehicles, electronics, and others), whether they are lost or found.
- **Easy Navigation**: Users can easily navigate between sections. For example, if a user has lost a vehicle, they can click "I lost" from the navigation menu and choose "vehicle" from a dropdown. This leads them to a page containing the form to submit vehicle details, along with a list of recently found vehicles.
- **Automatic Matching**: While filling out the form, the site automatically matches the entered specifications with existing lost or found items in the system.

## Future Features
- **Image Upload**: In the near future, users will be able to upload pictures with their posts, making it easier to identify lost or found items.
- **Comments and Messaging**: Users will soon have the ability to leave comments on posts or message the person directly through the site to facilitate communication.

## File Structure

- **app.py**: Contains all routes:
  - `/` to display database content
  - `post` to publish a new lost or found post
  - `query` for navigation between pages
  - `login` and `logout` for user session management
  - `register` for user registration
  - `search` API to dynamically filter and display search results via AJAX
  - `change_password` to update user passwords
  
  Only the logout, post, and change password routes require login.

- **helpers.py**: A collection of utility functions, including:
  - `apology()` for displaying error messages
  - `login_required()` to ensure login for protected routes
  - `get_current_time()` to retrieve the current timestamp
  - `validate_id()` and `get_id_value()` to handle database IDs
  - Several other functions for filtering and handling results.

- **/static**: Contains `search.js` for fetching and displaying search results in real-time using AJAX.

- **/images**: Stores default images for different categories like vehicles, electronics, and others.

- **/templates**:
  - `layout.html` for the main layout
  - `index.html`, `login.html`, `register.html`, and `change_password.html` for user interaction forms
  - `condition.html` for the dropdown menu with category options and card display
  - `property.html` for posting and searching forms that correspond with specific categories
  - `search.html` for rendering search results using AJAX.

- **lostandfound.db**: The database schema includes:
  - `users` table for storing user credentials (id, username, and hashed password)
  - `colors`, `vehicle_brands`, `vehicles_list` tables for reference in forms
  - Separate tables for each category, with details like color_id, user_id, condition_id, etc.
  - The `others` table contains free text for item descriptions.
  - The `publication` table holds all posts with a `property_id` and `post_id`.

---

## Additional Features

- **Planned Enhancements**:
  - Ability for users to upload images, likely through a file storage system such as AWS S3 or a local file storage system, with security to ensure images are properly filtered for inappropriate content.
  - Messaging system for users to communicate directly. This will likely involve an internal messaging feature to protect user privacy while facilitating contact between item finders and owners.
  - Improved security features such as stronger password requirements (e.g., minimum length, mix of uppercase and lowercase letters, numbers, and special characters) and email verification.

- **Session Management**: Flask-Session is configured to store user information on the server's filesystem (not using signed cookies). It tracks `session["user_id"]` and `session["username"]`, and uses `session["info"]` to manage flash message types (e.g., success, error, info).

- **Error Handling**: The application ensures input validation on both client and server sides. Most input fields use select menus to reduce errors. The server validates all input before processing it and provides appropriate error messages when validation fails.

- **AJAX Search Processing**: The search functionality allows users to see search results instantly while they fill out the form, without the need to submit or refresh the page. Results appear in real-time as data is entered.

- **Security**: Passwords are hashed using a secure algorithm before storing them in the database to protect user credentials. Although the current version does not include advanced security features beyond password hashing, future enhancements will focus on password complexity (minimum length, mix of characters) and email or phone number verification.


---

## Installation

1. Clone the repository:
   
2. Navigate to the project directory:
   
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database:
   - The project uses the CS50 SQL library to connect to a SQLite database. Make sure to initialize the database schema using the provided SQL scripts in the `schema.sql` file.
   ```bash
   flask run
   ```

5. Run the application:
   ```bash
   flask run
   ```

## Usage

1. **Register**: Users can sign up by providing a username, phone number, and password. No email or phone number verification is required.
2. **Post Lost or Found Items**: Use the form to input details about the item (e.g., item description, manufacture year, serial number).
3. **View Matches**: When the system finds a match, it will notify the user by displaying the other user’s contact information (phone number and username).
4. **Login and Logout**: Users can log in and log out using session management via Flask-Session.

## Technology Stack

- **Backend**: Python, Flask, Flask-Session, CS50 SQL Library
- **Frontend**: HTML, CSS (Bootstrap for responsive design), JavaScript
- **Templating Engine**: Jinja (used to dynamically render HTML content)
- **Database**: SQLite (using CS50 SQL Library)

## Credits

This project was developed as part of the CS50 course. Thanks to the CS50 team for providing resources and support during development.

<!-- This README file was made with the help of ChatGPT, an AI language model. -->
