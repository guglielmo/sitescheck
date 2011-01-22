Requirements
============

A periodic script (cron) checks a list of **contents** on the web. Whenever at least one of the contents changes, with respect to the last visit, a notification is sent to a list of registered recipients.

A content is identified by a *URL* and an *xpath* expression.

Content is grabbed and hashed (see http://docs.python.org/py3k/library/hashlib.html).

A regular expression may be used in order to exclude parts of the content that contain time-varying strings (i.e. sessions, dates, hashes, ...)

Whenever a difference between computed and stored hashes emerges, the hash is overwritten in the content's record on the DB and the verification status is set to changed.

If an error occurs, the status is changed to 
Another script checks whether there was at least one change, and send a notification to all registered recipient.

A backend interface allows administrators to manage the list of contents and of recipients and see the verificatio or error status.

Architecture
============

The project is written in **Django**, so that a backend interface can be easily built through the automatically-generated admin site.

Custom *django-admin* commands are implemented, in order to grab the content out of the web, verify them and send notifications when needed.
Each URL is visited and the xpath is grabbed, through the lxml.objectify library.
The content is hashed through the hashlib.sha512 algorythm.

Contents and Recipients are the only models.


Details
=======

The chosen hashing algorythm is sha512, which produces a digest string of 64 hexabytes::

  import hashlib
  h = hashlib.sha512()
  h.update(content)
  print h.hexdigest()

