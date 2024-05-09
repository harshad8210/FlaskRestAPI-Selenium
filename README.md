The Vahan Scraping App addresses the business challenge by offering a user-friendly API for retrieving vehicle details
directly from the Parivahan website. Leveraging web scraping techniques, the application programmatically extracts
relevant information from the website's HTML pages, bypassing the need for manual data entry or navigation. The Flask
framework provides the backbone for the application, offering a lightweight and modular structure for building web
applications in Python. With its intuitive design and efficient data retrieval capabilities, the Vahan Scraping App
offers a reliable solution for accessing up-to-date vehicle information.
---
**Key functionalities:**

- Robust Data Retrieval Engine: Powered by Python and integrated with web scraping library such as Selenium, the
  application boasts a robust data retrieval engine capable of extracting comprehensive vehicle details from the
  Parivahan website. Through automated processes, users can seamlessly retrieve information such as registration
  status, vehicle class, owner details, and more with minimal manual intervention.

- User-Friendly: The Vahan Scraping App features a user-friendly API designed for ease of navigation and intuitive
  operation. Users can easily input vehicle number, initiate data retrieval processes, and access detailed vehicle
  information.

- Automated Login and Captcha Solving: The Vahan Scraping App streamlines the login process by automating the
  submission of credentials and solving captcha challenges seamlessly. Utilizing sophisticated algorithms and
  integration with captcha-solving services, the application ensures a smooth and hassle-free login experience for
  users. By eliminating manual intervention in the authentication process, users can expedite access to the
  Parivahan website and initiate data retrieval operations without delay.

- Efficient Data Extraction: Leveraging advanced web scraping techniques and intelligent data extraction
  algorithms, the application efficiently retrieves vehicle details from the Parivahan website. Despite the
  website's limitation of allowing only five vehicle data retrievals per login session, the Vahan Scraping App
  optimizes resource utilization and maximizes efficiency to ensure seamless data retrieval operations. Through
  careful management of session persistence and resource allocation, the application circumvents limitations
  imposed by the Parivahan website, enabling users to access comprehensive vehicle information without constraints.

---
**Key Challenges:**

The development of the Vahan Scraping App posed several key challenges, among them being the need to design a robust and
scalable platform capable of efficiently handling the retrieval of vehicle details from the Parivahan website. The
following challenges were identified and addressed during the development process:

- Automating Captcha Solving : One of the significant challenges was automating captcha solving, which involved
  capturing and downloading captcha images from the Parivahan website. We implemented a solution by utilizing a captcha
  solving API that predicts captcha images, enabling automated captcha resolution and seamless data retrieval from the
  website.

- Session Persistence with Stored Cookies:  To maintain seamless user sessions and bypass repeated logins, we
  implemented a feature to store website login cookies securely in our database upon successful authentication. These
  cookies were then utilized in subsequent API requests, ensuring continuity of the session until a login was required
  again. This approach streamlined user interactions and enhanced efficiency by eliminating the need for repetitive
  authentication steps.

- Dynamic Browser Instance Management: To optimize performance and handle multiple requests efficiently, we introduced
  dynamic browser instance management. This feature dynamically adjusts the number of browser instances opened based on
  the workload and incoming requests to our API. By dynamically scaling browser instances, we ensured faster processing
  times and improved responsiveness, enabling the application to handle a higher volume of requests without sacrificing
  performance.

---
**Applied Technologies:**

    • Backend: Flask-Restx
    • Database: PostgreSQL
    • Load Testing: Locust
    • Automation & Scraping: Selenium
