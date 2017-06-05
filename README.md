# 2QuipE
Simple online quiplash

## Public Routes
**/** 

User enters name into a simple form, and submits to /join. If join succeeds, redirect
to lobby.

**/lobby**

Keeps track of current players in game, and repeatedly ping /check_started. If it
has, then move to answer.

**/answer**

Returns an html page with two questions to answer. There is a submit button which sends the responses to the server (/submit).
If 60 seconds elapses, submit is called regardless. Once submitted, we repeatedly ping /check_finished. If finished, proceed to
/vote.

**/vote**

Sends an html page with the first question and a voting interface. User submits vote and then pings the server for /check_voted
to make sure everyone else voted. Then, check_voted will return the next question, and this continues until all questions are finished,
in which case we move on to /scores.

**/scores**

Shows a page with all player scores on it.

## Helper Routes
**/join**

Accepts a POST request to join a game. If name is taken, return false.
If successful, return true.

**/start**

Set game start variable to true, and then assign questions.

**/check_started**

Returns true iff the game has been supported.

**/submit**

Collects and stores answers to questions

**/check_finished**

Returns true if everyone has submitted an answer.

**/submit_vote**

**/check_voted**

If all voted, return the next question. If there are no more questions, indicate to move on to /scores.
