# Assessment

When your project is finished, or as it's in progress if it's helpful, assess your project. Review the [project rubric](http://cs.fablearn.org/courses/cs10/unit00/project/) and then decide how your project should score on each criterion. Write a paragraph for each criterion justifying your assessment with evidence from your code, planning document, and commit messages.

## Criterion A - Knowing, understanding, and computational thinking

**Score: 7/8**

*I can read documentation to use services written by others.*
I used the Wolfram Alpha API in my search() function
in the services module. I had to read the documentation to figure out what the address and parameters were to get information from Wolfram wolfram Alpha. This helped me return information to the user of my bot when they asked for a search.

*I understand HTTP communication between clients and servers.*
- I defined routes for each service in my bot_server.py file. This allows my bot to be accessible through HTTP requests and through the message platform
- I return descriptive error messages for my service functions if there is a problem with the data that gets sent to my bot in the HTTP request. This shows that I know that I need specific data in the payload of HTTP requests.
- I used functions from the helpers module to parse data from HTTP requests. This helped me use that data to determine the functionality of my bot.

*I effectively use the principles of decomposition and abstraction to make my code more efficient and elegant.*
- I used my search() function both to respond to a user's message from the messaging platform and to serve and HTTP request to the search endpoint. This demonstrates decomposition because my search() function only does a search, nothing else. This demonstrates abstraction because my search function can be used in multiple places throughout my project.

## Criterion B - Planning and development
**Score: 5/8**

*My project demonstrates the following learning claims... Here's why.*
*I can thoughtfully plan a large computer science project.*
Unfortunately, I  did not make a plannign document, so I have no evidence to show for this claim...

*I can iteratively develop a project using version control tools such as GitHub.*
As can be seen in my GitHub repo, I made many commits to this project. This indicates that I can use
version control to develop a project over time. Additionally, you will see from my commits that I started with
more simple services like `add()` and got hose working before moving on to more complicated services like
`search()` which used an excternal API.

*I can document my software so that it is readable and usable by others.*
I documented my project very well. Not only can you find a description of all my services in my README.md file,
I commented all of the functions I wrote so that anyone reading my code would always know what a function did, 
what it's parameters were, and what it returned. Addtionally, I wrote a detailed README describing how to use
my message bot code. All of this indicates that I was very concious of documenting my project so that it could be
read, understood, and used by others.

## Criterion C - Evaluation
**Score: 5/8**

*My project demonstrates the following learning claims... Here's why.*

*I can identify different scenarios in which my code may be used and outline the expected functionality of my code in these instances.*
I did a good job of outlining the general usage of my bot in the README file where I included a table of all my bots services, what they do, what parameters they take, and how they respond. This helped guide my development of my bot's services.
I didn't do this very well at addressing edge cases because there are a number of cases where my bot cannot handle unexpected input from the user. For example, my bot breaks if the user sends a fraction.

*I can develop a testing strategy to ensure my code works as expected.*
I didn't plan any tests for my project before I started coding.
But I did test my bot after annd made changes. For example, I forgot to return responses as JSONs at first and realized after testing that I should be returning JSONs. You can see this in my commit history in commit 7b999bec5bda515a87867b58e8860a58c48d675f
