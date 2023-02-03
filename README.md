# SleeperDraftOrderFetcher-
SleeperDraftOrderFetcher is a Python script that uses the Sleeper API to determine the draft order for future years in a Sleeper dynasty fantasy football league. It takes into account the current Max PF standings of the league and outputs the draft order for future seasons and shows who currently has each pick. 

Sleeper API Documentation: https://docs.sleeper.com/#introduction

This script currently only sorts draft order by Max PF. The intended use is to run it each week of the season to see what the current draft order would look like if the season ended on that day.

You'll need the league ID for your league. This can be found in the URL of your Sleeper league: https://sleeper.com/leagues/**<this_number_right_here>**/matchup. Or if you open the App and go to your league -> League tab -> Settings (the gear icon) -> General, and then scroll to the bottom. 

![](https://github.com/george-harding/SleeperDraftOrderFetcher-/blob/main/SleeperDraftOrderFetcher.gif)
