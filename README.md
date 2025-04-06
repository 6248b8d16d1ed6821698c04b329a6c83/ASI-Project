<h1 align="center">ASI-Project</h1>

<h3 align="center">Connected Anywhere Across the Globe</h3>

<p align="center">
  <img src="https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/ef6178148852de43ce7a0f96ca962e0351b67081/assets/images/Empowering%20Access%20to%20Information.jpeg" alt="ASI Project Architecture" width="500"/>
</p>

## Introduction

ASI, or Autonomous Support for Information, is a project that enables users to access online information through various channels based on their needs. Powered by cloud computing, AI language models, and other technologies, ASI autonomously retrieves and delivers relevant data from websites, databases, and other platforms, offering intelligent data retrieval, real-time updates, and personalized interactions via a virtual assistant using natural language processing (NLP). You can access ASI from your phone using Telegram, POST method, or even SMS, making it an incredibly versatile solution for staying connected and efficient while minimizing data usage.

While traveling abroad, internet costs can skyrocket, especially in countries with expensive roaming charges. For instance, answering five simple queries, like getting directions, checking the weather, or translating a phrase, could cost you a hefty 114.00€ (e.g., a French operator charges 9.70€ per MB when traveling to Albania) when using traditional apps and search engines, consuming 11,837 KB of data. However, with the ASI POST method, the same queries use only 56 KB, resulting in a minimal cost of just 0.54€, a savings of over €113. That's more than 200 times less data used, meaning you can stay connected and informed without breaking the bank. 

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
- [Build a chatbot accessible via Telegram](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/6fb81d960d7d3f198bcd9c8645fc42195312df28/docs/Build%20a%20Telegram%20Chatbot%20Running%20on%20AWS.md)
- [Build a chatbot accessible via SMS](https://github.com/6248b8d16d1ed6821698c04b329a6c83/ASI-Project/blob/6fb81d960d7d3f198bcd9c8645fc42195312df28/docs/Build%20an%20SMS%20chatbot%20Running%20on%20AWS.md)


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


