# Common

Extractors have these entities in common:

## Settings Tab

- `default destination`: if the user has 'default' as `Destination` it will use this extraction path
- `sleep`: How much to sleep between requests and downloads

## User Table

- `Sel`: Selected users for operations
- `Skip`: Skip the user, don't extract
- `Note`: A note field for the user
- `User Handle`: It may be called differently, it's the name of the user to extract. Extractors might want a particular format explained below, only include the **Bold** part
- `Destination Path`: The user files during the extraction will be saved here
- `Extracted (UNIX)`: Saves the exact date when the user last got extracted
- `Auto`: Finds latest UNIX timestamp based on the user's folder
- `Delete Sql`: Delete the sql file that keeps the user's file history, press if you want to be able to download pictures that have already been marked as downloaded
- `Cursor ID`: Restart the extraction from this point (must be a valid cursor for the timeline)

# Gallery-dl Extractors

## Twitter

Settings Tab

- `Output filename`: If set to NA2000 it will use the newer filenames, which is recommended
- `Copy last cursor`: When clicked it will copy the last valid cursor value that is saved during the user extraction

User Table

- `User Handle`: the handle of the user you want to extract, not the name or id (twitter.com/**Wikipedia**)
- `Extraction level`: Define the 'deepness' of the extraction
  - `Profile`: Just saves the metadata of the user profile
  - `Media`: Just run through the media tab (fast) `twitter.com/Wikipedia/media`
  - `Timeline` Run through `twitter.com/Wikipedia/timeline` or more depending if `Deep Timeline` is enabled
  - `Search` Also run through `twitter.com/search?q=from:Wikipedia`
  - `Conversations` Also run through `twitter.com/search?q=@Wikipedia filter:replies`, which is the mentions of the user by other people
  - For normal use, use `Timeline` If you user has an old account with
    lots of tweets use `Conversations` and `Deep Timeline`
- `Deep Timeline`: Also run through `twitter.com/Wikipedia/tweets` and `twitter.com/Wikipedia/with_replies` to get more tweets
- `Text Tweets`: Save text tweets in JSON format
- `Media`: Save pictures
- `Retweets`: Save retweet information

## Bluesky

User Table

- `Full User Handle`: the full version handle of the user you want to extract, not the name or id (bsky.app/**wiki-potd.bsky.social**)
- `Extraction level`: Define the 'deepness' of the extraction

  - `Profile`: Just saves the metadata of the user profile
  - `Normal`: Run through the whole profile

- `Skies`: Save text only posts in JSON format
- `Media`: Save pictures

## Furaffinity

Settings Tab

- `Descriptions`: Choose the format of descriptions metadata

User Table

- `User Handle`: The handle of the user you want to extract, not the name or id (furaffinity.net/gallery/**wikipedia**/)
- `Scraps`: Also run through `furaffinity.net/scraps/wikipedia/`

## Pixiv

Settings Tab

- `Convert ugoira to`: Convert the ugoira animation to a viewable format, choose between None, GIF, MKV, WEBM. GIF may include inconsistent framing times
- `Move ugoira frames to zip`: If disabled frames of ugoira files will be saved as normal images
- `Download novel full series`: When downloading a novel being part of a series, download all novels of that series
- `Fetch novel comments`: Fetch comments metadata

User Table

- `User ID`: The id of the user you want to extract (pixiv.net/users/**11**)
- `Novels`: Also run through `pixiv.net/en/users/11/novels`

## Kemonoparty

User Table

- `Kemono ID`: The id of the user you want to extract (kemono.cr/patreon/user/**12345**)
- `Type`: The service to use, (**patreon** of user 12345)
- `File meta`: Save metadata of files
- `User meta`: Save metadata of user
- `Announcements`: Save announcements about user
- `Revisions`: Save revisions
- `Comments`: Save comments

## Inkbunny

User Table

- `User Handle`: The handle of the user you want to extract (inkbunny.net/**Wikipedia**)
- `Scraps`: Include inkbunny.net/scraps/**Wikipedia**

## Itaku

User Table

- `User Handle`: The handle of the user you want to extract (itaku.ee/profile/**wikipedia**)

# YT-DLP Extractors

Settings Tab

- `Other arguments`: Append arguments to the config file
- `Embed metadata in video`: Embed metadata in the video when possible

User Table

- `Video Metadata`: Write metadata such as description, playlist info
- `Fetch Comments`: Save video comments

- `Quality`: Best quality from top to bottom
`Merge Best` merges the best audio and video for the best overall quality (bestvideo*+bestaudio/best)
`best` selects the best already-merged audio and video (bestvideo*)
`best audio only` only saves the best audio (bestaudio)
Others correspond to their resolution

## Youtube

User Table

- `Type`: The type of url you want to extract:  
`User Handle` -> youtube.com/**@YouTube**
`Playlist ID` -> youtube.com/playlist?list=**PLbpi6ZahtOH5-vtiiO8B5jLdL-A4SxGxO**

## Nicovideo

Settings Tab

- `Extraction language`: Choose to have nicovideo in japanese or english, comments and title will display differently based on this setting

User Table

- `Type`: The type of url you want to extract:  
`User ID` -> nicovideo.jp/user/**20112017**
`Mylist ID` -> nicovideo.jp/mylist/**74178860**
`Series ID` -> nicovideo.jp/series/**487189**
