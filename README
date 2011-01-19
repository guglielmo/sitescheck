Requirements
============

A periodic script (cron) checks a list of **contents** on the web. Whenever some content changes, with respect to the last visit, then a notification is sent to a lit of registered recipients.

A content is identified by a *URL* and an *xpath* expression.

Content is grabbed and hashed (see http://docs.python.org/py3k/library/hashlib.html).

Whenever a difference between computed and stored hashes emerges, the hash is overwritten in the content's record on the DB. Simultaneously, a notification via email (or maybe some other channel, in the future) is sent to a list of recipients.

A backend interface allows administrators to manage the list of contents and of recipients.

Architecture
============

The project is written in **Django**, so that a backend interface can be easily built through the automatically-generated admin site.

A custom *django-admin* command is implemented, in order to grab the content out of the web.
Each URL is visited and the xpath is grabbed, through the lxml.objectify library.

Contents and Recipients are the only models.

