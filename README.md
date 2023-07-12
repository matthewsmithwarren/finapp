<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/matthewsmithwarren/finapp">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Stock Trading Sandbox deployed on AWS EC2</h3>

  <p align="center">
    Refactored the Finance web application to work outside of Harvard's CS50 environment and then deployed on AWS EC2
    <br />
    <a href="https://github.com/matthewsmithwarren/finapp"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/matthewsmithwarren/finapp">View Demo</a>
    ·
    <a href="https://github.com/matthewsmithwarren/finapp/issues">Report Bug</a>
    ·
    <a href="https://github.com/matthewsmithwarren/finapp/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](http://54.85.147.105/login)

The Finance web app from Harvard's CS50 was refactored so that it could be deployed to AWS EC2 as a persistent, publicly available Stock Trading Sandbox for any user.

Moving outside of the safety of the GitHub Codespace which is managed by the computer science faculty, enabled a practical self-learning of DevOps tasks. Some new skills and proficiencies are using Git to push/pull code from repositories/remotes, setting up codespaces, getting comfortable with SSH access between local, Ubuntu, AWS EC2 and GitHub, setting up virtual environments to test/run the app, provisioning servers and installing software packages and managing dependencies. Trouble-shooting and reestablishing API calls to a less expensive IEX endpoint after the trial-period ended, and then refactoring the app to work with the cheaper IEX package (eg. companyName unavailable).

The complexity of getting code to work in various environments is staggering. Now that I've gone through the process of learning and the pain of initiating and terminating AWS instances 15 - 30 times, the motions of DevOps tasks become more clearly understood and translatable to future projects.

While I understand the pragmatic reason to reduce complexity for the scope of CS50 so that instructors aren't dragged down with endless complaints from students who have unending "issues" with their local computer, this last step of learning how to deploy code from a GitHub repository to a cloud provider has been so important for the confidence to continue learning and to continue to explore and create.

A series of blockers caused this deployment to take much more effort than a typical problem set. Adding to challenges was the fact that there was little support from other classmates working on the same project. Google, StackOverflow and other communities became the source of solutions to each hurdle. And, it was this difficulty and independence that made the eventual success such an outstanding learning process.

As an example, there are insufficient permissions to install NodeJS on this local computer. After exploring various solutions like Oracle's Virtual Box, a Ubuntu GitHub CodeSpace was utilized to run the app while continuing to use the local computer and Visual Studio Code to move files and edit code. Git commands kept everything in sync.

A major blocker that became a learning opportunity was the API for stock price lookup. Finance worked for less than 48 hours before IEX shut down the trial membership in the last days of May 2023. CS50 faculty shifted to a Yahoo Finance API on June 1st but my research showed that Yahoo had shut down the service and it only yielded end-of-day pricing where real-time pricing is important to the user experience. The original code was built around IEX trial using a "premium data package" to pull "companyName", "symbol" and "latestPrice". For this project, a minimum "Bid, Ask, LastTrade" package offered only "symbol" and "price" so the application had to be refactored in a number of functions to accomodate this change. It must also be remembered that an important part of solving problems is understanding where it's breaking. When the IEX API was failing because it was using a premium endpoint and then failing because it was looking for an attribute that was no longer available, exploring a third stock price API (Alpha Vantage) was helpful because the documentation provided some sample code to test the response. This testing method was easily adapted to figure out the IEX problem.

There was a minor blocker using the PYTZ package for timezone because this has been deprecated.

Another key challenge was learning how to a production web server. Gunicorn and Nginx are used to establish a service on the AWS EC2 instance. Gunicorn and Nginx along with a service file placed in the SystemCTL directory help to automate the process of running the app in a production environment. Setup involves a complex series of steps with the systemctl, venv, daemon, ports and proxies. However, once you are using a Gunicorn/Nginx service, it is important to incorporate the API_KEY environment in this automation. Digging into the Flask, Gunicorn and Nginx documentation, a solution was found. An area that is still not fuly understood, adjusting the systemctl seems to be fragile such that once a service file was modified, the AWS EC2 server did not respond well to edits. So, in the DevOps tinkering, frequently a new instance would be spun up on AWS and the old one terminated. Although tedious, the repetition helped improve my skills, knowledge of templates and overall confidence with cloud provider AWS.

In summary, the Stock Trading Sandbox final project has been an opportunity to translate CS50 basic programming skills in C, Python and SQLite3 to having the confidence to create and deploy software for the friends, family and others people around the world to use and enjoy.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* Flask
* Python3-venv
* Pip3
* Flask and Flask_Session
* CS50
* Requests
* SQLite3
* Gunicorn
* Nginx
* AWS EC2
* VisualStudioCode
* GitHub and Codespaces
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps. Deploying to AWS EC2 is more involved and will be covered in later section.

### Prerequisites

Start with a Ubuntu OS somewhere. Then you'll need the following software.
* Update to current version of Ubuntu OS
  ```sh
  sudo apt-get update
  ```
* Install Python with option to create virtual environments
  ```sh
  sudo apt-get install python3-venv
  ```
* Create and activate virtual environment
  ```sh
  python3 -m venv venv
  ```
  ```sh
  source venv/bin/activate
  ```

### Installation

1. Get a free one-week trial API Key at [https://iexcloud.io/](https://iexcloud.io/)
2. Make sure you in the correct parent directory. Clone the repo and a folder "finapp" will created.
   ```sh
   git clone https://github.com/matthewsmithwarren/finapp.git
   ```
3. Install dependency packages with pip3 (part of python3)
  ```sh
  pip install flask
  pip install flask_session
  pip install cs50
  pip install requests
  sudo apt-get install sqlite3
  ```
4. Provide API_KEY
  ```sh
  export API_KEY="Your API key here inside the quotations"
  ```
5. Run the application (also may use "python app.py")
  ```sh
  flask run
  ```

### AWS EC2 deployment

1. Get a free-tier AWS account and create a Ubuntu instance on EC2.
2. Terminal commands to install and start finapp on AWS
3. SSH into AWS EC2 server
  ```sh
  $ ssh -i <your key name>.pem ubuntu@<Public DNS of your EC2> (get this from aws)
  ```

4. Prepare environment on EC2 similar to local
  ```sh
  sudo apt-get update
  sudo apt-get install python3-venv
  ```

5. Create an SSH connection to the GitHub account with the finapp code
  ```sh
  ssh-keygen
  
  Few returns on keyboard for default options.

  Then copy the public key to give to GitHub
  cat ~/.ssh/id_rsa.pub
  
  Copy the meat of what is returned.
  Go into GitHub settings and add SSH key with paste of what was copied above.
  Save it.

  Within GitHub, go back out to the finapp repository and copy the link under the Clone SSH tab.
  ```

6. Switch to aws/ubuntu terminal and clone finapp code
  ```sh 
  git clone <link to finapp repository>
  ls
  cd finapp
  ```

7. Create virtual environment and set up in a way similar to local
  ```sh
  python3 -m venv venv
  ```

8. Activate venv
  ```sh
  source venv/bin/activate
  ```

9. Install packages
  ```sh
  pip install flask
  pip install flask_session
  pip install cs50
  pip install requests
  ```

10. Install Sqlite3
  ```sh
  Sudo apt-get install sqlite3
  ```

11. Install Gunicorn
  ```sh
  pip install gunicorn
  gunicorn -b 0.0.0.0:8000 app:app —env API_KEY=“Your API_KEY here”
  ```

12. Create a Gunicorn service to automatically start finapp on EC2
  ```sh
  // When using Nano to create/modify files, use Ctrl-O, enter, Ctrl-X to save and exit Nano file editor
  sudo nano /etc/systemd/system/finapp.service
  ```

13. Copy this below into the file above
  ```sh
  [Unit]
  Description=Gunicorn instance for a simple stock trading app
  After=network.target
  [Service]
  User=ubuntu
  Group=www-data
  WorkingDirectory=/home/ubuntu/finapp
  ExecStart=/home/ubuntu/finapp/venv/bin/gunicorn -b localhost:8000 app:app —env API_KEY=“Your API_KEY here”
  Restart=always
  [Install]
  WantedBy=multi-user.target
  ```

14. Enable the finapp.service
  ```sh
  sudo systemctl daemon-reload
  sudo systemctl start finapp
  sudo systemctl enable finapp
  ```

15. Check that app is working
  ```sh
  curl localhost:8000
  ```

16. Install Nginx
  ```sh
  sudo apt-get install nginx
  sudo systemctl start nginx
  sudo systemctl enable nginx
  ```

17. Check the public ip address from AWS to see a Nginx message

18. Modify Nginx service file to connect with finapp proxy
  ```sh
  sudo nano /etc/nginx/sites-available/default
  ```

19. Insert the text below into the code just below comments section
  ```sh
  upstream flaskfinapp {
      server 127.0.0.1:8000;
  }
  ```
20. Find the "location" section of the code and modify to the text below
  ```sh 
  location / {
      proxy_pass http://flaskfinapp;
  }
  ```

21. Follow the Nano steps (Ctrl-O, enter, Ctrl-X) to save and exit back to terminal and restart Nginx
  ```sh
  sudo systemctl restart nginx
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] HTTPS Secure website and favicon
- [ ] Add HTML page to show a scoreboard of users
    - [ ] include sort capability for performance and user name 
- [ ] Improve security and the ability to change password

See the [open issues](https://github.com/matthewsmithwarren/finapp/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Matthew Smith Warren - [@matthewswarren](https://twitter.com/matthewswarren) - matthewsmithwarren@gmail.com

Project Link: [https://github.com/matthewsmithwarren/finapp](https://github.com/matthewsmithwarren/finapp)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Creating a Flask Web Server in EC2 on the AWS Free Tier from scratch!](https://youtu.be/z5XiVh6v4uI)
* [Step-by-step visual guide on deploying a Flask application on AWS EC2](https://medium.com/techfront/step-by-step-visual-guide-on-deploying-a-flask-application-on-aws-ec2-8e3e8b82c4f7)
* [API Keys Explained: What They Are and How to Use Them](https://blog.dreamfactory.com/api-keys-explained-what-they-are-and-how-to-use-them/#:~:text=There%20are%20two%20main%20types,server%2Dto%2Dserver%20communications.)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/matthewsmithwarren/finapp.svg?style=for-the-badge
[contributors-url]: https://github.com/matthewsmithwarren/finapp/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/matthewsmithwarren/finapp.svg?style=for-the-badge
[forks-url]: https://github.com/matthewsmithwarren/finapp/network/members
[stars-shield]: https://img.shields.io/github/stars/matthewsmithwarren/finapp.svg?style=for-the-badge
[stars-url]: https://github.com/matthewsmithwarren/finapp/stargazers
[issues-shield]: https://img.shields.io/github/issues/matthewsmithwarren/finapp.svg?style=for-the-badge
[issues-url]: https://github.com/matthewsmithwarren/finapp/issues
[license-shield]: https://img.shields.io/github/license/matthewsmithwarren/finapp.svg?style=for-the-badge
[license-url]: https://github.com/matthewsmithwarren/finapp/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/matthewsmithwarren
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
