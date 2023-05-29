# Story Generator with Resilient Task Queue

![Main Menu](/assets/menu.png "main menu")
## Overview

This project is a creative output from the [AIDevs course](https://AIDevs.pl). It crafts cautionary tales based on a given subject. The application creates a list of chapters, and then generates a short paragraph for each one.

[This is an example output for the subject: "zombie batman takes the revenge" with GPT-4 model.](/assets/zombie_batman_example.txt)


## Features

1. **Sequential Story Building:** Paragraphs are generated in sequence, ensuring a flowing narrative structure

2. **Resilient Task Queue:** Application implements a resilient task queue. If the application is interrupted or terminated, it has the ability to resume operations from where it last stopped, preventing loss of progress

3. **Persistent Storage:** Data is stored in a SQLite database located in `project_root/tasks.db`

4. **Export to TXT:** The generated story can be exported to a TXT file located in `project_root/output.txt`


## Getting Started

### Prerequisites

Ensure that Python is installed on your system.

### Installation

1. **Clone the repository** to your local machine:

    ```
    git clone <repository_url>
    ```

2. **Navigate to the project directory**:

    ```
    cd <project_directory>
    ```

3. **Install the necessary dependencies**:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Configure the application by filling in the appropriate values in the `config.py` file. Use `gpt-4` model for the best quality, or `gpt-3.5-turbo` for faster results.

2. Start the application with:

    ```
    python main.py
    ```

Now you are all set to start generating unique cautionary tales!

