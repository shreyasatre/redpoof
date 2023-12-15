# redpoof
red(dit) po(st) of(fline): an app that downloads reddit posts and comments in easy-to-read format for offline viewing.

### Problem
Saving Reddit posts using the platform's functionality is possible, but if the author deletes the post, accessing it again, even with the URL, becomes impossible. 

Consequently, the risk of losing a valuable resource arises when the author decides to remove it from the website.Browser extensions exist that enable the saving of web pages as HTML for offline viewing, yet they come with the drawback of also downloading extraneous graphical elements that may not be relevant to the content.

What if there was a way to download only the text content and associated comments of the reddit post?

### Process
My first thought was to use Python's excellent web crawling utilities to extract the content of the reddit post along with the associated selective comments. 

In the course of researching methods to extract data from a Reddit post, a more nuanced approach emerged. Rather than relying on a straightforward crawl of the HTML page, I discovered the efficacy of leveraging an exceptional library known as [PRAW](https://praw.readthedocs.io/en/stable/index.html). 

This library proved to be a game-changer, providing the capability to access a wealth of information beyond what is visibly presented in the Reddit post. PRAW's functionality extended beyond mere HTML scraping, enabling a comprehensive extraction of data that enriched the depth and scope of the information gathered from the Reddit platform.‍

### Solution
In this project there are three main modules of the app :

1. Access the reddit post
3. Process the data associated with the post
4. Export the content to a simple HTML file

![alt text](https://assets-global.website-files.com/63402a8bbd098358bb9773a4/6515e92be62346dabb60ab02_gui-redpoof.jpg)
   
