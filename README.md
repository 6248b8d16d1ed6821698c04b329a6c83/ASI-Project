<h1 align="center">ASI-Project</h1>

<h3 align="center">Connected Anywhere Across the Globe</h3>

<p align="center">
  <img src="https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/ef6178148852de43ce7a0f96ca962e0351b67081/assets/images/Empowering%20Access%20to%20Information.jpeg" alt="ASI Project Architecture" width="500"/>
</p>

## Introduction

Autonomous Support for Information (ASI) enables users to access online information through various channels depending on their
needs. Utilizing advanced technologies like cloud computing and machine learning, ASI autonomously retrieves and delivers relevant
data from websites, databases, and other platforms. It features intelligent data retrieval, continuous real-time updates, and
personalized interactions through a virtual assistant using natural language processing (NLP).

The algorithm relies on internal and external sources to answer queries. Here is a simplified diagram representing ASI architecture:

<p align="center">
  <img src="https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/df701badcfc6dafd14efdfdbd149a1b50e143c4f/assets/ASI%20Architecture.png" alt="ASI Project Architecture" width="600"/>
</p>

## Capabilities

1. Core Personality: Define the personality of ASI.
2. Specific Tasks Execution: Create personalized tasks for ASI to
perform. Default tasks include the following: executing POST
Requests, calculating, currency conversion, searching
Google Maps, switching default sources for point 3, and
searching on ChatGPT, Claude, Wikipedia, Gemini, and WolframAlpha.
Extra tasks could be sending emails, placing orders to buy
stocks, getting weather forecasts, etc.
3. Answer any question using the default sources. The default
source can be switched anytime from the following: ChatGPT,
Wikipedia, Claude, Gemini, and WolframAlpha.
4. Memory: Remember your preferences. The data is stored on a
DynamoDB table that you can consult, modify, or erase
anytime.

## Quick Start

To begin, you need to choose between three methods to access your virtual assistant:
- POST requests: search the web with a low internet connection.
- Telegram: search the web with a low internet connection.
- SMS: search the web without an internet connection.

Then, you can follow the step-by-step instructions for each of them:
- [Build a voice bot accessible via POST Method](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/98af5bfc1d21ca39b53dd55bd87bff93dbd252a2/docs/Build%20a%20Voice%20Bot%20Running%20on%20AWS.md)
- Build a chatbot accessible via Telegram.
- Build a chatbot accessible via SMS.


## Comparison Of Methods
<div align="center">
  <table>
    <tr>
      <th></th>
      <th>Telegram</th>
      <th>POST Method</th>
      <th>SMS</th>
    </tr>
    <tr>
      <td>Range Price</td>
      <td>Free – $0.005 per query</td>
      <td>Free – $0.005 per query</td>
      <td>$0.0079 – $0.0208 per query<br>+ $1.15 per month</td>
    </tr>
    <tr>
      <td>Accessible Via Phone</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Require Internet</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>No</td>
    </tr>
    <tr>
      <td>Require Extra Material</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
    </tr>
    <tr>
      <td>Type of Commands</td>
      <td>Written</td>
      <td>Written / Vocal</td>
      <td>Written</td>
    </tr>
    <tr>
      <td>External App Required</td>
      <td>Yes</td>
      <td>No</td>
      <td>No</td>
    </tr>
    <tr>
      <td>Chat History</td>
      <td>Yes</td>
      <td>No</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Access to Instructions</td>
      <td>Free</td>
      <td>Free</td>
      <td>Free</td>
    </tr>
  </table>
</div>


