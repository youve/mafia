# Mafia Utilities

[Mafia](https://wiki.mafiascum.net/index.php?title=Main_Page), also called Werewolf, is a game in which an uninformed majority of players, the town, try to guess the identities of an informed minority of players, the mafia. The game has a dayphase, in which the town -- and members of the mafia who are pretending to be town -- decide on who to eliminate from play by voting. Then the nightphase starts in which the mafia choose a town player to eliminate, and any town player with a special role can use their role to investigate/protect/etc. Town wins if the mafia is eliminated. Mafia wins if they gain a majority.

Modding mafia games online is fun but comes with some tedious administrative aspects: setting up the game threads, sending each player their role, posting vote counts throughout the day so players know who is being considered for elimination.

## mafiaMod.py

`mafiaMod.py` randomises the playerlist and then uses Selenium to sets up the game threads, send out role PMs. It is almost complete and can handle most of the pregame process for a [newbie game](https://forum.mafiascum.net/viewtopic.php?f=4) at this time.

## mafiaDeadlines.py

`mafiaDeadlines.py` is a program that works in conjunction with [schedule.py](https://github.com/youve/schedule/blob/master/schedule.py), producing output in a format that [main](https://github.com/youve/schedule/blob/master/files/main) can understand.

When I post a votecount during the dayphase, I like to increase the size of the deadline as we get closer to the deadline so that players have a visual reminder of how much time they have left to make their decision, to a maximum of 200 when there's 24 hours left. If the dayphase lasts 7 days, the deadline in a new votecount should increase by 5 every 7 hours and 12 minutes. If the dayphase lasts 10 days, then it should increase every 10 hours and 48 minutes. I used to do the math by hand, but now I have this.

## ruleOf3.py

When you are a member of the town, not knowing anybody's alignment but you're own, you're approximately equally likely to pay attention to anybody. Suppose there are 13 players alive, 1 is you, and 3 of them are mafia. When you mention 3 people in a post, then 9/12×8/11×7/10 == 38% of the time, all 3 people you mention will be town. 49% of the time, one will be mafia. 12% of the time, 2 will be mafia, and <1% of the time all three will be mafia.

When you are a member of the mafia, you won't follow this pattern at all. You will either talk about your fellow mafiosos too much or too little. You can use this script to get a feeling for how often your posts should be a townies vs. about mafiosos.

## removeBraces.py

While I was working out mafiaMod.py, it took me a while to settle on a template that I liked for inserting variables into the files. Ultimately, I decided that I didn't want to use braces but I didn't want to remove them from all of those files by hand.