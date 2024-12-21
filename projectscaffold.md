# SAR AOI Manager - Project Scaffold

## 1. Introduction

This document outlines the development plan for the SAR AOI Manager application, a desktop application designed to help users manage Areas of Interest (AOIs) and interact with Google Earth Engine (GEE) for Synthetic Aperture Radar (SAR) data processing and visualization.

The application will be built using Python and the Qt framework, targeting Ubuntu Linux as the primary operating system. It will provide a user-friendly interface for defining, visualizing, and managing AOIs, filtering GEE image collections, previewing SAR data, and exporting processed imagery as GeoTIFFs.

## 2. Application Overview

### 2.1. Purpose

The SAR AOI Manager aims to simplify the following workflows:

*   **AOI Management:** Allow users to easily create, import, edit, visualize, and delete AOIs.
*   **GEE Data Access:** Provide an intuitive way to interact with the GEE platform for searching and filtering SAR image collections.
*   **Data Preview:** Enable users to quickly preview SAR data with customizable visualization parameters.
*   **Data Export:** Facilitate the export of processed SAR data as GeoTIFFs for use in other GIS applications.
*   **Reliable Operation:** Ensure a stable user experience with robust state management and error handling.

### 2.2. Target Users

This application is intended for researchers, scientists, and geospatial analysts who work with SAR data and need a tool to streamline their AOI management and GEE data access workflows. The target users are expected to have a basic understanding of GIS concepts and familiarity with Google Earth Engine. The app will be deployed either on local native Ubuntu Linux, or on WSL or a Linux VM within a Windows operating system.

## 3. Functional Requirements

### 3.1. AOI Management

*   **Create AOI:**
    *   Allow users to create new AOIs by drawing polygons on an interactive map.
    *   Allow users to create new AOIs by importing an existing GeoJSON.
*   **Import AOI:**
    *   Enable users to import AOIs from GeoJSON files stored locally.
*   **Load AOI:**
    *   Automatically load existing AOIs from a designated directory on application startup.
*   **Edit AOI:**
    *   Allow users to modify the geometry of existing AOIs using on-map drawing tools.
    *   Allow users to edit existing AOIs by importing an existing GeoJSON.
*   **Delete AOI:**
    *   Allow users to delete AOIs.
    *   Implement a warning before an AOI is permanently deleted.
*   **Export AOI:**
    *   Enable users to export selected or all AOIs as GeoJSON files.
*   **Visualize AOI:**
    *   Display AOIs on the interactive map.

### 3.2. Google Earth Engine (GEE) Interaction

*   **Authentication:**
    *   Implement GEE authentication using the Python GEE API to allow the application to access GEE functionality on behalf of the user.
*   **Image Filtering:**
    *   Allow users to filter GEE image collections based on:
        *   Selected AOI
        *   Date range (start and end dates)
        *   Other relevant parameters (e.g., sensor platform, cloud cover percentage - optional)
*   **Image Count:**
    *   Display the number of images that match the user's filter criteria.
*   **SAR Data Preview:**
    *   Allow users to preview SAR data on the map.
    *   Enable users to adjust visualization parameters (e.g., band selection, min/max values, palette) for the preview.
*   **GeoTIFF Export:**
    *   Allow users to export filtered GEE imagery for a selected AOI as a GeoTIFF.
    *   Provide options to export either to the user's Google Drive or to a local directory.
    *   Enable configuration of export parameters (e.g., resolution, projection).

### 3.3. User Interface

*   **Main Window:**
    *   Menu bar with options for File (Open, Save, Export), AOI (New, Import, Manage), Settings, and Help.
    *   Optional toolbar with icons for quick access to frequently used actions.
*   **AOI List Panel:**
    *   A panel displaying a list of available AOIs.
    *   Checkboxes for selecting multiple AOIs.
    *   Buttons or context menu options for adding, editing, and deleting AOIs.
*   **Map View Panel:**
    *   An interactive map displayed using maplibre-gl-js within a QtWebEngine widget.
    *   Visualizes AOIs, SAR data previews, and supports AOI drawing.
*   **Image Information Panel:**
    *   Displays the count of images matching the current filter criteria.
    *   Provides controls for exporting data as GeoTIFFs.
    *   Optionally, includes a timeline widget to visualize the temporal distribution of the filtered images.
*   **Filter Panel:**
    *   Date pickers for selecting the start and end dates for filtering.
    *   Optionally, additional filter controls (e.g., dropdowns, checkboxes) for other GEE filter parameters.
    *   Buttons to trigger "Get Image Count", "Preview SAR Data", and "Reset" actions.

### 3.4. Reliability and Error Handling

*   **Query System:**
    *   Implement a query-like system to manage user interactions and avoid unexpected behavior when updating or refining search parameters.
    *   Store the last used query parameters (AOI, date range, filters) to repopulate UI elements on update.
    *   Use separate, explicit actions/buttons for distinct operations.
*   **State Management:**
    *   Properly manage the application state, especially regarding AOI creation/editing and temporary data.
    *   Reset temporary data when a user starts a new query or switches to a different operation.
*   **Error Handling:**
    *   Use `try-except` blocks to gracefully handle potential errors (e.g., network issues, GEE API errors, file I/O errors).
    *   Display informative error messages to the user through message boxes or status bar updates.
*   **Logging:**
    *   Log application events, warnings, and errors to a file for debugging purposes.

### 3.5 Settings and Preferences

*   **AOI Directory:**
    *   Allow the user to configure the default directory for storing AOI GeoJSON files.
*   **GEE Authentication:**
    *   Store GEE credentials securely using the GEE Python API's authentication mechanisms, you should define how a token would be generated for the JS client's use as well.
*   **Other Settings:**
    *   Potentially, allow the user to configure other application settings (e.g., map appearance, default filter values).

## 4. Technology Stack

*   **Programming Language:** Python
*   **GUI Framework:** Qt (PyQt6 or PySide6)
*   **Mapping Library:** maplibre-gl-js
*   **Web Browser Component:** QtWebEngine (for embedding the map and GEE JavaScript API)
*   **GEE APIs:**
    *   Google Earth Engine Python API (for authentication and export tasks, other operations may be considered on a case by case basis)
    *   Google Earth Engine JavaScript API (for map display, filtering, and data preview within QtWebEngine)
*   **Data Handling:**
    *   `geopandas`: For reading, writing, and processing GeoJSON files.
    *   `pandas`: For managing tabular data (e.g., image metadata).
*   **Other Libraries:**
    *   `requests`: For making HTTP requests (e.g., downloading GeoTIFFs).
    *   `psutil`: For process management (in the `killapp.py` script).

## 5. Project Structure

```
sar_aoi_manager/
├── main.py                # Main application entry point
├── appstart.py            # Script to start the application
├── authenticate.py        # Script to handle GEE authentication
├── killapp.py             # Script to terminate application instances
├── setup.py               # Script to set up the development environment
├── aoi_manager/           # Module for AOI management
│   ├── __init__.py
│   └── aoi.py            # AOI class, handling GeoJSON data
├── gee_interface/         # Module for interacting with GEE
│   ├── __init__.py
│   ├── image_viewer.py       # Handles map display and interaction
│   ├── gee_utils.py          # Functions for GEE API calls (authentication, filtering, etc.)
│   └── <>.js                 # Javascript code for configuration and interfacing with maplibre and GEE's JS client, as well as defining communication messages with Python
├── ui/                    # UI-related files
│   ├── __init__.py
│   ├── main_window.py     # Main window class and logic
│   ├── resources.py       # Compiled Qt resources (icons, etc.)
│   ├── <ui_name>.ui       # UI layout files created with Qt Designer
│   └── style.qss          # Qt stylesheet (optional)
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── helpers.py        # General helper functions
├── tests/                 # Unit tests
│   ├── __init__.py
│   ├── test_aoi.py        # Tests for AOI management
│   └── test_gee_utils.py  # Tests for GEE interaction
├── resources/             # Icons, images, and other static assets
├── data/                  # Default directory for storing AOI GeoJSON files (can be changed by the user)
├── requirements.txt       # Lists project dependencies
└── .gitignore             # Specifies files and folders to be ignored by Git
```

## 6. Development Steps

1. **Environment Setup:**
    *   Create a virtual environment for the project.
    *   Install the required packages listed in `requirements.txt` using `setup.py`.
2. **UI Design:**
    *   Use Qt Designer to create the user interface layout, including the main window, panels, and widgets.
    *   Save the UI designs as `.ui` files in the `ui/` directory.
    *   Compile the `.ui` files into Python code using `pyuic6` and configure maplibre using QtWebEngine.
    *   Design the communication interface with Javascript running within **QtWebEngine** and implement asynchronous message handling.
3. **Core Functionality Implementation:**
    *   Implement the `AOI` class in `aoi_manager/aoi.py` to handle AOI data loading, saving, and geometry management.
    *   Develop functions in `gee_interface/gee_utils.py` to interact with the GEE Python API for authentication, image filtering, and GeoTIFF export.
    *   Implement map display, AOI visualization, and drawing tools using **maplibre-gl-js** within **QtWebEngine** in `gee_interface/image_viewer.py` and relevant Javascript files loaded into it.
    *   Connect UI signals to slots in `main_window.py` to trigger appropriate actions in response to user interactions.
4. **GEE Integration:**
    *   Write functions to handle GEE authentication, image filtering, data preview, and GeoTIFF export, you will make the design decision whether to use the Python or Javascript API on a case by case basis.
    *   Ensure the Python and JavaScript components can communicate effectively, passing data and triggering actions as needed. Consider abstracting this communication using asynchronous handlers or a dedicated message queue to avoid UI freezes.
5. **Query System and State Management:**
    *   Implement the query system to store and manage the last used query parameters.
    *   Ensure that the UI state is properly managed and reset between operations to prevent inconsistent behavior.
6. **Error Handling and Logging:**
    *   Add `try-except` blocks to handle potential errors gracefully.
    *   Implement logging to record important events and errors for debugging.
7. **Testing:**
    *   Write unit tests for the `AOI` class and GEE interaction functions, you may define tests for testing the Javascript as well.
8. **Script Development:**
    *   Create the `setup.py`, `authenticate.py`, `appstart.py`, and `killapp.py` scripts. Ensure they work as intended and handle errors properly.

## 7. File Descriptions

*   **`main.py`:** The entry point for the application. Creates the `QApplication` and main window instances, initializes the UI, and starts the event loop.
*   **`appstart.py`:** Activates the virtual environment and starts the main application using `main.py`
*   **`authenticate.py`:** Uses the GEE Python API to handle user authentication with Google Earth Engine.
*   **`setup.py`:** Creates a virtual environment and installs the required Python packages listed in `requirements.txt`.
*   **`killapp.py`:** Terminates running instances of the application, identified by process name.
*   **`aoi_manager/aoi.py`:**
    *   Defines the `AOI` class for managing AOI data:
        *   `load_from_geojson(filepath)`: Loads AOI data from a GeoJSON file.
        *   `save_to_geojson(filepath)`: Saves AOI data to a GeoJSON file.
        *   `get_geometry()`: Returns the AOI geometry for use with GEE.
*   **`gee_interface/gee_utils.py`:**
    *   Contains functions for interacting with the GEE Python API:
        *   `authenticate()`: Handles GEE authentication (if not already authenticated).
        *   `get_filtered_image_collection(aoi, start_date, end_date, other_filters)`: Filters GEE image collections based on input parameters.
        *   `export_geotiff_to_drive(image, description, folder, filename, region, scale, crs)`: Exports a GeoTIFF to Google Drive.
        *   `export_geotiff_to_local(image, description, filename, region, scale, crs)`: Downloads a GeoTIFF to the local filesystem.
*   **`gee_interface/image_viewer.py`:**
    *   Handles the map display and interaction using maplibre-gl-js within QtWebEngine:
        *   `display_map()`: Initializes and displays the map.
        *   `add_aoi_to_map(aoi)`: Adds an AOI to the map for visualization.
        *   `display_sar_preview(image, vis_params)`: Displays a SAR data preview on the map using GEE's JavaScript API, as well as implement how GEE JS client would be initialized and used.
        *   Handles drawing new AOIs on the map and communicating the geometry data to the `AOIManager`, ensuring drawing is properly handled, emitting a message or function call that can be understood by the python side.
        *   Defines how to style and configure maplibre, including controls, and handlers for map interaction as well as those needed by GEE.
    *   Handles communication with the JS side using **QtWebEngine**.
*   **`ui/main_window.py`:**
    *   Defines the `MainWindow` class, which sets up the main application window:
        *   Loads the UI from the `.ui` file created by Qt Designer or using code to generate it.
        *   Connects UI signals (e.g., button clicks, menu selections) to corresponding slot functions.
        *   Implements slot functions to handle user actions (e.g., creating an AOI, filtering images, triggering export).
        *   Manages the interaction between different UI components (e.g., AOI List Panel, Map View, Filter Panel, Image Information Panel).
        *   Implements the query system to store and manage the last used query parameters.
*   **`ui/resources.py`:** A Python file generated by compiling a `.qrc` resource file (using `pyrcc6`). It contains binary data for icons, images, and other resources used in the UI.
*   **`ui/<ui_name>.ui`:** UI layout files created using Qt Designer, defining the visual structure of different parts of the application's user interface (e.g., `main_window.ui`, `filter_panel.ui`).
*   **`utils/helpers.py`:** Contains general-purpose utility functions that might be used across different modules of the application (e.g., date/time formatting, string manipulation).
*   **`tests/test_aoi.py`:** Unit tests for the `aoi_manager/aoi.py` module, verifying the correct behavior of AOI loading, saving, and geometry handling.
*   **`tests/test_gee_utils.py`:** Unit tests for the `gee_interface/gee_utils.py` module, verifying the correct behavior of GEE API interactions (filtering, export).
*   **`resources/`:** A directory for storing static resources like icons, images, and potentially example GeoJSON files.
*   **`data/`:** The default directory where AOI GeoJSON files are stored. Can be changed by the user in the application settings.
*   **`requirements.txt`:** A text file listing the project's Python dependencies. Used by `setup.py` to install the required packages.
*   **`.gitignore`:** Specifies files and directories that should be ignored by Git version control (e.g., virtual environment directory, compiled Python files, `.DS_Store`).

## 8. Further Considerations

*   **Asynchronous Operations:**  Long-running operations, such as GEE API calls, image filtering, and GeoTIFF export, should be performed asynchronously to prevent the UI from freezing. This can be achieved using Python's `asyncio` or by using Qt's threading mechanisms. An event loop for example can help to define such a queue to handle messages passed by between the JS side and the Python side.
*   **Code Style and Documentation:** Follow consistent code style guidelines (e.g., PEP 8 for Python) and document the code thoroughly using docstrings and comments to ensure maintainability.
*   **Version Control:** Use Git for version control throughout the development process, define which files should not be managed by it as well.

## 9. Conclusion

This scaffold provides a detailed starting point for developing the SAR AOI Manager application. It outlines the functional requirements, technology choices, project structure, and development steps. This document serves as a guide for developers and LLMs involved in building the application, providing sufficient context to understand the project goals and contribute effectively. By following this scaffold, the development process should be well-organized, efficient, and result in a robust and user-friendly application. Remember to prioritize testing, error handling, and logging to ensure the application's reliability and maintainability. Consider generating more comprehensive documentation once code is written, using the docstrings and code generated, as well as incorporating this document as part of it's README or main documentation.
```


