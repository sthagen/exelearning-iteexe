# ===========================================================================
# eXe 
# Copyright 2004-2006, University of Auckland
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================

"""
An RSS Idevice is one built from a RSS feed.
"""

import re

from exe.engine               import feedparser
from exe.engine.idevice       import Idevice
from exe.engine.field         import TextAreaField
from exe.engine.translate     import lateTranslate
from exe.engine.path          import Path, TempDirPath
from exe.engine.resource      import Resource


# ===========================================================================
class RssIdevice(Idevice):
    """
    An RSS Idevice is one built from a RSS feed.
    """
    def __init__(self):
        Idevice.__init__(self,
                         x_(u"RSS"), 
                         x_(u"Auckland University of Technology"), 
                         x_(u"""The RSS iDevice is used 
to provide new content to an individual users machine. Using this
iDevice you can provide links from a feed you select for learners to view."""), 
                         u"",
                         u"")
        self.emphasis         = Idevice.NoEmphasis
        self.rss              = TextAreaField(x_(u"RSS"))
        self.rss.idevice      = self
        self.icon             = u"inter"
        self._urlInstruc      = x_(u"""Enter an RSS URL for the RSS feed you 
want to attach to your content. Feeds are often identified by a small graphic
 icon (often like this <img src="/images/feed-icon.png" />) or the text "RSS". Clicking on the 
 icon or text label will display an RSS feed right in your browser. You can copy and paste the
URL into this field. Alternately, right clicking on the link or graphic will open a menu box;
click on COPY LINK LOCATION or Copy Shortcut. Back in eXe open the RSS bookmark iDevice and Paste the URL 
into the RSS URL field and click the LOAD button. This will extract the titles from your feed and
display them as links in your content. From here you can edit the bookmarks and add
 instructions or additional learning information.""")
        self.url              = ""
        

        
    # Properties
    urlInstruc      = lateTranslate('urlInstruc')

   
    def loadRss(self, url):
        """
        Load the rss
        """
        content = ""
        rssDic = feedparser.parse(url)
        length = len(rssDic['entries'])
        print str(length)
        if length > 0 :
            for i in range(0, length):
                content += '<p><A href="%s">%s</A></P>' %(
                    rssDic['entries'][i].link, rssDic['entries'][i].title)          

        self.rss.content = unicode(content)



# ===========================================================================
