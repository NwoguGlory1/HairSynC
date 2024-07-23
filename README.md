# Project Name
"HairSynC" 

## Introduction

Welcome to HairSynC, a brand that links lovers of authentic luxury hairs and wigs directly to trusted Hair Companies.

## Live Site url
 https://hairsync.onrender.com/

## FinalProject Blog Article:

## Authors GitHub urls: 
https://github.com/NwoguGlory1/HairSynC.git

https://github.com/fae713/django.git


## Authors LinkedIn urls: 
https://www.linkedin.com/in/nwogu-glory-a2a95020b/
https://www.linkedin.com/in/favour-michael/

## Installation
To run this project locally, follow these steps:

Clone the repository:
git clone https://github.com/NwoguGlory1/HairSynC.git

Navigate to the project directory:
cd hairsync
Install dependencies:
pip install -r requirements.txt

Set up your Django environment variables (e.g., database credentials, secret key).

Apply migrations:
python manage.py migrate

Activate virtual environment:
source ~/.virtualenvs/yournamedjango/Scripts/activate

Run the development server:
python manage.py runserver

Access the website at http://localhost:8000/store

## Usage
Browse through the different categories of hair products available on the website.
Click on All Products to view its details and add it to your cart.
Navigate to a specific product page (Straight Hairs, Wavy Hairs, etc) and click Add To Cart button to add it to cart.
Click the cart logo on the nav bar to navigate to the Shopping Page, review your selected items and proceed to checkout.
Select a choice Hair Company on the Checkout page. 
Choose a  shipping and payment option to complete your purchase. 
Note: HairSynC website did not integrate delivery or shipping info but provides users the option to choose any shipping option available on the platform.

## Contributing
We welcome contributions from the community to improve HairSynC. If you'd like to contribute, please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/improvement).
Make your changes.
Commit your changes (git commit -am 'Add new feature').
Push to the branch (git push origin feature/improvement).
Create a new Pull Request.

 ## Related Projects
 Hair.com.ng
 https://www.naijabeautyhair.com

## Licensing
Distributed under the MIT License. See `LICENSE` for more information.

## Screenshot url
https://imgur.com/a/obVzsup
https://imgur.com/a/g4J1d7j

HairSynC was inspired from  the need to provide a platform where lovers of quality luxury hair can always get only authentic hairs directly from trusted hair companies, without having to haggle with the wholesalers who might at the end of the day not offer quality hairs/wigs to customers. From a first hand experience in the hair selling business, potential customers may be overwhelmed by the numerous number of wholesalers offering different textures of human hairs, some customers has run into the risk of having to purchase fake hairs, what some people funningly call "sponge" from these wholsalers and so, the team imagined a platform where the hair companies themselves, trusted ones that produce only authentic hairs are linked directly to the customers. The customers can get to interact with several of  these hair companies and from their price range purchase any hair they want with the confidence that it will always be quality. 
In as much as this project was done for passion, the platform obviously is an E-commerce website and this is one of the websites that its importance cannot be over-emphasized. For one, people have needs to buy or sell anything everyday and so, we channeled our passion towards building one of the important sites that can never get old- HairSynC. 

Due to the limited number of human hair types we used for the website, we assumed that the listed Hair Companies that a user can select from our platform will always provide all the hair types that a user selects from the product page.   
The most technical difficulty we experienced would be getting the Cart functionality right. This required a good knowlege of JavaScript. We were able to make the backend to correctly fetch items users add to cart by clicking the Add to Cart button, but we struggled with the JavaScript that would cause the Cart counter on the nav bar to reflect this count. It is only when the user clicks on this same Cart on the nav bar and navigates to the shopping cart page that the user can see the listed items that he/she has added to the cart. Due to the time constraint, we resorted to removing the cart counter on the nav bar and across all the pages and we utilized an alert that informs the users that the item was successfully added to cart.  Also, when the user clicks the "Clear Cart" button on the shopping cart, it expected that the cart clears from the frontend and the data is deleted from the database, but on our page, the user will only see that the items in the cart has been deleted if the page is reloaded. We also struggled in the JavaScript fucntion that should fetch the "Total Amount" and "Total Quantity" for a given number of added item in cart and at the same time, the UpdateCart function responsible for any modification done by the user to the cart items on the shopping cart page.  We are still working to completely get the Cart functionality right.
