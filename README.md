

# Note APP -Serverless Architecture


* *Demo URL*: [<https://kenil-patel-csci-5709-web-a1.netlify.app/>](https://kenil-patel-csci-5709-web-a1.netlify.app/)

## Authors
Kenil Shaileshkumar Patel

## Getting Started

### Prerequisites

To have a local copy of this lab up and running on your local machine, you will first need to install the following software / libraries / plug-ins

```
npm (Comes with node.js installation)

"axios": "^1.7.2",
"react": "^18.2.0",
"react-dom": "^18.2.0",
"react-error-boundary": "^4.0.13",
"sweetalert2": "^11.11.0"
```

See the following section for detailed step-by-step instructions on how to install this software / libraries / plug-ins

### Installing

#### Install Node.js (to use npm)

1. Goto https://nodejs.org/en/download and download the LTS installer as per your OS.
2. Run the installer.
3. Accept License Agreement
4. Choose Installation path.
5. Keep the default installation settings and click next.
6. Skip the optional installation window and click next and click install.
7. To check the installation, run the below commands.

```
node -v
```
Sample output: v20.12.2
```
npm -v
```
Sample output: 10.5.0

#### Install React and related libraries
```
npm install
```

## Deployment

Link the GitHub/GitLab repository with [Netlify](https://app.netlify.com/).
Then, use the below site configurations:

* Base directory: `/frontend`
* Build command: `npm run build`
* Publish directory: `/frontend/dist`


## Built With


* [React](https://react.dev/) - The Frontend Library
* [Vite](https://vitejs.dev/guide/) - Tool to generate boilerplate code and structure of a React App
* [npm](https://www.npmjs.com/) - Dependency management


