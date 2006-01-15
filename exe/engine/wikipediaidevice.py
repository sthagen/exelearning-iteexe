# ===========================================================================
# eXe 
# Copyright 2004-2005, University of Auckland
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
A Wikipedia Idevice is one built from a Wikipedia article.
"""

import re
from exe.engine.beautifulsoup import BeautifulSoup
from exe.engine.idevice       import Idevice
from exe.engine.field         import TextAreaField
from exe.engine.translate     import lateTranslate
from exe.engine.path          import Path, TempDirPath
from exe.engine.resource      import Resource

import urllib
class UrlOpener(urllib.FancyURLopener):
    """
    Set a distinctive User-Agent, so Wikipedia.org knows we're not spammers
    """
    version = "eXe/exe@auckland.ac.nz"
urllib._urlopener = UrlOpener()

import logging
log = logging.getLogger(__name__)

# ===========================================================================
class WikipediaIdevice(Idevice):
    """
    A Wikipedia Idevice is one built from a Wikipedia article.
    """
    persistenceVersion = 6

    def __init__(self, defaultSite):
        Idevice.__init__(self, x_(u"Wikipedia Article"), 
                         x_(u"University of Auckland"), 
                         x_(u"""The Wikipedia iDevice takes a copy of an
article from en.wikipedia.org, including copying the associated images."""), 
                         u"", u"")
        self.emphasis         = Idevice.NoEmphasis
        self.articleName      = u""
        self.article          = TextAreaField(x_(u"Article"))
        self.article.idevice  = self
        self.images           = {}
        self.site             = defaultSite
        self.icon             = u"inter"
        self.systemResources += ["fdl.html"]


    def loadArticle(self, name):
        """
        Load the article from Wikipedia
        """
        self.articleName = name

        name = urllib.quote(name.replace(" ", "_"))
        try:
            net  = urllib.urlopen(self.site+'wiki/'+name)
            page = net.read()
            net.close()

        except IOError, error:
            log.warning(unicode(error))
            self.article.content = _(u"Unable to connect to ") + self.site
            return

        # avoidParserProblems is set to False because BeautifulSoup's
        # cleanup was causing a "concatenating Null+Str" error,
        # and Wikipedia's HTML doesn't need cleaning up.
        # BeautifulSoup is faster this way too.
        soup = BeautifulSoup(unicode(page, "utf8"), False)
        content = soup.first('div', {'id': "content"})

        if not content:
            log.error("no content")

        # clear out any old images
        for resource in self.userResources:
            resource.delete()
        self.userResources = []
            
        # download the images
        tmpDir = TempDirPath()
        for imageTag in content.fetch('img'):
            imageSrc  = unicode(imageTag['src'])
            imageName = imageSrc.split('/')[-1]

            # Search if we've already got this image
            if imageName not in self.images:
                if not imageSrc.startswith("http://"):
                    imageSrc = self.site + imageSrc
                urllib.urlretrieve(imageSrc, tmpDir/imageName)
                self.images[imageName] = True
                self.userResources.append(Resource(self.parentNode.package,
                                                   tmpDir/imageName))

            # We have to use absolute URLs if we want the images to
            # show up in edit mode inside FCKEditor
            imageTag['src'] = (u"/" + self.parentNode.package.name + 
                               u"/resources/" + imageName)

        self.article.content = self.reformatArticle(unicode(content))


    def reformatArticle(self, content):
        """
        Changes links, etc
        """
        content = re.sub(r'href="/wiki/', 
                         r'href="'+self.site+'wiki/', content)
        content = re.sub(r'<div class="editsection".*?</div>', '', content)
        #TODO Find a way to remove scripts without removing newlines
        content = content.replace("\n", " ")
        content = re.sub(r'<script.*?</script>', '', content)
        return content


    def __getstate__(self):
        """
        Re-write the img URLs just in case the class name has changed
        """
        log.debug("in __getstate__ " + repr(self.parentNode))

        # need to check parentNode because __getstate__ is also called by 
        # deepcopy as well as Jelly.
        if self.parentNode:
            self.article.content = re.sub(r'/[^/]*?/resources/', 
                                          u"/" + self.parentNode.package.name + 
                                          u"/resources/", 
                                          self.article.content)

        return Idevice.__getstate__(self)


    def delete(self):
        """
        Clear out any old images when this iDevice is deleted
        """
        self.images = {}
        Idevice.delete(self)

        
    def upgradeToVersion1(self):
        """
        Called to upgrade from 0.6 release
        """
        self.site        = _('http://en.wikipedia.org/')


    def upgradeToVersion2(self):
        """
        Upgrades v0.6 to v0.7.
        """
        self.lastIdevice = False
        

    def upgradeToVersion3(self):
        """
        Upgrades exe to v0.10
        """
        self._upgradeIdeviceToVersion1()
        self._site = self.__dict__['site']


    def upgradeToVersion4(self):
        """
        Upgrades exe to v0.11... what was I thinking?
        """
        self.site = self.__dict__['_site']


    def upgradeToVersion5(self):
        """
        Upgrades exe to v0.11... forgot to change the icon
        """
        self.icon = u"inter"


    def upgradeToVersion6(self):
        """
        Upgrades to v0.12
        """
        self._upgradeIdeviceToVersion2()
        self.systemResources += ["fdl.html"]

        if self.images and self.parentNode:
            for image in self.images:
                imageResource = Resource(self.parentNode.package, Path(image))
                self.userResources.append(imageResource) 

# ===========================================================================
