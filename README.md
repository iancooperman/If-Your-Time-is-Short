# If Your Time Is Short

Not just any Reddit summarizer bot.

## Description

Let's face it, hardly anyone reads past the headline these days, especially not Redditors. I can't force anyone to start, but I can provide the next best thing: summaries! If Your Time Is Short is a Reddit bot that peruses /r/nottheonion, /r/offbeat, and other subreddits for rising posts linking to news articles and uses GPT-3-Turbo (only as advanced a model as needed) to reply to the post with a concise, bullet-pointed summary of the article's contents.

Check out [/u/IfYourTimeIsShort](https://www.reddit.com/user/IfYourTimeIsShort/)'s latest replies!

## Getting Started

### Dependencies

* [Python 3.12](https://www.python.org/downloads/release/python-3120/) (required libraries can be found in requirements.txt)
* OpenAI API access
* A Reddit account with API access

### Installing

1. Clone the repository to your computer.
2. Create a venv
3. Use pip to download the required libraries
4. Set up a config.ini following config.ini.example as a guide

### Executing program

1. Run main.py
2. That's it.
3. That's really it!

## Authors

[Ian Cooperman](mailto:ian.pl.cooperman@gmail.com)

## Version History
* 0.1
    * Initial Release

## Planned Future Revisions
- Transition to open-source LLM.
- Slight condensing of generated summaries. 

## License

This project is licensed under the GNU GPLv3 License - see the LICENSE.md file for details

## Acknowledgments
* [auto;tldr](http://autotldr.io) for providing the initial inspiration for this project.
* [@DomPizzie](https://twitter.com/dompizzie) for providing an amazing README template.
