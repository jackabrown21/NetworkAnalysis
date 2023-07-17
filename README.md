## Setup

In order to run this project, you'll need to create your own .env file in the project root directory and set the following variables:

    USER_AGENT=<Your User Agent>
    ACCEPT_ENCODING=<Your Accept-Encoding>
    HOST=<Your Host>
    FROM=<Your From>


The .env file should be in the same directory as your main Python script. Replace `<Your User Agent>`, `<Your Accept-Encoding>`, `<Your Host>`, and `<Your From>` with your actual values. The `USER_AGENT` should be your name and email, `ACCEPT_ENCODING` should typically be "gzip, deflate", `HOST` should be "www.sec.gov", and `FROM` should be your email. 

Please make sure to never commit your .env file to any public repositories to protect your sensitive data.
