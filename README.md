![imagen](https://github.com/user-attachments/assets/c857976c-bc35-417d-8551-276d2f8931af)
![imagen](https://github.com/user-attachments/assets/745e3412-d66c-40c2-9b3b-117081898cae)
![imagen](https://github.com/user-attachments/assets/893e2a19-0f0e-46d9-a367-89e213dd8de9)
![imagen](https://github.com/user-attachments/assets/c41479bb-98ee-4885-b172-44d53f0e3960)
![imagen](https://github.com/user-attachments/assets/5c6f8766-9901-4dfc-bfb0-5c61d48596e4)
![imagen](https://github.com/user-attachments/assets/7b1a58ad-2282-44b7-bfb3-6dbaee045cee)
![imagen](https://github.com/user-attachments/assets/2a671390-9d9b-4c15-99c8-395eeb6a83a8)
![imagen](https://github.com/user-attachments/assets/3010d75b-b614-4fb5-902a-2acb5e5a8a25)
![imagen](https://github.com/user-attachments/assets/01e98ec3-0d53-4a17-9c08-3638cda7c774)
![imagen](https://github.com/user-attachments/assets/a82f86d1-3e1f-47e8-a32c-6ed3199c2323)


## 1. Introduction and Overview

The module integrates multiple functionalities including:

- **Meal Planning and Nutritional Tracking:** Create, manage, and analyze meals and their components.
- **Dietary Goal Management:** Set and track personalized daily nutrient goals.
- **Water Intake Monitoring:** Record daily water consumption and compute total intake.
- **Allergen Management:** Link allergens to products and warn users based on their personal allergen profiles.
- **Gamification:** Award badges to users based on healthy behaviors.
- **Custom Wizards and Reports:** Provide interactive tools such as a recipe suggestion wizard and a QWeb-based PDF nutrition report.

This presentation will walk you through how each of these features is implemented and how they interact to form a comprehensive solution.

---

## 2. Detailed Requirements and How They Are Met

This module was developed to meet specific academic and functional requirements. Let’s review each requirement in detail:

### Field Types

- **Date Fields (Fecha):**
    - `meal_date` in the `meal.template` model records the date of the meal.
    - The `date` field in the `water.intake` model tracks when the water intake is recorded.
- **String Fields:**
    - Fields like `name`, `description`, and `notes` are implemented using `fields.Char` and `fields.Text` to store textual information for meals, products, allergens, etc.
- **Numeric Fields (Número):**
    - Numeric fields such as `calories`, `servings`, and computed fields like `totalcalories` in the `meal.template` model are used to handle quantitative data.
- **Selection Fields (Selección):**
    - The `meal_type` field in `meal.template` is a selection field offering options such as breakfast, lunch, dinner, and snack.
- **Computed Fields (Campo Calculado):**
    - The `totalcalories` field in `meal.template` is computed by summing the calories of each meal item.
    - Similarly, `nutritionscore` and `nutri_score_letter` in the extended `product.template` are computed based on the nutritional facts.

### Models and Their Relationships

- **One-to-Many Relationship:**
    - The `meal.template` model has a one-to-many relation with `mealitem.template`, allowing each meal to have multiple items.
- **Many-to-One Relationship:**
    - Each meal item in `mealitem.template` references a parent meal in `meal.template`.
- **Many-to-Many Relationship:**
    - The allergen management feature uses a many-to-many relationship between the `diet.allergen` model and `res.partner`, enabling the system to track which allergens are relevant for each user.
- **Extended Relationships:**
    - `product.template` is extended to include a one-to-many relationship with `nutritionfact.template` to handle nutritional data.

### Views: Tree, Form, Kanban, and Search

- **Tree and Form Views:**
    - Every model, including meals, products, allergens, and water intake, has both tree and form views. For instance, the `meal.template` form view not only shows basic meal data but also includes an embedded one-to-many view of its meal items.
- **Kanban Views:**
    - The module enhances the product view by implementing a kanban view, which visually groups diet-related products by category, thereby improving data navigation.
- **Search Views:**
    - Customized search views are available, complete with filters (e.g., filter by meal type, high-calorie meals) to assist in data retrieval.
- **Tables and Combo Boxes:**
    - Some views use table layouts (especially in nutrition facts reporting) and combo boxes for selection fields (such as choosing the meal type).

### User Roles and Access Rights

- **Defined Access Rights:**
    - The module includes an `ir.model.access.csv` file that defines two primary roles:
        - **Basic User:** Granted read access and limited write permissions.
        - **Manager/System User:** Granted full CRUD (create, read, update, delete) rights.
- **Security:**
    - Security rules ensure that only authorized users can modify or delete critical records.

### Initial and Demo Data

- **Demo Data:**
    - XML files load demo data for products, meals, allergens, dietary goals, and more, ensuring that the module is demonstrable immediately after installation.
- **Initial Setup:**
    - Preconfigured data assists in both development and demonstration phases.

### Optional Enhancements

- **Reports:**
    - A QWeb PDF report for nutrition facts is implemented, providing a printable document that summarizes the nutritional information of a product.
- **Custom Wizards:**
    - The Recipe Suggestion Wizard is an interactive feature that recommends meals based on a selected product.
- **Cron Jobs:**
    - Automated cron jobs check user activity daily and award badges accordingly.

---

## 3. Environment Setup on Windows

To get the module running on a Windows machine, follow these extended steps:

1. **Install Python 3.x:**
    - Download the installer from [python.org](https://www.python.org/downloads/).
    - Ensure that you select the option to add Python to your PATH.
2. **Install Odoo 17:**
    - Download the Odoo 17 Windows installer from the official Odoo website.
    - Run the installer and follow the on-screen instructions.
    - Configure Odoo using the provided `odoo.conf` file.
3. **Install PostgreSQL:**
    - Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/).
    - Install PostgreSQL and create a new database dedicated to Odoo.
    - Set up a database user with the necessary privileges.
4. **Configure Odoo:**
    - Edit the `odoo.conf` file to include your PostgreSQL database credentials:
        - Parameters like `db_host`, `db_port`, `db_user`, `db_password`, and `db_name` should be correctly set.
5. **Add the Module:**
    - Copy the Diet Facts Management module folder into the Odoo `addons` directory.
    - Restart the Odoo service to load the new module.
    - Log in to the Odoo backend, update the module list, and install the module.

---

## 4. Setting Up the Development Environment

For effective development and debugging, consider the following recommendations:

- **Integrated Development Environment (IDE):**
    - Use VSCode, PyCharm, or another IDE that supports Python and Odoo development.
    - Install Odoo-specific plugins if available.
- **Version Control:**
    - Initialize a Git repository in your module’s directory.
    - Commit your changes regularly and use branches to separate features or fixes.
- **Developer Mode in Odoo:**
    - Activate developer mode from the Odoo settings to access advanced debugging tools and to edit views on the fly.
- **Testing and Logging:**
    - Leverage Odoo’s built-in logging functionality to troubleshoot issues.
    - Write and run unit tests where applicable.
- **Customization Techniques:**
    - Utilize XML inheritance to modify standard views without rewriting them completely.
    - Keep your customizations modular to ease maintenance and future updates.

---

## 5. Module Structure and Code Explanation

The module is organized into several key components, each playing a crucial role.

### 5.1 Manifest and Data Files

- **`__manifest__.py`:**
    - This file serves as the entry point for the module, providing metadata such as the module name, version, author, dependencies, and data files to load.
    - It lists all XML files for views, security, demo data, cron jobs, and reports.
    - An icon is also specified here, ensuring that the module is easily recognizable in the Odoo interface.
- **Data Files:**
    - **XML Views:** Define the structure of tree, form, kanban, and search views.
    - **Security Files:** The `ir.model.access.csv` file sets up user roles and access permissions.
    - **Demo Data:** Files load initial and demo records, which are essential for both testing and presentation.

### 5.2 Models and Their Relationships

Let’s break down the main models:

### Meal Management

- **`meal.template`:**
    - **Purpose:** Represents a meal record with details such as name, type, date, and user.
    - **Key Fields:**
        - `name`: The meal’s name.
        - `user_id`: References the user who logged the meal.
        - `meal_date`: Date of the meal; includes a constraint to prevent past dates.
        - `meal_type`: A selection field (breakfast, lunch, dinner, snack).
        - `totalcalories`: A computed field that sums the calories from all related meal items.
        - `largemeal`: A boolean flag set to true if the total calories exceed a set threshold.
    - **Relationships:** Has a one-to-many relationship with `mealitem.template`.
- **`mealitem.template`:**
    - **Purpose:** Represents individual items within a meal.
    - **Key Fields:**
        - `meal_id`: Many2one field linking back to `meal.template`.
        - `item_id`: References the product (from `product.template`).
        - `servings`: The number of servings.
        - `calories`: Computed from the related product’s calorie information.
    - **Behavior:** Automatically calculates calories per serving using related product data.

### Nutritional Information

- **`product.template` (Extended):**
    - **Purpose:** Manages product data including extended fields for diet items.
    - **Key Additions:**
        - `calories`: Total calories per 100g.
        - `servingsize`: Default serving size in grams.
        - `nutrition_ids`: One2many relationship to `nutritionfact.template`.
        - `nutritionscore` and `nutri_score_letter`: Computed fields that evaluate the overall nutritional quality.
- **`nutritionfact.template`:**
    - **Purpose:** Stores detailed nutritional information for a product.
    - **Key Fields:**
        - `nutrient_id`: Reference to the nutrient (from `nutrient.template`).
        - `value` and `dailypercent`: Numerical values representing nutrient content and its percentage of daily requirements.
        - `uom`: Computed field deriving the unit of measure from `nutrient.template`.
- **`nutrient.template`:**
    - **Purpose:** Defines individual nutrients, such as protein, fat, carbohydrates, etc.
    - **Key Fields:**
        - `name`, `description`: Basic nutrient information.
        - `uom_id`: Links to the unit of measure (e.g., grams).

### Dietary Goals and Water Intake

- **`dietary.goal`:**
    - **Purpose:** Allows users to set daily nutritional targets (calories, protein, fat, carbs).
    - **Behavior:** Contains methods to compute remaining calories based on logged meals.
- **`water.intake`:**
    - **Purpose:** Records daily water consumption.
    - **Key Field:** A computed field that aggregates total water intake for a given day.

### Allergen Management

- **`diet.allergen`:**
    - **Purpose:** Manages allergen information with details on common allergens.
- **Extension of `res.partner`:**
    - **Purpose:** Links partners to allergens via a many-to-many field, so that the system can warn users if a meal contains allergens they are sensitive to.
- **Meal Validation:**
    - **Logic:** The meal model includes logic to check if any meal item contains allergens matching those of the user and raises a validation error if so.

### Gamification

- **`user.badge`:**
    - **Purpose:** Stores records of achievement badges awarded to users.
- **`gamification.tools`:**
    - **Purpose:** Contains helper methods (invoked via a cron job) that analyze user behavior and award badges for milestones such as consecutive days of meal logging and adequate water intake.

### Wizards and Controllers

- **Recipe Suggestion Wizard:**
    - **Purpose:** Provides an interactive wizard that suggests recipes based on a selected product.
    - **Implementation:** Uses a transient model and a dedicated view.
- **Controllers:**
    - **Purpose:** Handle HTTP routes, such as generating and downloading PDF reports. For example, the route `/nutrition/facts/<int:product_id>/pdf` triggers the QWeb report generation.

### 5.3 Views: Detailed Breakdown

- **Tree Views:** Offer a tabular layout of records. For instance, the meal tree view lists meal names, dates, types, and total calories.
- **Form Views:** Provide detailed record editing forms. The meal form view not only includes fields for basic meal details but also embeds a one-to-many list of meal items.
- **Kanban Views:** Enhance visual representation; for example, diet products are grouped by category in a kanban layout.
- **Search Views:** Feature advanced filtering options allowing users to quickly narrow down records based on criteria like meal type or calorie content.
- **UI Components:** Some views incorporate tables to display nutrition facts and combo boxes to allow selection of options (e.g., meal type).

### 5.4 Access Rights and Security

- **Security Configuration:**
    - An `ir.model.access.csv` file defines the access rules for each model.
    - Two primary user roles have been established:
        - **Basic Users:** Typically only have read and limited write permissions.
        - **Managers:** Possess full CRUD capabilities.
- **Practical Implications:** This ensures data integrity and prevents unauthorized modifications.

### 5.5 Reports and Wizards

- **Nutrition Facts Report:**
    - A QWeb template is used to generate a detailed PDF report that includes product information, serving size, and a comprehensive nutrient breakdown in a table.
    - The report is accessed via a controller route, ensuring it is only available to authenticated users.
- **Recipe Suggestion Wizard:**
    - This wizard offers interactive functionality where a user selects a primary ingredient, and the system suggests a set of meals that incorporate that ingredient.
    - It demonstrates how transient models and wizard views can provide a guided user experience.

### 5.6 Controllers and Cron Jobs

- **Custom Controllers:**
    - Controllers in the module handle HTTP requests and generate dynamic content. For example, the Nutrition Facts PDF report is generated and returned as a downloadable file.
- **Cron Job for Gamification:**
    - A scheduled task (cron job) runs daily, invoking the `cron_award_badges` method from `gamification.tools`. This method evaluates user activity and awards badges when certain criteria are met (e.g., a 7-day meal logging streak or adequate water intake).

---

## 6. Utility and Benefits

The benefits of this module are extensive:

- **Centralized Diet Management:** Consolidates meal planning, nutritional tracking, and dietary goals into a single application.
- **User Engagement:** Gamification elements like badge awards encourage users to maintain healthy habits.
- **Detailed Nutritional Analysis:** The nutrition facts report provides valuable insights for users, nutritionists, and health professionals.
- **Personalized Experience:** Users can set their dietary goals, track water intake, and receive recipe suggestions based on their preferred ingredients.
- **Scalability:** The module’s design allows for easy extension and integration with additional features or third-party APIs.

---

## 7. Potential Improvements

While the module is comprehensive, here are some ideas for further enhancements:

- **Enhanced Analytics:**
    - Develop interactive dashboards with visual charts and graphs to display nutrient intake trends.
    - Integrate business intelligence tools for in-depth dietary analysis.
- **Mobile Optimization:**
    - Improve the UI/UX for mobile devices to facilitate on-the-go dietary tracking.
- **Advanced Recommendation System:**
    - Implement machine learning algorithms to provide more personalized meal recommendations based on historical data.
- **Expanded API Integrations:**
    - Integrate with external APIs (such as OpenFoodFacts) to enrich product information and support barcode scanning functionalities.
- **User Feedback Mechanisms:**
    - Add functionality for users to rate meals and provide feedback, enhancing the interactive experience.
- **Internationalization:**
    - Incorporate multi-language support and adapt nutritional standards to regional requirements.

---

##
