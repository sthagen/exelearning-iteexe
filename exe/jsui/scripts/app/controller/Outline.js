// ===========================================================================
// eXe
// Copyright 2012, Pedro Peña Pérez, Open Phoenix IT
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//===========================================================================

Ext.define('eXe.controller.Outline', {
    extend: 'Ext.app.Controller',

    stores: ['OutlineXmlTreeStore'],
    
    refs: [{
	    	selector: '#outline_treepanel',
	    	ref: 'outlineTreePanel'
    	}, {
    		selector: '#outline_add_node',
    		ref: 'outlineAddNodeBtn'
    	}, {
    		selector: '#outline_del_node',
    		ref: 'outlineDelNodeBtn'
    	}, {
    		selector: '#outline_ren_node',
    		ref: 'outlineRenNodeBtn'
    	}, {
    		selector: 'outlinetoolbar1',
    		ref: 'outlineToolBar1'
    	}
    ],
    
    init: function() {
        this.control({
        	'#outline_treepanel': {
        		itemclick:	this.onNodeClick,
        		itemdblclick: this.onNodeRename
        	},
        	'#outline_add_node': {
        		click: this.onNodeAdd
        	},
        	'#outline_del_node': {
        		click: this.onNodeDel
        	},
        	'#outline_ren_node': {
        		click: this.onNodeRename
        	}
        });
    },
    
    onLaunch: function() {
    	this.reload();
    },
    
    onNodeClick: function(view, record, item, index, e, eOpts) {
    	this.loadNodeOnAuthoringPage(record.data.id);
        document.title = "eXe : " + record.data.text;
    },
    
    onNodeAdd: function(button, e, eOpts) {
    	var outlineTreePanel = this.getOutlineTreePanel(),
    		selected = outlineTreePanel.getSelectionModel().getSelection(),
    		nodeid = '0';
    	
    	if (selected != 0)
    		nodeid = selected[0].data.id;
    	this.disableButtons();
		nevow_clientToServerEvent('AddChild', this, '', nodeid);    		
    },
    
    onNodeDel: function(button, e, eOpts) {
    	var outlineTreePanel = this.getOutlineTreePanel(),
    		selected = outlineTreePanel.getSelectionModel().getSelection(),
    		nodeid = '0';
    	
    	if (selected != 0)
    		nodeid = selected[0].data.id;
    	if (nodeid != '0') { 
    		msg = new Ext.Template(_('Delete "{node}" node and all its children?')).apply({node: selected[0].data.text});
    		Ext.Msg.show( {
    			title: _('Confirm'),
    			msg: msg,
    			scope: this,
    			modal: true,
    			buttons: Ext.Msg.YESNO,
    			fn: function(button) {
					if (button == "yes")	{
						this.disableButtons();
						nevow_clientToServerEvent('DelNode', this, '', nodeid);
			    	}
    			}
    		});
    	}
	},

    onNodeRename: function() {
    	var outlineTreePanel = this.getOutlineTreePanel(),
    		selected = outlineTreePanel.getSelectionModel().getSelection(),
    		nodeid = '0';
    	
    	if (selected != 0)
    		nodeid = selected[0].data.id;
		title = new Ext.Template(_('Rename "{node}" node')).apply({node: selected[0].data.text});
		Ext.Msg.show({
			prompt: true,
			title: title,
			msg: _('Enter the new name:'),
			buttons: Ext.Msg.OKCANCEL,
			multiline: false,
			value: selected[0].data.text,
			scope: this,
			fn: function(button, text) {
				if (button == "ok")	{
					this.disableButtons();
					nevow_clientToServerEvent('RenNode', this, '', nodeid, text);
		    	}
			}
		});
    },

    loadNodeOnAuthoringPage: function(node) {
        var authoring = Ext.get('authoringIFrame').dom.contentWindow;
        if (authoring && authoring.submitLink)
    		authoring.submitLink('changeNode', node, 0);
    },
    
    //called from exe.jsui.outlinepane.OutlinePane.handleSetTreeSelection
    select: function(nodeid) {
    	var outlineTreePanel = this.getOutlineTreePanel(),
    		selmodel = outlineTreePanel.getSelectionModel(),
    		store = this.getOutlineXmlTreeStoreStore();
    		
    	node = store.getNodeById(nodeid);
    	if (node) {
    		selmodel.select(node);
    		this.loadNodeOnAuthoringPage(node.data.id);
            document.title = "eXe : " + node.data.text;
    	}
    	this.enableButtons();
    },
    
    enableButtons: function() {
    	this.getOutlineAddNodeBtn().enable();
    	this.getOutlineDelNodeBtn().enable();
    	this.getOutlineRenNodeBtn().enable();
    },
    
    disableButtons: function() {
    	this.getOutlineAddNodeBtn().disable();
    	this.getOutlineDelNodeBtn().disable();
    	this.getOutlineRenNodeBtn().disable();
    },

    reload: function() {
    	var store = this.getOutlineXmlTreeStoreStore();
    	store.load();
    }
});