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

import logging
import gettext
from exe.webui.block               import Block
from exe.webui.blockfactory        import g_blockFactory
from exe.engine.reflectionidevice  import ReflectionIdevice
from exe.webui                     import common

log = logging.getLogger(__name__)
_   = gettext.gettext


# ===========================================================================
class ReflectionBlock(Block):
    """
    ReflectionBlock can render and process ReflectionIdevices as XHTML
    """
    def __init__(self, idevice):
        """
        Initialize a new Block object
        """
        Block.__init__(self, idevice)
        self.activity    = idevice.activity 
        self.answer      = idevice.answer


    def process(self, request):
        """
        Process the request arguments from the web server
        """
        Block.process(self, request)
        
        if "acti"+self.id in request.args:
            self.idevice.activity = request.args["acti"+self.id][0]

        if "answer"+self.id in request.args:
            self.idevice.answer = request.args["answer"+self.id][0]
        

    def processMove(self, request):
        """
        Move this iDevice to a different node
        """
        Block.processMove(self, request)
        nodeId = request.args["move"+self.id][0]
        node   = self.idevice.parentNode.package.findNode(nodeId)
        if node is not None:
            self.idevice.setParentNode(node)
        else:
            log.error("addChildNode cannot locate "+nodeId)


    def processMovePrev(self, request):
        """
        Move this block back to the previous position
        """
        Block.processMovePrev(self, request)
        self.idevice.movePrev()


    def processMoveNext(self, request):
        """
        Move this block forward to the next position
        """
        Block.processMoveNext(self, request)
        self.idevice.moveNext()


    def renderEdit(self):
        """
        Returns an XHTML string with the form element for editing this block
        """
        self.activity = self.activity.replace("\r", "")
        self.activity = self.activity.replace("\n","\\n")
        self.activity = self.activity.replace("'","\\'")
        self.answer   = self.answer.replace("\r", "")
        self.answer   = self.answer.replace("\n","\\n")
        self.answer   = self.answer.replace("'","\\'")
        html  =  _("Activity:") + "<br/>"
        html += common.richTextArea("acti"+self.id, self.activity)
        html += _("Answer:") + "<br/>"
        html += common.richTextArea("answer"+self.id, self.answer)           
        html += "<br/>" + self.renderEditButtons()
        html += "</div>\n"
        return html


    def renderPage(self):
        """
        Returns an XHTML string for this block
        """
        html  = "<script type=\"text/javascript\">\n"
        html += "<!--\n"
        html += """
            function showAnswer(id,isShow){
                if (isShow==1){
                    document.getElementById("s"+id).style.display = "block";
                    document.getElementById("hide"+id).style.display = "block";
                    document.getElementById("view"+id).style.display = "none";
                }else{
                    document.getElementById("s"+id).style.display = "none";
                    document.getElementById("hide"+id).style.display = "none";
                    document.getElementById("view"+id).style.display = "block";
                }
            }\n"""           
        html += "//-->\n"
        html += "</script>\n"
        html += "<div id=\"iDevice\">\n"
        html += self.activity   
        html += '<div id="view%s" style="display:block";>' % self.id
        html += '<input type="button" name ="btnshow%s" ' % self.id
        html += 'value ="Show answers"' 
        html += 'onclick ="showAnswer(\'%s\',1)"/></div>\n ' % self.id
        html += '<div id="hide%s" style="display:none";>' % self.id
        html += '<input type="button" name ="btnhide%s"'  % self.id 
        html += 'value ="Hide answers"'
        html += 'onclick ="showAnswer(\'%s\',0)"/></div>\n ' % self.id
        html += '<div id="s%s" style="color: rgb(0, 51, 204);' % self.id
        html += 'display: none;">'
        html += self.answer
        html += "</div>\n"
        return html
    
    def renderView(self):
        """
        Returns an XHTML string for viewing this block
        """
        html = self.renderPage()
        html += "</div>\n"
        return html

    def renderPreview(self):
        """
        Returns an XHTML string for previewing this block
        """
        html  = self.renderPage()
        html += self.renderViewButtons()
        html += "</div>\n"
        return html


g_blockFactory.registerBlockType(ReflectionBlock, ReflectionIdevice)


# ===========================================================================
