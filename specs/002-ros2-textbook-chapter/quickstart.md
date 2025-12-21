# Quickstart Guide

This guide explains how to set up the development environment for the Docusaurus textbook.

## Prerequisites

-   Node.js (LTS version, 20.x)
-   npm (comes with Node.js)

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2.  Navigate to the project directory:
    ```bash
    cd <project-directory>
    ```
3.  Install the dependencies:
    ```bash
    npm install
    ```

## Running the Development Server

To start the local development server with live reloading:

```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) to view the site.

## Building the Site

To generate a static build of the site:

```bash
npm run build
```

The build output will be in the `build` directory.

## Contributing

1.  Create a new branch for your changes:
    ```bash
    git checkout -b feature/your-feature-name
    ```
2.  Add or edit content in the `docs` directory. Follow the structure defined in `data-model.md`.
3.  Commit your changes and push to the remote repository.
4.  Create a pull request.


## Notes for WSL Users

- Run the project inside the Linux filesystem (e.g. `/home/username/project`), NOT `/mnt/c`, to ensure file watching works correctly.
- If live reload does not trigger, restart the dev server.

