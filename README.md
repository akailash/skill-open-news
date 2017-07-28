# Open News Skill (for Mycroft AI)

This skill makes Mycroft read out news from one the available sources. Currently the news sources supported are:
- Google
- Reddit
- BBC
- Fox
- CNN
- Reuters

*Note: This is assuming, Mycroft is already installed with all its requirements. If it is not installed already please refer to https://mycroft.ai/ or https://github.com/MycroftAI/mycroft-core*

To install this skill use one of the methods listed below.

## MSM install

`msm install https://github.com/akailash/skill-open-news.git`

## Git-clone install

Go to the skills path and clone this repository and install the required libraries with pip

- `cd /opt/mycroft/skills/`
- `git clone https://github.com/akailash/skill-open-news.git`
- `cd skill-open-news; sudo pip install -r requirements.txt`

Restart Mycroft

- `./mycroft.sh start`

## Usage:
* `headlines from google india about sushma`
* `headlines from google about chuck norris`
* `google headlines`
* `headlines from reddit about sushma swaraj`

## Current state
 
 Working features:
  - Tested Google and reddit sources
  - Tested whether it detects countries mentioned and updates locale
 
 Known issues:
  - Only Google RSS feed has the parameters to take in locale and find the news from the country mentioned.
  - Reddit RSS feed may list subreddits instead of actual news
 
 TODO:
  - Find and add other RSS news feeds as sources which can search based on topic as well as location mentioned

