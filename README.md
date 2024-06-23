The bot doesn't greet or provide info about usage (TODO)
It accepts messages in form of
Forwarded Message
{name}:{text} (regex: (.*?):\s*(.*) for reference) 
List of lines of text in previous format. (then and only then it shows a summary divided by user and sorted from most positive to most negative)
The telegram bot token should be placed in ".env" file
The bot support Polish and English language albeit the detection of which to use is bad approach of checking for polish diacritics characters.
