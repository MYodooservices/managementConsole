
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from odoo import models, fields
from odoo.http import request
from odoo import http
import odoo.tools as tools
import os
import configparser
import odoo
from odoo import api


from proxmoxer import ProxmoxAPI



class PMC(models.TransientModel):
    _name = 'mmc.pmc'
    _inherit = ['multi.step.wizard.mixin'] 

    host = fields.Char(string='proxmox host with port', required=True)
    user = fields.Char(string='user', required=True)
    password = fields.Char(string='password', required=True)

    version = fields.Char(string='proxmox version')


    def getVersion(self):
        proxmox = ProxmoxAPI(
            self.host, user=self.user, password=self.password, verify_ssl=False
        )
        self.version = proxmox.version.get()
        print(self.version)
        print("pve update: ")
        print(proxmox.nodes("pve").apt.update)
        print("--")

        for node in proxmox.nodes.get():
            for vm in proxmox.nodes(node["node"]).lxc.get():
                print("{0}. {1} => {2}".format(vm["vmid"], vm["name"], vm["status"]))

        #proxmox.nodes("pve").lxc("102").clone.post(newid="106")




    
    @api.model
    def _selection_state(self):
        return [
            ('start', 'Start'),
            ('gui', 'GUI')
        ]

    @api.model
    def _default_project_id(self):
        return self.env.context.get('active_id')

    def state_exit_start(self):
        self.getVersion()
        self.state = 'gui'

    def state_previous_gui(self):
        self.state = 'start'
  


    
        
  
    
    
   
